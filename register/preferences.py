import bpy
import rna_keymap_ui

import bpy
import rna_keymap_ui

# Static list of common key types - no callback bullshit needed
COMMON_KEY_TYPES = [
    # Letters A-Z
    ('A', 'A', ''), ('B', 'B', ''), ('C', 'C', ''), ('D', 'D', ''), ('E', 'E', ''),
    ('F', 'F', ''), ('G', 'G', ''), ('H', 'H', ''), ('I', 'I', ''), ('J', 'J', ''),
    ('K', 'K', ''), ('L', 'L', ''), ('M', 'M', ''), ('N', 'N', ''), ('O', 'O', ''),
    ('P', 'P', ''), ('Q', 'Q', ''), ('R', 'R', ''), ('S', 'S', ''), ('T', 'T', ''),
    ('U', 'U', ''), ('V', 'V', ''), ('W', 'W', ''), ('X', 'X', ''), ('Y', 'Y', ''), ('Z', 'Z', ''),
    
    # Numbers 0-9
    ('ZERO', '0', ''), ('ONE', '1', ''), ('TWO', '2', ''), ('THREE', '3', ''), ('FOUR', '4', ''),
    ('FIVE', '5', ''), ('SIX', '6', ''), ('SEVEN', '7', ''), ('EIGHT', '8', ''), ('NINE', '9', ''),
    
    # Function keys
    ('F1', 'F1', ''), ('F2', 'F2', ''), ('F3', 'F3', ''), ('F4', 'F4', ''), ('F5', 'F5', ''),
    ('F6', 'F6', ''), ('F7', 'F7', ''), ('F8', 'F8', ''), ('F9', 'F9', ''), ('F10', 'F10', ''),
    ('F11', 'F11', ''), ('F12', 'F12', ''),
    
    # Common keys
    ('SPACE', 'Space', ''), ('TAB', 'Tab', ''), ('ESC', 'Escape', ''), ('RET', 'Enter', ''),
    ('BACK_SPACE', 'Backspace', ''), ('DEL', 'Delete', ''),
    
    # Arrow keys
    ('LEFT_ARROW', 'Left Arrow', ''), ('RIGHT_ARROW', 'Right Arrow', ''),
    ('UP_ARROW', 'Up Arrow', ''), ('DOWN_ARROW', 'Down Arrow', ''),
    
    # Mouse buttons
    ('LEFTMOUSE', 'Left Mouse', ''), ('RIGHTMOUSE', 'Right Mouse', ''), 
    ('MIDDLEMOUSE', 'Middle Mouse', ''), ('BUTTON4MOUSE', 'Mouse Button 4', ''),
    ('BUTTON5MOUSE', 'Mouse Button 5', ''),
    
    # Symbols
    ('COMMA', 'Comma', ''), ('PERIOD', 'Period', ''), ('SLASH', 'Slash', ''),
    ('BACK_SLASH', 'Backslash', ''), ('MINUS', 'Minus', ''), ('EQUAL', 'Equal', ''),
    ('LEFT_BRACKET', '[', ''), ('RIGHT_BRACKET', ']', ''), ('SEMI_COLON', 'Semicolon', ''),
    ('QUOTE', 'Quote', ''), ('ACCENT_GRAVE', 'Grave Accent', ''),
]

