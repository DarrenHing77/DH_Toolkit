import bpy
from ..icons.icons import load_icons

class DH_MT_Weight_Paint_Menu(bpy.types.Menu):
    bl_idname = "DH_MT_Weight_Paint_Menu"
    bl_label = "DH Weight Paint Toolkit"

    def draw(self, context):
        pie = self.layout.menu_pie()

        # LEFT - Weight Brushes
        col_left = pie.column()
        box_left = col_left.box()
        box_left2 = col_left.box()
        self.draw_weight_brushes(box_left2, context)
        self.draw_weight_transfer(box_left, context)

        # RIGHT - Brush Settings
        col_right = pie.column()
        box_right = col_right.box()
        self.draw_brush_settings(box_right, context)

        # BOTTOM - Weight Tools
        col_bottom = pie.column()
        box_bottom = col_bottom.box()
        self.draw_weight_tools(box_bottom, context)

        # TOP - Vertex Groups
       # col_top = pie.column()
       # box_top = col_top.box()
       # self.draw_vertex_groups(box_top, context)

        # BOTTOM-LEFT - Weight Gradients
        #col_bottom_left = pie.column()
        #box_bottom_left = col_bottom_left.box()
        

        # BOTTOM-RIGHT - Weight Transfer
        col_bottom_right = pie.column()
        box_bottom_right = col_bottom_right.box()
        

        # TOP-LEFT - Empty
        pie.column()

        # TOP-RIGHT - Empty
        pie.column()
    
    def draw_weight_brushes(self, layout, context):
        layout.label(text="Weight Brushes")
        
        box = layout.box()
        column = box.column()
        
        column.operator("wm.tool_set_by_id", text="Brush").name = "builtin.brush"
        column.operator("wm.tool_set_by_id", text="Blur").name = "builtin_brush.blur"
        column.operator("wm.tool_set_by_id", text="Average").name = "builtin_brush.average"
        column.operator("wm.tool_set_by_id", text="Smear").name = "builtin_brush.smear"
        column.operator("wm.tool_set_by_id", text="Gradient").name = "builtin.gradient"

    def draw_brush_settings(self, layout, context):
        layout.label(text="Brush Settings")
        
        wpaint = context.tool_settings.weight_paint
        if not wpaint or not wpaint.brush:
            layout.label(text="No brush selected")
            return
            
        brush = wpaint.brush
        box = layout.box()
        box.label(text="Brush Properties")
        
        # Size and Weight
        row = box.row()
        row.prop(context.scene.tool_settings.unified_paint_settings, "size", text="Size")
        row.prop(context.scene.tool_settings.unified_paint_settings, "weight", text="Weight")
        
        # Pressure settings
        box.prop(brush, "use_pressure_size", text="Size Pressure")
        box.prop(brush, "use_pressure_strength", text="Strength Pressure")
        
        # Falloff curve
        if hasattr(brush, "curve"):
            box.label(text="Falloff Curve:")
            box.template_curve_mapping(brush, "curve")
    
    def draw_weight_tools(self, layout, context):
        layout.label(text="Weight Tools")
        
        box = layout.box()
        column = box.column()
        
        column.operator("paint.weight_set", text="Set Weight")
        column.operator("object.vertex_group_smooth", text="Smooth Weight")
        column.operator("dh.cycle_vertex_groups", text="Cycle Vertex Groups")
        column.operator("dh.weight_fill_modal", text="Fill Shell")

        op = column.operator("object.symmetrize_vertex_weights", text="Symmetrize R→L")
        op.groups = 'ALL'
        op.direction = 'RIGHT_TO_LEFT'
        op2 = column.operator("object.symmetrize_vertex_weights", text="Symmetrize L→R")
        op2.group = 'ALL'
        op2.direction = 'LEFT_TO_RIGHT'
        op3 = column.operator("object.symmetrize_vertex_weights", text="Symmetrize Active")
        op3.groups = 'ACTIVE'
        

    
    def draw_vertex_groups(self, layout, context):
        layout.label(text="Vertex Groups")
        
        obj = context.active_object
        if not obj or not obj.vertex_groups:
            layout.label(text="No vertex groups")
            layout.operator("object.vertex_group_add", text="Add Vertex Group")
            return
        
        # Group management
        box = layout.box()
        box.label(text="Group Management")
        
        row = box.row()
        row.operator("object.vertex_group_add", text="Add")
        row.operator("object.vertex_group_remove", text="Remove")
        
        row = box.row()
        row.operator("object.vertex_group_assign", text="Assign")
        row.operator("object.vertex_group_remove_from", text="Remove")
        
        row = box.row()
        row.operator("object.vertex_group_select", text="Select")
        row.operator("object.vertex_group_deselect", text="Deselect")
        
        # Active group
        box = layout.box()
        box.label(text="Active Group")
        if obj.vertex_groups.active:
            box.template_ID(obj, "vertex_groups", new="object.vertex_group_add")
    

    
    def draw_weight_transfer(self, layout, context):
        layout.label(text="Weight Transfer")
        
        box = layout.box()
        box.label(text="Transfer Options")
        box.operator("object.data_transfer", text="Transfer Weights")
        
        box = layout.box()
        box.label(text="Copy Between Objects")
        
        row = box.row()
        row.operator("object.vertex_group_copy", text="Copy Groups")
        row.operator("object.vertex_group_copy_to_linked", text="Copy to Linked")
        
        box = layout.box()
        box.label(text="Mirror")
        box.operator("object.vertex_group_mirror", text="Mirror Vertex Groups")