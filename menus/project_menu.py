import bpy
import os
from ..icons.icons import load_icons
import inspect





def draw_project(layout, context):
    ob = context.active_object
    layout.label(text='Project')
    
    
    layout.operator_context = 'INVOKE_DEFAULT'
    icons = load_icons()
    
    
    
    
    
    layout.operator("dh.dcc_importer", text="DCC Import")
    layout.operator("dh.dcc_exporter", text="DCC Export")
    layout.operator("dh.dcc_split_exporter", text="Multi FBX Export") # new operator 



    

