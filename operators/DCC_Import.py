import bpy

class DH_OP_dcc_import(bpy.types.Operator):
    
    ## imports objects from temp folder from other DCC's
    
    bl_idname = "dh.dcc_importer"
    bl_label = "DCC_Import"
    bl_options = {'REGISTER', 'UNDO'}
    
   
    
    
    
    def draw(self,context):
        
        layout =  self.layout
       # layout.operator_context = 'INVOKE DEFAULT'
        layout.label(text ="DCC Importer")
        
        layout.operator(DH_OP_dcc_import.bl_idname, text="Dialog Operator")
       


    
    
    def execute(self, context):
        directory = 'C:\\temp\\exported.obj'
        bpy.ops.import_scene.obj(filepath = directory)
        return {'FINISHED'}