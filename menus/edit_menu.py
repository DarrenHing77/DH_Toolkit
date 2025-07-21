import bpy
from ..icons.icons import load_icons

def draw_selection_tools(layout, context):
    layout.label(text='Selection')
    layout.operator("mesh.select_all", text="Select All").action = 'SELECT'
    layout.operator("mesh.select_all", text="Select None").action = 'DESELECT'
    layout.operator("mesh.select_all", text="Invert").action = 'INVERT'
    layout.operator("mesh.select_more", text="Grow Selection")
    layout.operator("mesh.select_less", text="Shrink Selection")

def draw_modeling_tools(layout, context):
    layout.label(text='Modeling')
    layout.operator("mesh.extrude_region_move", text="Extrude")
    layout.operator("mesh.inset", text="Inset Faces")
    layout.operator("mesh.bevel", text="Bevel")
    layout.operator("mesh.loopcut_slide", text="Loop Cut")
    layout.operator("mesh.knife_tool", text="Knife")

def draw_mesh_operations(layout, context):
    layout.label(text='Mesh Operations')
    layout.operator("mesh.merge", text="Merge")
    layout.operator("mesh.remove_doubles", text="Merge by Distance")
    layout.operator("mesh.split", text="Split")
    layout.operator("mesh.separate", text="Separate").type = 'SELECTED'
    layout.operator("mesh.normals_make_consistent", text="Recalculate Normals")

def draw_face_tools(layout, context):
    layout.label(text='Face Tools')
    layout.operator("mesh.fill", text="Fill")
    layout.operator("mesh.beautify_fill", text="Beautify Faces")
    layout.operator("mesh.quads_convert_to_tris", text="Triangulate")
    layout.operator("mesh.tris_convert_to_quads", text="Tris to Quads")

def draw_delete_tools(layout, context):
    layout.label(text='Delete')
    layout.operator("mesh.delete", text="Vertices").type = 'VERT'
    layout.operator("mesh.delete", text="Edges").type = 'EDGE'
    layout.operator("mesh.delete", text="Faces").type = 'FACE'
    layout.operator("mesh.delete_edgeloop", text="Edge Loop")
    layout.operator("mesh.dissolve_verts", text="Dissolve Vertices")

def draw_visibility_tools(layout, context):
    layout.label(text='Visibility')
    layout.operator("mesh.hide", text="Hide Selected").unselected = False
    layout.operator("mesh.hide", text="Hide Unselected").unselected = True
    layout.operator("mesh.reveal", text="Reveal All")
    layout.operator('dh.toggle_wireframe', text='Wireframe Override')

def draw_uv_tools(layout, context):
    layout.label(text='UV Tools')
    layout.operator("uv.unwrap", text="Unwrap")
    layout.operator("mesh.mark_seam", text="Mark Seam").clear = False
    layout.operator("mesh.mark_seam", text="Clear Seam").clear = True
    layout.operator("mesh.mark_sharp", text="Mark Sharp").clear = False
    layout.operator("mesh.mark_sharp", text="Clear Sharp").clear = True

class DH_MT_Edit_Menu(bpy.types.Menu):
    bl_idname = "DH_MT_Edit_Menu"
    bl_label = "DH Edit Toolkit"

    def draw(self, context):
        pie = self.layout.menu_pie()
        
        # LEFT - Selection and Delete Tools in same column, different rows
        col_left = pie.column()
        
        # First the Selection Tools
        box1 = col_left.box()
        draw_selection_tools(box1, context)
        
        # Then a bit of space
        col_left.separator()
        
        # Then the Delete Tools
        box2 = col_left.box()
        draw_delete_tools(box2, context)
        
        # RIGHT - Split into two columns for Modeling and Face Tools (unchanged)
        col_right = pie.column()
        row = col_right.row(align=True)
        
        # First column for Modeling
        col1 = row.column()
        box1 = col1.box()
        draw_modeling_tools(box1, context)
        
        # Second column for Face Tools
        col2 = row.column()
        box2 = col2.box()
        draw_face_tools(box2, context)
        
        # BOTTOM - Visibility Tools (replacing Transform tools)
        col_bottom = pie.column()
        box = col_bottom.box()
        draw_visibility_tools(box, context)
        
        # TOP - Mesh Operations and UV Tools in same column, different rows
        col_top = pie.column()
        
        # First the Mesh Operations
        box1 = col_top.box()
        draw_mesh_operations(box1, context)
        
        # Then a bit of space
        col_top.separator()
        
        # Then the UV Tools
        box2 = col_top.box()
        draw_uv_tools(box2, context)
        
        # Leave the corners empty to avoid overlaps
        # BOTTOM-LEFT
        col_bl = pie.column()
        # Intentionally empty
        
        # BOTTOM-RIGHT
        col_br = pie.column()
        # Intentionally empty
        
        # TOP-LEFT
        col_tl = pie.column()
        # Intentionally empty
        
        # TOP-RIGHT
        col_tr = pie.column()
        # Intentionally empty