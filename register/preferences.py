import bpy

class DH_ToolkitPreferences(bpy.types.AddonPreferences):
    bl_idname = "DH_Toolkit"

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

    def draw(self, context):
        layout = self.layout
        
        # Keymap settings - the proper way
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
    
    def find_kmi_from_idname(self, km, idname, properties=None):
        """Find keymap item by idname and optional properties"""
        for kmi in km.keymap_items:
            if kmi.idname == idname:
                if properties:
                    match = True
                    for prop_name, prop_value in properties:
                        if not hasattr(kmi.properties, prop_name) or getattr(kmi.properties, prop_name) != prop_value:
                            match = False
                            break
                    if match:
                        return kmi
                else:
                    return kmi
        return None

    def draw_keymap_item(self, layout, kc, km, kmi, label=""):
        """Draw individual keymap item with proper controls"""
        split = layout.split(factor=0.3)
        
        # Left side - checkbox and label
        row = split.row()
        row.prop(kmi, "active", text="")
        row.label(text=label)
        
        # Right side - keymap controls
        split.template_keymap_item_properties(kmi)

    def draw_keymap_settings(self, layout, context):
        """Draw keymap settings using Blender's built-in UI"""
        box = layout.box()
        box.label(text="Keymap Settings", icon='KEYINGSET')
        
        wm = context.window_manager
        kc = wm.keyconfigs.user
        
    def draw_keymap_settings(self, layout, context):
        """Draw keymap settings using Blender's built-in UI"""
        box = layout.box()
        box.label(text="Keymap Settings", icon='KEYINGSET')
        
        wm = context.window_manager
        kc = wm.keyconfigs.user
        
        # DEBUG: Show what we actually find
        debug_box = box.box()
        debug_box.label(text="Debug Info:")
        
        found_items = []
        for km in kc.keymaps:
            for kmi in km.keymap_items:
                if "DH_MT_" in str(kmi.properties.name if hasattr(kmi.properties, 'name') else '') or kmi.idname == "object.dh_smart_hide":
                    found_items.append((km.name, kmi.idname, getattr(kmi.properties, 'name', 'N/A'), kmi.type, kmi.active))
        
        if found_items:
            debug_box.label(text=f"Found {len(found_items)} DH Toolkit keymap items:")
            for km_name, idname, menu_name, key, active in found_items:
                debug_box.label(text=f"  {km_name}: {idname} -> {menu_name} ({key}) [{'Active' if active else 'Inactive'}]")
        else:
            debug_box.label(text="No DH Toolkit keymap items found!")
            debug_box.label(text="Available keymaps:")
            for km in list(kc.keymaps)[:10]:  # Show first 10
                debug_box.label(text=f"  {km.name}")
        
        # Try to draw one keymap item if we found any
        if found_items:
            box.separator()
            box.label(text="Keymap Controls:")
            
            # Find first item and try to draw it
            km_name, idname, menu_name, key, active = found_items[0]
            km = kc.keymaps.get(km_name)
            if km:
                for kmi in km.keymap_items:
                    if ((kmi.idname == idname and hasattr(kmi.properties, 'name') and kmi.properties.name == menu_name) or 
                        (kmi.idname == "object.dh_smart_hide")):
                        
                        # Try the template
                        split = box.split(factor=0.3)
                        row = split.row()
                        row.prop(kmi, "active", text="")
                        row.label(text=f"Test: {menu_name if menu_name != 'N/A' else idname}")
                        split.template_keymap_item_properties(kmi)
                        break

def register_preferences():
    bpy.utils.register_class(DH_ToolkitPreferences)

def unregister_preferences():
    bpy.utils.unregister_class(DH_ToolkitPreferences)