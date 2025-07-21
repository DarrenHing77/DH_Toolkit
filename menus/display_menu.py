import bpy
import os
from ..icons.icons import load_icons
import inspect


def draw_display(layout, context):
    ob = context.active_object
    layout.label(text='Display')
    
    layout.operator_context = 'INVOKE_DEFAULT'
    #icons = load_icons()
    
    #icon = icons.get("icon_primitives")
    layout.operator('dh.toggle_wireframe', text='Wireframe Override')
    layout.operator('dh.toggle_visibility_outliner', text='Unhide Outliner Selection')
    layout.operator('dh.switch_to_shader_editor', text='Shader Editor')
    
    layout.separator()
    
    # Viewport Background Controls
    if context.space_data and hasattr(context.space_data, 'shading'):
        shading = context.space_data.shading
        scene = context.scene
        
        layout.label(text="Viewport Background")
        
        # Background type selector
        row = layout.row(align=True)
        row.prop(shading, "background_type", expand=True)
        
        # Background-specific controls
        if shading.background_type == 'VIEWPORT':
            layout.prop(shading, "background_color", text="Background Color")
            layout.prop(shading, "background_opacity", text="Opacity")
            
        elif shading.background_type == 'WORLD':
            if scene.world:
                # Check for world shader nodes
                if hasattr(scene.world, 'node_tree') and scene.world.node_tree:
                    bg_shader = None
                    for node in scene.world.node_tree.nodes:
                        if node.type == 'BACKGROUND':
                            bg_shader = node
                            break
                    
                    if bg_shader:
                        # Background color (if not connected)
                        if not bg_shader.inputs['Color'].links:
                            layout.prop(bg_shader.inputs['Color'], 'default_value', text="Background Color")
                        
                        # Background strength (if not connected)
                        if not bg_shader.inputs['Strength'].links:
                            layout.prop(bg_shader.inputs['Strength'], 'default_value', text="Background Strength")
                else:
                    # Fallback for worlds without node trees
                    if hasattr(scene.world, 'color'):
                        layout.prop(scene.world, "color", text="World Color")
            else:
                layout.operator("world.new", text="Add World", icon='ADD')
                
        elif shading.background_type == 'THEME':
            layout.prop(shading, "background_opacity", text="Opacity")
        
        layout.separator()