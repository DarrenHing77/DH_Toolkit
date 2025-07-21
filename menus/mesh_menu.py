import bpy
import os
from ..icons.icons import load_icons
import inspect





def draw_mesh(layout, context):
    ob = context.active_object
    layout.label(text='Mesh')
    
    
    layout.operator_context = 'INVOKE_DEFAULT'
    icons = load_icons()
    
    #layout.operator("dh.decimate", text = "decimate")
    icon = icons.get("icon_switcharrow")
    layout.operator('object.join', text='Join',icon_value=icon.icon_id)
    
    icon = icons.get("icon_separate")
    layout.operator('mesh.separate',icon_value=icon.icon_id ).type="LOOSE"
    
    layout.separator()
    icon = icons.get("icon_undo")
    layout.operator('dh_op.reset_transforms', text="Reset Transforms")
    #layout.operator('dh.fix_rotation', text="Fix Rotation")

    
    
    
   


def draw_mask(layout, context):
    ob = context.active_object
    layout.label(text='Mask Tools')
    layout.operator('dh.mask_extract')
    layout.operator('mesh.paint_mask_slice')
    layout.operator('dh.decimate')
    
    

