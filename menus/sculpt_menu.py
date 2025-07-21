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

        # LEFT - Face Sets and Brushes
        col_left = pie.column()
        col_left.scale_y = 1.3

        # Face Sets Tools
        face_box = col_left.box()
        face_box.label(text='Face Sets')

        row = face_box.row(align=True)
        row.operator('sculpt.face_sets_create', text='From Masked').mode = 'MASKED'
        row.operator('sculpt.face_sets_create', text='From Visible').mode = 'VISIBLE'

        row = face_box.row(align=True)
        row.operator('sculpt.face_sets_create', text='From Edit Selection').mode = 'SELECTION'
        row.operator('sculpt.face_sets_init', text='Init Loose Parts').mode = 'LOOSE_PARTS'

        row = face_box.row()
        row.operator('mesh.face_set_extract', text="Extract Face Set")

        # Brushes
        brush_box = col_left.box()
        brush_box.label(text='Brushes')

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

        # RIGHT - Brush Settings and Symmetry
        col_right = pie.column()
        col_right.scale_y = 1.3

        # Use existing brush panel function
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

        # BOTTOM - Masking and Transform Tools
        col_bottom = pie.column()
        col_bottom.scale_y = 1.3

        # Mask Tools
        mask_box = col_bottom.box()
        mask_box.label(text="Mask Tools")

        row = mask_box.row(align=True)
        row.operator("wm.tool_set_by_id", text="Box Mask").name = "builtin.box_mask"
        row.operator("wm.tool_set_by_id", text="Lasso Mask").name = "builtin.lasso_mask"

        row = mask_box.row(align=True)
        row.operator('dh.mask_extract', text="Extract Mask")
        row.operator('mesh.paint_mask_slice', text="Mask Slice")

        row = mask_box.row(align=True)
        op = row.operator("paint.mask_flood_fill", text="Fill")
        op.mode = 'VALUE'
        op.value = 1.0
        op = row.operator("paint.mask_flood_fill", text="Clear")
        op.mode = 'VALUE'
        op.value = 0.0

        # Transform Tools
        transform_box = col_bottom.box()
        transform_box.label(text='Transform')

        row = transform_box.row(align=True)
        row.operator("wm.tool_set_by_id", text="Move").name = "builtin.move"
        row.operator("wm.tool_set_by_id", text="Rotate").name = "builtin.rotate"
        row.operator("wm.tool_set_by_id", text="Scale").name = "builtin.scale"

        row = transform_box.row(align=True)
        row.prop(context.scene.tool_settings, "transform_pivot_point", text="Pivot")

        # TOP - Use your existing modifiers/multires function
        col_top = pie.column()
        col_top.scale_y = 1.3

        # Dyntopo
        dyntopo_box = col_top.box()
        dyntopo_box.label(text='Dynamic Topology')

        if context.sculpt_object:
            dyntopo_enabled = context.sculpt_object.use_dynamic_topology_sculpting
            dyntopo_box.operator("sculpt.dynamic_topology_toggle",
                                 text="Disable Dyntopo" if dyntopo_enabled else "Enable Dyntopo")

            if dyntopo_enabled and hasattr(context.tool_settings.sculpt, "detail_type_method"):
                dyntopo_box.prop(context.tool_settings.sculpt, "detail_type_method", text="")
                dyntopo_box.operator("sculpt.detail_flood_fill", text="Detail Flood Fill")

        # Use your existing modifiers/multires menu function
        modifiers_box = col_top.box()
        draw_modifiers_multires_menu(modifiers_box, context)