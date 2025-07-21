import bpy
from ..icons.icons import load_icons

class DH_MT_Shader_Editor_Menu(bpy.types.Menu):
    bl_idname = "DH_MT_Shader_Editor_Menu"
    bl_label = "DH Shader Editor Toolkit"

    def draw(self, context):
        pie = self.layout.menu_pie()
        
        # LEFT - Math, Texture, and Input Nodes (3 boxes stacked)
        col_left = pie.column()
        
        # Math Nodes (top)
        box_left_math = col_left.box()
        self.draw_math_utility_nodes(box_left_math, context)
        
        col_left.separator()
        
        # Texture Nodes (middle)
        box_left_texture = col_left.box()
        self.draw_texture_nodes(box_left_texture, context)
        
        col_left.separator()
        
        # Input Nodes (bottom)
        box_left_input = col_left.box()
        self.draw_input_nodes(box_left_input, context)
        
        # RIGHT - Output and Utility (same as before)
        col_right = pie.column()
        
        # Output Nodes (top)
        box_right_top = col_right.box()
        self.draw_output_nodes(box_right_top, context)
        
        col_right.separator()
        
        # Utility Operations (bottom)
        box_right_bottom = col_right.box()
        self.draw_utility_operations(box_right_bottom, context)
        
        # BOTTOM - Color & Mixing Nodes
        col_bottom = pie.column()
        box_bottom = col_bottom.box()
        self.draw_color_mixing_nodes(box_bottom, context)
        
        # TOP - Converter and Vector Nodes (2 boxes stacked)
        col_top = pie.column()
        
        # Converter Nodes (top)
        box_top_converter = col_top.box()
        self.draw_converter_nodes(box_top_converter, context)
        
        col_top.separator()
        
        # Vector Nodes (bottom)
        box_top_vector = col_top.box()
        self.draw_vector_nodes(box_top_vector, context)
        
        # Empty corners to avoid overlaps
        pie.column()  # BOTTOM-LEFT
        pie.column()  # BOTTOM-RIGHT  
        pie.column()  # TOP-LEFT
        pie.column()  # TOP-RIGHT
    
    def draw_texture_nodes(self, layout, context):
        layout.label(text="Texture Nodes")
        
        # Use grid to keep it compact
        grid = layout.grid_flow(row_major=True, columns=2, even_columns=True)
        grid.operator("node.add_node", text="Image Texture").type = "ShaderNodeTexImage"
        grid.operator("node.add_node", text="Noise Texture").type = "ShaderNodeTexNoise"
        grid.operator("node.add_node", text="Voronoi").type = "ShaderNodeTexVoronoi"
        grid.operator("node.add_node", text="Wave").type = "ShaderNodeTexWave"
        grid.operator("node.add_node", text="Musgrave").type = "ShaderNodeTexMusgrave"
        grid.operator("node.add_node", text="Gradient").type = "ShaderNodeTexGradient"
    
    def draw_math_utility_nodes(self, layout, context):
        layout.label(text="Math & Utility")
        
        # Essential math and utility nodes
        layout.operator("node.add_node", text="Math").type = "ShaderNodeMath"
        layout.operator("node.add_node", text="Vector Math").type = "ShaderNodeVectorMath"
        layout.operator("node.add_node", text="Map Range").type = "ShaderNodeMapRange"
        layout.operator("node.add_node", text="Clamp").type = "ShaderNodeClamp"
        layout.operator("node.add_node", text="Value").type = "ShaderNodeValue"
        layout.operator("node.add_node", text="Frame").type = "NodeFrame"
        layout.operator("node.add_node", text="Reroute").type = "NodeReroute"
    
    def draw_color_mixing_nodes(self, layout, context):
        layout.label(text="Color & Mixing")
        
        # Color and mixing nodes
        layout.operator("node.add_node", text="Mix RGB").type = "ShaderNodeMixRGB"
        layout.operator("node.add_node", text="ColorRamp").type = "ShaderNodeValToRGB"
        layout.operator("node.add_node", text="RGB").type = "ShaderNodeRGB"
        layout.operator("node.add_node", text="Hue/Saturation").type = "ShaderNodeHueSaturation"
        layout.operator("node.add_node", text="Gamma").type = "ShaderNodeGamma"
        layout.operator("node.add_node", text="Bright/Contrast").type = "ShaderNodeBrightContrast"
        layout.operator("node.add_node", text="Invert").type = "ShaderNodeInvert"
    
    def draw_converter_nodes(self, layout, context):
        layout.label(text="Converter Nodes")
        
        # Converter nodes
        layout.operator("node.add_node", text="Separate RGB").type = "ShaderNodeSeparateRGB"
        layout.operator("node.add_node", text="Combine RGB").type = "ShaderNodeCombineRGB"
        layout.operator("node.add_node", text="Separate XYZ").type = "ShaderNodeSeparateXYZ"
        layout.operator("node.add_node", text="Combine XYZ").type = "ShaderNodeCombineXYZ"
        layout.operator("node.add_node", text="Separate HSV").type = "ShaderNodeSeparateHSV"
        layout.operator("node.add_node", text="Combine HSV").type = "ShaderNodeCombineHSV"
        layout.operator("node.add_node", text="RGB to BW").type = "ShaderNodeRGBToBW"
    
    def draw_input_nodes(self, layout, context):
        layout.label(text="Input Nodes")
        
        # Use grid to keep it compact
        grid = layout.grid_flow(row_major=True, columns=2, even_columns=True)
        grid.operator("node.add_node", text="Tex Coord").type = "ShaderNodeTexCoord"
        grid.operator("node.add_node", text="UV Map").type = "ShaderNodeUVMap"
        grid.operator("node.add_node", text="Mapping").type = "ShaderNodeMapping"
        grid.operator("node.add_node", text="Geometry").type = "ShaderNodeNewGeometry"
        grid.operator("node.add_node", text="Object Info").type = "ShaderNodeObjectInfo"
        grid.operator("node.add_node", text="Fresnel").type = "ShaderNodeFresnel"
    
    def draw_output_nodes(self, layout, context):
        layout.label(text="Output & Shaders")
        
        # Use grid to keep it compact
        grid = layout.grid_flow(row_major=True, columns=2, even_columns=True)
        grid.operator("node.add_node", text="Material Output").type = "ShaderNodeOutputMaterial"
        grid.operator("node.add_node", text="Principled BSDF").type = "ShaderNodeBsdfPrincipled"
        grid.operator("node.add_node", text="Emission").type = "ShaderNodeEmission"
        grid.operator("node.add_node", text="Transparent").type = "ShaderNodeBsdfTransparent"
        grid.operator("node.add_node", text="Mix Shader").type = "ShaderNodeMixShader"
        grid.operator("node.add_node", text="Add Shader").type = "ShaderNodeAddShader"
    
    def draw_vector_nodes(self, layout, context):
        layout.label(text="Vector Nodes")
        
        # Vector nodes
        layout.operator("node.add_node", text="Normal Map").type = "ShaderNodeNormalMap"
        layout.operator("node.add_node", text="Bump").type = "ShaderNodeBump"
        layout.operator("node.add_node", text="Displacement").type = "ShaderNodeDisplacement"
        layout.operator("node.add_node", text="Vector Transform").type = "ShaderNodeVectorTransform"
        layout.operator("node.add_node", text="Normal").type = "ShaderNodeNormal"
        layout.operator("node.add_node", text="Vector Curves").type = "ShaderNodeVectorCurve"
    
    def draw_utility_operations(self, layout, context):
        layout.label(text="Node Operations")
        
        # Use grid to keep it compact
        grid = layout.grid_flow(row_major=True, columns=2, even_columns=True)
        grid.operator("node.duplicate_move", text="Duplicate")
        grid.operator("node.delete", text="Delete")
        grid.operator("node.group_make", text="Group")
        grid.operator("node.group_ungroup", text="Ungroup")
        grid.operator("node.links_cut", text="Cut Links")
        grid.operator("node.select_all", text="Select All").action = 'SELECT'