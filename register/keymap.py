import bpy

# Store all keymap items for cleanup
addon_keymaps = []

def get_keymap_settings():
    """Get keymap settings from addon preferences"""
    try:
        prefs = bpy.context.preferences.addons["DH_Toolkit"].preferences
        return {
            'key': prefs.keymap_key,
            'shift': prefs.keymap_shift,
            'alt': prefs.keymap_alt,
            'ctrl': prefs.keymap_ctrl
        }
    except:
        # Fallback to defaults if preferences not available
        return {
            'key': 'X',
            'shift': True,
            'alt': False,
            'ctrl': False
        }

def register_keymap():
    """Register all keymaps with settings from preferences"""
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if not kc:
        return

    # Get key settings from preferences
    settings = get_keymap_settings()
    key = settings['key']
    shift = settings['shift'] 
    alt = settings['alt']
    ctrl = settings['ctrl']

    print(f"🔥 DH Toolkit: Registering keymaps with {key} + modifiers: Ctrl={ctrl}, Alt={alt}, Shift={shift}")

    # Define all pie menu keymaps
    keymap_configs = [
        # (keymap_name, space_type, menu_idname, description)
        ("3D View", "VIEW_3D", "DH_MT_Main_Menu", "Main Menu"),
        ("Mesh", "EMPTY", "DH_MT_Edit_Menu", "Edit Menu"),
        ("Sculpt", "EMPTY", "DH_MT_Sculpt_Menu", "Sculpt Menu"),
        ("Image Paint", "EMPTY", "DH_MT_Texture_Paint_Menu", "Texture Paint Menu"),
        ("Weight Paint", "EMPTY", "DH_MT_Weight_Paint_Menu", "Weight Paint Menu"),
        ("UV Editor", "EMPTY", "DH_MT_UV_Edit_Menu", "UV Edit Menu"),
        ("Node Editor", "NODE_EDITOR", "DH_MT_Shader_Editor_Menu", "Shader Editor Menu"),
        ("Outliner", "OUTLINER", "DH_MT_Outliner_Menu", "Outliner Menu"),
    ]

    # Register pie menu keymaps
    for keymap_name, space_type, menu_name, description in keymap_configs:
        km = kc.keymaps.new(name=keymap_name, space_type=space_type)
        kmi = km.keymap_items.new(
            "wm.call_menu_pie",
            key, "PRESS",
            shift=shift, alt=alt, ctrl=ctrl
        )
        kmi.properties.name = menu_name
        addon_keymaps.append((km, kmi))

    # Register other keymaps
    _register_additional_keymaps(kc)

def _register_additional_keymaps(kc):
    """Register non-pie menu keymaps"""
    # Mesh loop select keymaps
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

    # Smart Hide keymap
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
    print("🔥 DH Toolkit: Unregistered all keymaps")