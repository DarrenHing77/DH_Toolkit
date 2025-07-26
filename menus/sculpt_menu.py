import bpy
from ..icons.icons import load_icons
from .modifers_multires_menu import draw_modifiers_multires_menu


def draw_sculpt_panels(layout, context):
    """Draw brush settings panels that actually exist in Blender 4.4"""
    brush = context.tool_settings.sculpt.brush
    col = layout.column(align=True)
    
    col.popover('VIEW3D_PT_tools_brush_settings_advanced', text="Advanced")
    col.popover('VIEW3D_PT_tools_brush_falloff', text="Falloff")
    col.popover('VIEW3D_PT_tools_brush_texture', text="Texture") 
    col.popover('VIEW3D_PT_tools_brush_stroke', text="Stroke")
    col.popover('VIEW3D_PT_sculpt_options', text="Sculpt Options")
    col.popover('VIEW3D_PT_sculpt_symmetry', text="Symmetry")


class DH_MT_Sculpt_Menu(bpy.types.Menu):
    """Context-specific pie menu for Sculpt Mode"""
    bl_idname = "DH_MT_Sculpt_Menu"
    bl_label = "DH Sculpt Toolkit"

    def draw(self, context):
        icons = load_icons()
        pie = self.layout.menu_pie()

        # LEFT - Brushes (grid) above Face Sets (not grid)
        col_left = pie.column()
        
        # Brushes - Grid layout, slightly bigger
        brush_box = col_left.box()
        brush_box.label(text='Brushes')
        brush_box.scale_y = 1.4  # Slightly bigger

        grid = brush_box.grid_flow(row_major=True, columns=3, even_columns=True)

        brushes = [
            ("Draw", "brushes\\essentials_brushes-mesh_sculpt.blend\\Brush\\Draw"),
            ("Draw Sharp", "brushes\\essentials_brushes-mesh_sculpt.blend\\Brush\\Draw Sharp"),
            ("Clay", "brushes\\essentials_brushes-mesh_sculpt.blend\\Brush\\Clay"),
            ("Clay Strips", "brushes\\essentials_brushes-mesh_sculpt.blend\\Brush\\Clay Strips"),
            ("Grab", "brushes\\essentials_brushes-mesh_sculpt.blend\\Brush\\Grab"),
            ("Smooth", "brushes\\essentials_brushes-mesh_sculpt.blend\\Brush\\Smooth"),
            ("Scrape", "brushes\\essentials_brushes-mesh_sculpt.blend\\Brush\\Scrape/Fill"),
            ("Pinch", "brushes\\essentials_brushes-mesh_sculpt.blend\\Brush\\Pinch"),
            ("Crease", "brushes\\essentials_brushes-mesh_sculpt.blend\\Brush\\Crease"),
            ("Mask", "brushes\\essentials_brushes-mesh_sculpt.blend\\Brush\\Mask"),
        ]
        
        for name, identifier in brushes:
            op = grid.operator("brush.asset_activate", text=name)
            op.asset_library_type = 'ESSENTIALS'
            op.asset_library_identifier = ""
            op.relative_asset_identifier = identifier

        # Face Sets - Not grid, regular column
        face_box = col_left.box()
        face_box.label(text='Face Sets')

        face_box.operator('sculpt.face_sets_create', text='From Masked').mode = 'MASKED'
        face_box.operator('sculpt.face_sets_create', text='From Visible').mode = 'VISIBLE'
        face_box.operator('sculpt.face_sets_create', text='From Edit Selection').mode = 'SELECTION'
        face_box.operator('sculpt.face_sets_init', text='Init Loose Parts').mode = 'LOOSE_PARTS'
        face_box.operator('sculpt.face_set_extract', text="Extract Face Set")

        # RIGHT - Brush Settings and Symmetry
        col_right = pie.column()

        # Brush Settings
        brush_box = col_right.box()
        brush_box.label(text="Brush Settings")
        draw_sculpt_panels(brush_box, context)

        # Symmetry
        sym_box = col_right.box()
        sym_box.label(text='Symmetry')

        row = sym_box.row(align=True)
        row.prop(context.object, "use_mesh_mirror_x", text="X", toggle=True)
        row.prop(context.object, "use_mesh_mirror_y", text="Y", toggle=True)
        row.prop(context.object, "use_mesh_mirror_z", text="Z", toggle=True)

        row = sym_box.row(align=True)
        row.operator("sculpt.symmetrize", text="+X to -X")
        row.operator("sculpt.symmetrize", text="-X to +X")

        # BOTTOM - Not grid, bigger buttons
        col_bottom = pie.column()

        # Mask Tools - Grid but wider/shorter buttons
        mask_box = col_bottom.box()
        mask_box.label(text="Mask Tools")
        mask_box.scale_y = 1.6  # Slightly bigger than brushes

        # 2 columns for wider buttons
        grid = mask_box.grid_flow(row_major=True, columns=2, even_columns=True)
        grid.operator("wm.tool_set_by_id", text="Box Mask").name = "builtin.box_mask"
        grid.operator("wm.tool_set_by_id", text="Lasso Mask").name = "builtin.lasso_mask"
        grid.operator("wm.tool_set_by_id", text="Polyline Mask").name = "builtin.polyline_mask"
        grid.operator("wm.tool_set_by_id", text="Line Mask").name = "builtin.line_mask"
        grid.operator('dh.advanced_mask_extract', text="Extract Mask")
        # Fill the last spot or leave empty
        grid.separator()

        # Trim Tools - Separate section, also grid
        trim_box = col_bottom.box()
        trim_box.label(text='Trim Tools')
        trim_box.scale_y = 1.6

        trim_grid = trim_box.grid_flow(row_major=True, columns=2, even_columns=True)
        trim_grid.operator("wm.tool_set_by_id", text="Box Trim").name = "builtin.box_trim"
        trim_grid.operator("wm.tool_set_by_id", text="Lasso Trim").name = "builtin.lasso_trim"
        trim_grid.operator("wm.tool_set_by_id", text="Polyline Trim").name = "builtin.polyline_trim"
        # Leave last spot empty or add another tool
        trim_grid.separator()

        # Transform Tools - Not grid, big buttons
        transform_box = col_bottom.box()
        transform_box.label(text='Transform')
        transform_box.scale_y = 2.0  # Bigger buttons

        transform_box.operator("wm.tool_set_by_id", text="Move").name = "builtin.move"
        transform_box.operator("wm.tool_set_by_id", text="Rotate").name = "builtin.rotate"
        transform_box.operator("wm.tool_set_by_id", text="Scale").name = "builtin.scale"

        row = transform_box.row()
        row.prop(context.scene.tool_settings, "transform_pivot_point", text="Pivot")

        # TOP - Modifiers/Multires
        col_top = pie.column()
        modifiers_box = col_top.box()
        draw_modifiers_multires_menu(modifiers_box, context)

        # Empty corners to avoid overlap
        pie.column()  # BOTTOM-LEFT
        pie.column()  # BOTTOM-RIGHT  
        pie.column()  # TOP-LEFT
        pie.column()  # TOP-RIGHT