import bpy

class DH_OP_SetShortcutKey(bpy.types.Operator):
    bl_idname = "dh.set_shortcut_key"
    bl_label = "Click to press any key"
    bl_description = "Click then press any key to set it as the shortcut key"
    bl_options = {'REGISTER', 'INTERNAL'}

    button_text = "Click to set key"

    @classmethod
    def set_button_text(cls, text):
        cls.button_text = text
        # Force UI redraw
        for area in bpy.context.screen.areas:
            if area.type == 'PREFERENCES':
                area.tag_redraw()

    def invoke(self, context, event):
        DH_OP_SetShortcutKey.set_button_text("Press any key...")
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        ignored_keys = {
            'MOUSEMOVE', 'INBETWEEN_MOUSEMOVE', 
            'LEFTMOUSE', 'RIGHTMOUSE', 'MIDDLEMOUSE',
            'LEFT_CTRL', 'RIGHT_CTRL', 'LEFT_ALT', 'RIGHT_ALT', 
            'LEFT_SHIFT', 'RIGHT_SHIFT'
        }

        if event.value == 'PRESS' and event.type not in ignored_keys:
            prefs = context.preferences.addons["DH_Toolkit"].preferences
            prefs.key_type = event.type
            DH_OP_SetShortcutKey.set_button_text(f"Key: {event.type}")
            
            # Update keymap
            from .keymap import update_keymap
            update_keymap()
            
            return {'FINISHED'}
        
        elif event.type == 'ESC':
            DH_OP_SetShortcutKey.set_button_text("Click to set key")
            return {'CANCELLED'}
        
        return {'RUNNING_MODAL'}

class DH_ToolkitPreferences(bpy.types.AddonPreferences):
    bl_idname = "DH_Toolkit"

    # Keymap settings
    key_type: bpy.props.StringProperty(
        name="Key",
        description="Key for the pie menu",
        default='X',
        update=lambda self, context: self._update_keymap()
    )
    
    use_shift: bpy.props.BoolProperty(
        name="Shift",
        description="Use Shift modifier",
        default=True,
        update=lambda self, context: self._update_keymap()
    )
    
    use_alt: bpy.props.BoolProperty(
        name="Alt",
        description="Use Alt modifier",
        default=False,
        update=lambda self, context: self._update_keymap()
    )
    
    use_ctrl: bpy.props.BoolProperty(
        name="Ctrl",
        description="Use Ctrl modifier",
        default=False,
        update=lambda self, context: self._update_keymap()
    )

    # Default projects directory
    default_projects_dir: bpy.props.StringProperty(
        name="Default Projects Directory",
        description="Base path for new projects and unsaved scenes",
        subtype='DIR_PATH',
        default=""
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

    # Add these to DH_ToolkitPreferences class
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

    def _update_keymap(self):
        """Update keymap when preferences change"""
        try:
            from .keymap import update_keymap
            update_keymap()
        except:
            pass  # Ignore during initial registration

    def draw(self, context):
        layout = self.layout
        
        # Keymap settings
        box = layout.box()
        box.label(text="Keymap Settings", icon='KEYINGSET')
        
        row = box.row()
        row.prop(self, "use_shift")
        row.prop(self, "use_alt")
        row.prop(self, "use_ctrl")
        
        row = box.row()
        row.label(text="Shortcut Key:")
        row.operator("dh.set_shortcut_key", text=DH_OP_SetShortcutKey.button_text)
        
        if self.key_type:
            box.label(text=f"Current key: {self.key_type}")

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

def register_preferences():
    bpy.utils.register_class(DH_OP_SetShortcutKey)
    bpy.utils.register_class(DH_ToolkitPreferences)

def unregister_preferences():
    bpy.utils.unregister_class(DH_ToolkitPreferences)
    bpy.utils.unregister_class(DH_OP_SetShortcutKey)