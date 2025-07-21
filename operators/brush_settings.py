class SCTK_PT_brush_panel(bpy.types.Panel):
    bl_idname = 'DH_TOOLKIT_PT_brush_panel'
    bl_label = 'Brush'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'

    def __getattribute__(self, item):
        if item == 'is_popover':
            return False
        else:
            return super().__getattribute__(item)

    def paint_settings(self, context):
        settings = bpy.types.VIEW3D_PT_tools_brush_settings.paint_settings(context)
        return settings

    def draw(self, context):
        bpy.types.VIEW3D_PT_tools_brush_settings.draw(self, context)