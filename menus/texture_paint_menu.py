import bpy
from ..icons.icons import load_icons

class DH_MT_Texture_Paint_Menu(bpy.types.Menu):
    bl_idname = "DH_MT_Texture_Paint_Menu"
    bl_label = "DH Texture Paint Toolkit"

    def draw(self, context):
        pie = self.layout.menu_pie()
        
        # Left column - Brushes
        col_left = pie.column()
        box_left = col_left.box()
        self.draw_paint_brushes(box_left, context)
        
        # Right column - Brush Settings
        col_right = pie.column()
        box_right = col_right.box()
        self.draw_brush_settings(box_right, context)
        
        # Bottom column - Paint Options
        col_bottom = pie.column()
        box_bottom = col_bottom.box()
        self.draw_paint_options(box_bottom, context)
        
        # Top column - Canvas Navigation
        col_top = pie.column()
        box_top = col_top.box()
        self.draw_canvas_navigation(box_top, context)
        
        # Bottom left - Color and Palette
        col_bottom_left = pie.column()
        box_bottom_left = col_bottom_left.box()
        self.draw_color_palette(box_bottom_left, context)
        
        # Bottom right - Layer Management
        col_bottom_right = pie.column()
        box_bottom_right = col_bottom_right.box()
        self.draw_layer_management(box_bottom_right, context)
        
        # Top left - Image Management
        col_top_left = pie.column()
        box_top_left = col_top_left.box()
        self.draw_image_management(box_top_left, context)
        
        # Top right - Display Options (reused partly from main menu)
        col_top_right = pie.column()
        box_top_right = col_top_right.box()
        self.draw_display_options(box_top_right, context)
    
    def draw_paint_brushes(self, layout, context):
        layout.label(text="Paint Brushes")
        
        # Common texture painting brushes
        box = layout.box()
        box.label(text="Common Brushes")
        
        # Row 1 - Basic brushes
        row = box.row()
        row.operator("paint.brush_select", text="Draw").texture_paint_tool = 'DRAW'
        row.operator("paint.brush_select", text="Soften").texture_paint_tool = 'SOFTEN'
        
        # Row 2 - More brushes
        row = box.row()
        row.operator("paint.brush_select", text="Smear").texture_paint_tool = 'SMEAR'
        row.operator("paint.brush_select", text="Clone").texture_paint_tool = 'CLONE'
        
        # Row 3 - Even more brushes
        row = box.row()
        row.operator("paint.brush_select", text="Fill").texture_paint_tool = 'FILL'
        row.operator("paint.brush_select", text="Mask").texture_paint_tool = 'MASK'
        
        # Brush creation
        layout.separator()
        layout.operator("brush.add", text="Add Brush")
        layout.operator("brush.reset", text="Reset Brush")
    
    def draw_brush_settings(self, layout, context):
        layout.label(text="Brush Settings")
        
        if context.tool_settings.image_paint:
            brush = context.tool_settings.image_paint.brush
            if brush:
                # Brush properties section
                box = layout.box()
                box.label(text="Brush Properties")
                
                # Row 1 - Size and Strength
                row = box.row()
                row.prop(brush, "size", text="Size")
                row.prop(brush, "strength", text="Strength")
                
                # Row 2 - Blend and Flow
                row = box.row()
                row.prop(brush, "blend", text="Blend")
                if hasattr(brush, "flow"):  # Check for Blender 4.x compatibility
                    row.prop(brush, "flow", text="Flow")
                
                # Additional properties
                box.prop(brush, "use_pressure_size", text="Size Pressure")
                box.prop(brush, "use_pressure_strength", text="Strength Pressure")
                
                # Texture section if applicable
                if brush.texture:
                    box = layout.box()
                    box.label(text="Texture")
                    box.template_ID(brush, "texture", new="texture.new")
                    box.prop(brush, "texture_angle", text="Angle")
    
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
            box.prop(ipaint, "seam_bleed")
        
        # Fill options
        box = layout.box()
        box.label(text="Fill Options")
        
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
        row.operator("image.view_selected", text="View Selected")
        
        # Row 3 - Pan
        box.operator("image.view_pan", text="View Pan")
        
        # Toggle features
        box = layout.box()
        box.label(text="Toggle")
        
        row = box.row()
        row.operator("image.view_center_cursor", text="Center View to Cursor")
        
        # Add UV reference display
        if context.scene.tool_settings.use_uv_select_sync:
            row = box.row()
            row.operator("image.uv_sync_toggle", text="Disable UV Sync")
        else:
            row = box.row()
            row.operator("image.uv_sync_toggle", text="Enable UV Sync")
    
    def draw_color_palette(self, layout, context):
        layout.label(text="Color & Palette")
        
        # Color picker section
        tool_settings = context.tool_settings
        ipaint = tool_settings.image_paint
        
        box = layout.box()
        box.label(text="Color Picker")
        
        # Color UI
        box.template_color_picker(ipaint, "color", value_slider=True)
        
        # RGB/HSV swatches
        row = box.row()
        row.prop(ipaint, "color", text="")
        
        # Palette management
        box = layout.box()
        box.label(text="Palette")
        
        row = box.row()
        row.template_ID(ipaint, "palette", new="palette.new")
        if ipaint.palette:
            box.template_palette(ipaint, "palette", color=True)
    
    def draw_layer_management(self, layout, context):
        layout.label(text="Layer Management")
        
        # Get the active image
        image = None
        if context.space_data and context.space_data.type == 'IMAGE_EDITOR':
            image = context.space_data.image
        elif context.tool_settings.image_paint.canvas:
            image = context.tool_settings.image_paint.canvas
        
        # Image layers section
        box = layout.box()
        box.label(text="Paint Slots")
        
        if image:
            box.template_image_layers(image)
        else:
            box.label(text="No active image")
        
        # Layer blend options
        if image and image.use_paint_mask:
            box = layout.box()
            box.label(text="Masking")
            
            row = box.row()
            row.prop(image, "use_paint_mask", text="Paint Mask")
            row.prop(image, "use_paint_mask_layer", text="Layer Mask")
    
    def draw_image_management(self, layout, context):
        layout.label(text="Image Management")
        
        # Image options
        box = layout.box()
        box.label(text="Image")
        
        tool_settings = context.tool_settings
        ipaint = tool_settings.image_paint
        
        # Canvas selection
        row = box.row()
        row.template_ID(ipaint, "canvas", new="image.new", open="image.open")
        
        # Image operations
        if ipaint.canvas:
            box.operator("image.save", text="Save Image")
            box.operator("image.save_as", text="Save As...")
            
            # UV Map selection if relevant
            mesh = context.active_object.data
            if hasattr(mesh, "uv_layers") and mesh.uv_layers:
                box = layout.box()
                box.label(text="UV Map")
                
                row = box.row()
                row.template_ID(ipaint, "uv_layer", new="mesh.uv_layers.new")