class DH_ToolkitPreferences(bpy.types.AddonPreferences):
    bl_idname = "DH_Toolkit"

    # Default projects directory
    default_projects_dir: bpy.props.StringProperty(
        name="Default Projects Directory",
        description="Base path for new projects and unsaved scenes",
        subtype='DIR_PATH',
        default=""
    )

    # KEYMAP SETTINGS - The shit that actually works
    keymap_key: bpy.props.EnumProperty(
        name="Key",
        description="Main key for DH Toolkit pie menus",
        items=COMMON_KEY_TYPES,
        default='X',
        update=lambda self, context: self.update_keymaps(context)
    )
    
    keymap_shift: bpy.props.BoolProperty(
        name="Shift",
        description="Use Shift modifier",
        default=True,
        update=lambda self, context: self.update_keymaps(context)
    )
    
    keymap_ctrl: bpy.props.BoolProperty(
        name="Ctrl", 
        description="Use Ctrl modifier",
        default=False,
        update=lambda self, context: self.update_keymaps(context)
    )
    
    keymap_alt: bpy.props.BoolProperty(
        name="Alt",
        description="Use Alt modifier", 
        default=False,
        update=lambda self, context: self.update_keymaps(context)
    )

    # Shader Builder settings
    naming_separator: bpy.props.EnumProperty(
        name="Separator",
        description="Character used to separate parts of texture names",
        items=[
            ('_', "Underscore (_)", "wood_basecolor_4k"),
            ('-', "Dash (-)", "wood-basecolor-4k"),
            ('.', "Dot (.)", "wood.basecolor.4k"),
            ('', "None", "woodbasecolor4k"),
        ],
        default='_'
    )
    
    # Simplified suffix properties (just the common ones)
    suffix_basecolor: bpy.props.StringProperty(name="Base Color Suffix", default="d")
    suffix_normal: bpy.props.StringProperty(name="Normal Suffix", default="n")
    suffix_roughness: bpy.props.StringProperty(name="Roughness Suffix", default="r")
    suffix_metallic: bpy.props.StringProperty(name="Metallic Suffix", default="m")
    suffix_orm: bpy.props.StringProperty(name="ORM Suffix", default="orm")
    suffix_height: bpy.props.StringProperty(name="Height Suffix", default="h")
    suffix_ao: bpy.props.StringProperty(name="AO Suffix", default="ao")
    suffix_emission: bpy.props.StringProperty(name="Emission Suffix", default="e")
    
    # Advanced toggle
    use_advanced_patterns: bpy.props.BoolProperty(
        name="Use Advanced Regex Patterns",
        description="Enable direct regex input for advanced users",
        default=False
    )
    
    # Advanced patterns (collapsed by default)
    regex_basecolor: bpy.props.StringProperty(name="Base Color Regex", default="")
    regex_normal: bpy.props.StringProperty(name="Normal Regex", default="")
    regex_roughness: bpy.props.StringProperty(name="Roughness Regex", default="")
    regex_metallic: bpy.props.StringProperty(name="Metallic Regex", default="")
    regex_orm: bpy.props.StringProperty(name="ORM Regex", default="")
    regex_height: bpy.props.StringProperty(name="Height Regex", default="")
    regex_ao: bpy.props.StringProperty(name="AO Regex", default="")
    regex_emission: bpy.props.StringProperty(name="Emission Regex", default="")

    # Text Overlay settings
    text_overlay_success_color: bpy.props.FloatVectorProperty(
        name="Success Color",
        description="Color for success messages",
        subtype='COLOR',
        default=(0.2, 1.0, 0.2, 1.0),
        size=4,
        min=0.0, max=1.0
    )

    text_overlay_error_color: bpy.props.FloatVectorProperty(
        name="Error Color", 
        description="Color for error messages",
        subtype='COLOR',
        default=(1.0, 0.2, 0.2, 1.0),
        size=4,
        min=0.0, max=1.0
    )

    text_overlay_info_color: bpy.props.FloatVectorProperty(
        name="Info Color",
        description="Color for info messages", 
        subtype='COLOR',
        default=(0.2, 0.6, 1.0, 1.0),
        size=4,
        min=0.0, max=1.0
    )

    text_overlay_show_outline: bpy.props.BoolProperty(
        name="Show Text Outline",
        description="Show outline around overlay text",
        default=False
    )

    def update_keymaps(self, context):
        """Reload keymaps when preferences change"""
        try:
            from ..register.keymap import unregister_keymap, register_keymap
            unregister_keymap()
            register_keymap()
            print(f"🔥 DH Toolkit: Updated keymaps to {self.get_keymap_string()}")
        except Exception as e:
            print(f"🔥 DH Toolkit: Failed to update keymaps: {e}")

    def get_keymap_string(self):
        """Get human-readable keymap string"""
        modifiers = []
        if self.keymap_ctrl:
            modifiers.append("Ctrl")
        if self.keymap_alt:
            modifiers.append("Alt") 
        if self.keymap_shift:
            modifiers.append("Shift")
        
        if modifiers:
            return f"{'+'.join(modifiers)}+{self.keymap_key}"
        else:
            return self.keymap_key

    def draw(self, context):
        layout = self.layout
        
        # Keymap settings - front and center
        self.draw_keymap_settings(layout, context)

        # Project settings
        layout.separator()
        proj_box = layout.box()
        proj_box.label(text="Project Settings", icon='FILE_FOLDER')
        proj_box.prop(self, "default_projects_dir")

        # Shader Builder settings (collapsed)
        layout.separator()
        shader_box = layout.box()
        shader_box.label(text="Shader Builder Texture Naming", icon='TEXTURE')
        
        shader_box.prop(self, "naming_separator")
        
        # Simple grid layout for suffixes
        grid = shader_box.grid_flow(row_major=True, columns=4, even_columns=True)
        grid.prop(self, "suffix_basecolor")
        grid.prop(self, "suffix_normal")
        grid.prop(self, "suffix_roughness")
        grid.prop(self, "suffix_metallic")
        grid.prop(self, "suffix_orm")
        grid.prop(self, "suffix_height")
        grid.prop(self, "suffix_ao")
        grid.prop(self, "suffix_emission")
        
        # Advanced toggle (collapsed by default)
        shader_box.prop(self, "use_advanced_patterns")
        
        if self.use_advanced_patterns:
            advanced_box = shader_box.box()
            advanced_box.label(text="Advanced Regex Patterns")
            
            grid = advanced_box.grid_flow(row_major=True, columns=2, even_columns=True)
            grid.prop(self, "regex_basecolor")
            grid.prop(self, "regex_normal")
            grid.prop(self, "regex_roughness")
            grid.prop(self, "regex_metallic")
            grid.prop(self, "regex_orm")
            grid.prop(self, "regex_height")
            grid.prop(self, "regex_ao")
            grid.prop(self, "regex_emission")
        
        # Text Overlay settings
        layout.separator()
        overlay_box = layout.box()
        overlay_box.label(text="Text Overlay Settings", icon='FONTPREVIEW')
        
        overlay_box.prop(self, "text_overlay_show_outline")
        
        grid = overlay_box.grid_flow(row_major=True, columns=3, even_columns=True)
        grid.prop(self, "text_overlay_success_color")
        grid.prop(self, "text_overlay_error_color") 
        grid.prop(self, "text_overlay_info_color")
    
    def draw_keymap_settings(self, layout, context):
        """Draw keymap settings with proper UI"""
        box = layout.box()
        box.label(text="🔥 DH Toolkit Keymaps", icon='KEYINGSET')
        
        # Current keymap display
        current_box = box.box()
        row = current_box.row()
        row.label(text="Current Shortcut:", icon='EVENT_SHIFT')
        row.label(text=self.get_keymap_string())
        
        # Keymap configuration
        config_box = box.box()
        config_box.label(text="Configure Shortcut:")
        
        # Key selection
        row = config_box.row()
        row.label(text="Key:")
        row.prop(self, "keymap_key", text="")
        
        # Modifiers
        row = config_box.row()
        row.label(text="Modifiers:")
        row.prop(self, "keymap_ctrl", text="Ctrl")
        row.prop(self, "keymap_alt", text="Alt") 
        row.prop(self, "keymap_shift", text="Shift")
        
        # Show existing keymap items from user keyconfig
        self.draw_existing_keymaps(box, context)
    
    def draw_existing_keymaps(self, layout, context):
        """Draw existing DH Toolkit keymaps from user keyconfig"""
        box = layout.box()
        box.label(text="Active Keymaps:", icon='SETTINGS')
        
        wm = context.window_manager
        kc = wm.keyconfigs.user
        if not kc:
            box.label(text="No user keyconfig available")
            return
        
        found_any = False
        
        # Look for our operators in user keymaps
        dh_operators = [
            "wm.call_menu_pie",  # Our pie menus
            "object.dh_smart_hide",  # Smart hide
        ]
        
        for km_name in ["3D View", "Mesh", "Sculpt", "Image Paint", "Weight Paint", "UV Editor", "Node Editor", "Outliner"]:
            km = kc.keymaps.get(km_name)
            if not km:
                continue
                
            for kmi in km.keymap_items:
                # Check for our pie menus
                if (kmi.idname == "wm.call_menu_pie" and 
                    hasattr(kmi.properties, 'name') and 
                    kmi.properties.name.startswith("DH_MT_")):
                    
                    found_any = True
                    row = box.row()
                    row.label(text=f"{km_name}:")
                    
                    # Use the proper template for keymap item display
                    sub_box = box.box()
                    try:
                        rna_keymap_ui.draw_kmi([], kc, km, kmi, sub_box, 0)
                    except:
                        # Fallback if draw_kmi fails
                        sub_box.label(text=f"Menu: {kmi.properties.name}")
                        sub_box.label(text=f"Key: {self.format_kmi_key(kmi)}")
                
                # Check for smart hide
                elif kmi.idname == "object.dh_smart_hide":
                    found_any = True
                    row = box.row()
                    row.label(text=f"{km_name}:")
                    
                    sub_box = box.box()
                    try:
                        rna_keymap_ui.draw_kmi([], kc, km, kmi, sub_box, 0)
                    except:
                        sub_box.label(text="Smart Hide")
                        sub_box.label(text=f"Key: {self.format_kmi_key(kmi)}")
        
        if not found_any:
            box.label(text="No DH Toolkit keymaps found. Try disabling/enabling the addon.")
    
    def format_kmi_key(self, kmi):
        """Format keymap item key for display"""
        modifiers = []
        if kmi.ctrl:
            modifiers.append("Ctrl")
        if kmi.alt:
            modifiers.append("Alt")
        if kmi.shift:
            modifiers.append("Shift")
        
        key_str = kmi.type
        if modifiers:
            return f"{'+'.join(modifiers)}+{key_str}"
        return key_str

def register_preferences():
    bpy.utils.register_class(DH_ToolkitPreferences)

def unregister_preferences():
    bpy.utils.unregister_class(DH_ToolkitPreferences)