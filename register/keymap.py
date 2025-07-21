import bpy
import addon_utils

# Store all keymap items for cleanup
addon_keymaps = []

def get_addon_preferences():
    """Get addon preferences with fallback"""
    try:
        return bpy.context.preferences.addons["DH_Toolkit"].preferences
    except:
        return None

def register_keymap():
    """Register all keymaps in one place"""
    prefs = get_addon_preferences()
    if not prefs:
        key, shift, alt, ctrl = 'X', True, False, False
    else:
        key = prefs.key_type
        shift = prefs.use_shift
        alt = prefs.use_alt
        ctrl = prefs.use_ctrl

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if not kc:
        return

    # Define all keymaps in one structure
    keymap_configs = [
        # (keymap_name, space_type, menu_idname)
        ("3D View", "VIEW_3D", "DH_MT_Main_Menu"),
        ("Mesh", "EMPTY", "DH_MT_Edit_Menu"),
        ("Sculpt", "EMPTY", "DH_MT_Sculpt_Menu"),
        ("Image Paint", "EMPTY", "DH_MT_Texture_Paint_Menu"),
        ("Weight Paint", "EMPTY", "DH_MT_Weight_Paint_Menu"),
        ("UV Editor", "EMPTY", "DH_MT_UV_Edit_Menu"),
        ("Node Editor", "NODE_EDITOR", "DH_MT_Shader_Editor_Menu"),
    ]

    # Register all keymaps
    for keymap_name, space_type, menu_name in keymap_configs:
        km = kc.keymaps.new(name=keymap_name, space_type=space_type)
        kmi = km.keymap_items.new(
            "wm.call_menu_pie",
            key, "PRESS",
            shift=shift, alt=alt, ctrl=ctrl
        )
        kmi.properties.name = menu_name
        addon_keymaps.append((km, kmi))

    # Add other keymaps (loop select, smart hide, etc.)
    _register_additional_keymaps(kc)

def _register_additional_keymaps(kc):
    """Register non-pie menu keymaps"""
    # Loop select
    km_loop = kc.keymaps.new(name="Mesh", space_type="EMPTY")
    
    kmi1 = km_loop.keymap_items.new('mesh.loop_select', 'LEFTMOUSE', 'DOUBLE_CLICK')
    kmi1.properties.extend = False
    kmi1.properties.deselect = False
    kmi1.properties.toggle = False

    kmi2 = km_loop.keymap_items.new('mesh.loop_select', 'LEFTMOUSE', 'DOUBLE_CLICK', shift=True)
    kmi2.properties.extend = True
    kmi2.properties.toggle = True

    kmi3 = km_loop.keymap_items.new('mesh.loop_select', 'LEFTMOUSE', 'DOUBLE_CLICK', ctrl=True)
    kmi3.properties.extend = False
    kmi3.properties.deselect = True
    kmi3.properties.toggle = False

    # Smart Hide
    km_hide = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
    kmi_hide = km_hide.keymap_items.new(
        idname="object.dh_smart_hide",
        type='H', value='PRESS', ctrl=True
    )

    addon_keymaps.extend([
        (km_loop, kmi1), (km_loop, kmi2), (km_loop, kmi3),
        (km_hide, kmi_hide)
    ])

def unregister_keymap():
    """Clean up all keymaps"""
    for km, kmi in addon_keymaps:
        try:
            km.keymap_items.remove(kmi)
        except:
            pass
    addon_keymaps.clear()

def update_keymap():
    """Update keymaps when preferences change"""
    unregister_keymap()
    register_keymap()