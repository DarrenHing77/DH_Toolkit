import bpy
from ..icons.icons import load_icons


def draw_texture_paint_panels(layout, context):
    """Draw brush settings panels for texture painting"""
    col = layout.column(align=True)
    
    col.popover('VIEW3D_PT_tools_brush_settings_advanced', text="Advanced")
    col.popover('VIEW3D_PT_tools_brush_falloff', text="Falloff")
    col.popover('VIEW3D_PT_tools_brush_texture', text="Texture") 
    col.popover('VIEW3D_PT_tools_brush_stroke', text="Stroke")
    col.popover('VIEW3D_PT_tools_mask_texture', text="Mask")
    col.popover('VIEW3D_PT_tools_brush_display', text="Display")


class DH_MT_Texture_Paint_Menu(bpy.types.Menu):
    bl_idname = "DH_MT_Texture_Paint_Menu"
    bl_label = "DH Texture Paint Toolkit"

    def draw(self, context):
        icons = load_icons()
        pie = self.layout.menu_pie()

        # LEFT - Brushes (grid) above Image Management (not grid)
        col_left = pie.column()
        
        # Brushes - Grid layout, slightly bigger
        brush_box = col_left.box()
        brush_box.label(text='Brushes')
        brush_box.scale_y = 1.4  # Slightly bigger

        grid = brush_box.grid_flow(row_major=True, columns=3, even_columns=True)

        # Texture paint brushes using correct syntax
        brushes = [
            ("Brush", "builtin.brush"),
            ("Fill", "builtin_brush.fill"),
            ("Erase", "builtin_brush.erase_alpha"),
            ("Soften", "builtin_brush.soften"),
            ("Smear", "builtin_brush.smear"),
            ("Clone", "builtin_brush.clone"),
        ]
        
        for name, tool_id in brushes:
            op = grid.operator("wm.tool_set_by_id", text=name)
            op.name = tool_id

        # Image Management - Not grid, regular column
        image_box = col_left.box()
        image_box.label(text='Image Management')
        image_box.operator("image.new", text="New Image")
        image_box.operator("image.open", text="Open Image")
        if hasattr(bpy.ops.image, "save"):
            image_box.operator("image.save", text="Save Image")
        if hasattr(bpy.ops.image, "reload"):
            image_box.operator("image.reload", text="Reload Image")

        # RIGHT - Brush Settings Panels
        col_right = pie.column()
        draw_texture_paint_panels(col_right, context)

        # BOTTOM - Paint Options
        col_bottom = pie.column()
        box_bottom = col_bottom.box()
        self.draw_paint_options(box_bottom, context)
        
        # TOP - Canvas Navigation
        col_top = pie.column()
        box_top = col_top.box()
        self.draw_canvas_navigation(box_top, context)
        
        # BOTTOM LEFT - Layer Management
        col_bottom_left = pie.column()
        box_bottom_left = col_bottom_left.box()
        self.draw_layer_management(box_bottom_left, context)
        
        # BOTTOM RIGHT - Empty
        pie.column()
        
        # TOP LEFT - Empty
        pie.column()
        
        # TOP RIGHT - Empty
        pie.column()
    
    def draw_paint_options(self, layout, context):
        layout.label(text="Paint Options")
        
        # Tool options
        box = layout.box()
        box.label(text="Tool Options")
        
        tool_settings = context.tool_settings
        ipaint = tool_settings.image_paint
        
        # Drawing options
        row = box.row()
        row.label(text="Draw Mode:")
        row.prop(ipaint, "mode", text="")
        
        # Blending options
        if ipaint.mode == 'MATERIAL':
            box.prop(ipaint, "use_normal_falloff", text="Normal Falloff")
            if hasattr(ipaint, "seam_bleed"):
                box.prop(ipaint, "seam_bleed")
        
        # Fill options
        box = layout.box()
        box.label(text="Fill Options")
        
        if hasattr(ipaint, "fill_threshold"):
            row = box.row()
            row.prop(ipaint, "fill_threshold", text="Threshold")
    
    def draw_canvas_navigation(self, layout, context):
        layout.label(text="Canvas Navigation")
        
        # View controls
        box = layout.box()
        box.label(text="View")
        
        # Row 1 - Zoom
        row = box.row()
        row.operator("image.view_zoom_in", text="Zoom In")
        row.operator("image.view_zoom_out", text="Zoom Out")
        
        # Row 2 - Fit and reset view
        row = box.row()
        row.operator("image.view_all", text="View All")
        if hasattr(bpy.ops.image, "view_selected"):
            row.operator("image.view_selected", text="View Selected")
    
    def draw_layer_management(self, layout, context):
        layout.label(text="Layer Management")
        
        box = layout.box()
        box.label(text="Layer Tools")
        
        # Basic layer operations
        box.operator("image.pack", text="Pack Images")
        if hasattr(bpy.ops.image, "unpack"):
            box.operator("image.unpack", text="Unpack Images")