import bpy
from ..icons.icons import load_icons

class DH_MT_UV_Edit_Menu(bpy.types.Menu):
    bl_idname = "DH_MT_UV_Edit_Menu"
    bl_label = "DH UV Edit Toolkit"

    def draw(self, context):
        pie = self.layout.menu_pie()
        
        # Left column - Selection Tools
        col_left = pie.column()
        box_left = col_left.box()
        self.draw_selection_tools(box_left, context)
        
        # Right column - Transform Tools
        col_right = pie.column()
        box_right = col_right.box()
        self.draw_transform_tools(box_right, context)
        
        # Bottom column - Unwrap Tools
        col_bottom = pie.column()
        box_bottom = col_bottom.box()
        self.draw_unwrap_tools(box_bottom, context)
        
        # Top column - Display Options
        col_top = pie.column()
        box_top = col_top.box()
        self.draw_display_options(box_top, context)
        
        # Bottom left - Align and Pack
        col_bottom_left = pie.column()
        box_bottom_left = col_bottom_left.box()
        self.draw_align_pack_tools(box_bottom_left, context)
        
        # Bottom right - Utility Tools
        col_bottom_right = pie.column()
        box_bottom_right = col_bottom_right.box()
        self.draw_utility_tools(box_bottom_right, context)
        
        # Top left - UV Maps
        col_top_left = pie.column()
        box_top_left = col_top_left.box()
        self.draw_uv_maps(box_top_left, context)
        
        # Top right - Export/Import
        col_top_right = pie.column()
        box_top_right = col_top_right.box()
        self.draw_export_import(box_top_right, context)
    
    def draw_selection_tools(self, layout, context):
        layout.label(text="Selection Tools")
        
        # Row for selection modes
        box = layout.box()
        box.label(text="Select")
        
        row = box.row(align=True)
        row.operator("uv.select_all", text="All").action = 'SELECT'
        row.operator("uv.select_all", text="None").action = 'DESELECT'
        row.operator("uv.select_all", text="Invert").action = 'INVERT'
        
        # Common selection operations
        box.operator("uv.select_linked", text="Linked")
        box.operator("uv.select_split", text="Split")
        
        # Row for grow/shrink
        row = box.row(align=True)
        row.operator("uv.select_more", text="More")
        row.operator("uv.select_less", text="Less")
        
        # Select loops
        layout.separator()
        box = layout.box()
        box.label(text="Loops")
        
        row = box.row(align=True)
        row.operator("uv.select_loop", text="Loop").extend = False
        row.operator("uv.select_loop", text="+Loop").extend = True
        
        box.operator("uv.select_edge_ring", text="Edge Ring")
    
    def draw_transform_tools(self, layout, context):
        layout.label(text="Transform")
        
        # Basic transforms
        box = layout.box()
        box.label(text="Basic")
        
        row = box.row(align=True)
        row.operator("transform.translate", text="Move")
        row.operator("transform.rotate", text="Rotate")
        row.operator("transform.resize", text="Scale")
        
        # Special transforms
        box = layout.box()
        box.label(text="Special")
        
        row = box.row(align=True)
        row.operator("transform.mirror", text="Mirror")
        row.operator("uv.weld", text="Weld")
        
        box.operator("uv.pin", text="Pin").clear = False
        box.operator("uv.pin", text="Unpin").clear = True
        
        # Snap options
        box = layout.box()
        box.label(text="Snap")
        
        row = box.row(align=True)
        row.operator("uv.snap_selected", text="Pixels").target = 'PIXELS'
        row.operator("uv.snap_selected", text="Cursor").target = 'CURSOR'
        
        row = box.row(align=True)
        row.operator("uv.snap_cursor", text="Cursor to Selection").target = 'SELECTED'
        row.operator("uv.snap_cursor", text="Cursor to Origin").target = 'ORIGIN'
    
    def draw_unwrap_tools(self, layout, context):
        layout.label(text="Unwrap Tools")
        
        # Basic unwrap methods
        box = layout.box()
        box.label(text="Basic Methods")
        
        row = box.row(align=True)
        row.operator("uv.unwrap", text="Unwrap")
        row.operator("uv.smart_project", text="Smart UV Project")
        
        row = box.row(align=True)
        row.operator("uv.lightmap_pack", text="Lightmap Pack")
        row.operator("uv.follow_active_quads", text="Follow Active Quads")
        
        # Specialized methods
        box = layout.box()
        box.label(text="Specialized")
        
        row = box.row(align=True)
        row.operator("uv.cube_project", text="Cube Projection")
        row.operator("uv.cylinder_project", text="Cylinder Projection")
        
        row = box.row(align=True)
        row.operator("uv.sphere_project", text="Sphere Projection")
        row.operator("uv.project_from_view", text="Project from View")
    
    def draw_display_options(self, layout, context):
        layout.label(text="Display Options")
        
        # UV display settings
        box = layout.box()
        box.label(text="Display")
        
        # Get overlay properties
        overlay = context.space_data.overlay
        
        # Row for edge and face display
        row = box.row()
        row.prop(overlay, "show_edges", text="Edges")
        row.prop(overlay, "show_faces", text="Faces")
        
        # Row for display modes
        if hasattr(overlay, "display_stretch_type"):
            row = box.row()
            row.label(text="Stretch:")
            row.prop(overlay, "display_stretch_type", text="")
            
            # Stretch angle/area based on selected type
            if overlay.display_stretch_type in {'ANGLE', 'AREA'}:
                row = box.row()
                row.prop(overlay, "show_stretch", text="Show Stretch")
        
        # Background image settings
        box = layout.box()
        box.label(text="Background")
        
        if context.space_data.image:
            row = box.row()
            row.prop(context.space_data, "use_image_pin", text="Pin Image")
    
    def draw_align_pack_tools(self, layout, context):
        layout.label(text="Align & Pack")
        
        # Align tools
        box = layout.box()
        box.label(text="Align")
        
        row = box.row(align=True)
        row.operator("uv.align", text="X").axis = 'ALIGN_X'
        row.operator("uv.align", text="Y").axis = 'ALIGN_Y'
        
        row = box.row(align=True)
        row.operator("uv.align_rotation", text="Straighten")
        row.operator("uv.align_rotation", text="Straighten X-axis").axis = 'ALIGN_TO_AXIS_X'
        
        # Pack tools
        box = layout.box()
        box.label(text="Pack")
        
        row = box.row(align=True)
        row.operator("uv.pack_islands", text="Pack Islands")
        row.operator("uv.average_islands_scale", text="Average Scale")
        
        box.operator("uv.minimize_stretch", text="Minimize Stretch")
    
    def draw_utility_tools(self, layout, context):
        layout.label(text="Utilities")
        
        # Seams and sharp edges
        box = layout.box()
        box.label(text="Mark")
        
        row = box.row(align=True)
        row.operator("uv.mark_seam", text="Mark Seam").clear = False
        row.operator("uv.mark_seam", text="Clear Seam").clear = True
        
        # UV manipulation
        box = layout.box()
        box.label(text="Manipulation")
        
        row = box.row(align=True)
        row.operator("uv.stitch", text="Stitch")
        row.operator("uv.seams_from_islands", text="Seams from Islands")
        
        row = box.row(align=True)
        row.operator("uv.rip", text="Rip")
        row.operator("uv.rip_move", text="Rip & Move")
        
        # Advanced utilities
        box = layout.box()
        box.label(text="Advanced")
        
        row = box.row(align=True)
        row.operator("uv.reset", text="Reset")
        row.operator("uv.remove_doubles", text="Remove Doubles")