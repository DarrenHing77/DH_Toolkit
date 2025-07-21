import bpy
import os

class DH_OP_dcc_split_export(bpy.types.Operator):
    """Exports each selected object as its own FBX file"""
    bl_idname = "dh.dcc_split_exporter"
    bl_label = "DCC Split Exporter"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Get the path of the current .blend file
        filepath = bpy.data.filepath
        if not filepath:
            self.report({'ERROR'}, "Please save the .blend file before exporting.")
            return {'CANCELLED'}
        
        # Get the directory of the current .blend file
        directory = os.path.dirname(filepath)
        
        # Go up one directory and create an "FBX_split" folder
        parent_directory = os.path.abspath(os.path.join(directory, os.pardir))
        split_fbx_directory = os.path.join(parent_directory, "FBX_split")
        
        # Ensure the FBX_split folder exists
        os.makedirs(split_fbx_directory, exist_ok=True)

        # Loop through selected objects
        selected_objects = context.selected_objects
        if not selected_objects:
            self.report({'ERROR'}, "No objects selected for export.")
            return {'CANCELLED'}
        
        for obj in selected_objects:
            # Deselect all objects
            bpy.ops.object.select_all(action='DESELECT')
            
            # Select the current object
            obj.select_set(True)
            context.view_layer.objects.active = obj
            
            # Set the output FBX file path
            fbx_file = os.path.join(split_fbx_directory, f"{obj.name}.fbx")
            
            # Export the current object to the FBX file
            bpy.ops.export_scene.fbx(filepath=fbx_file, use_selection=True)
        
        self.report({'INFO'}, f"Exported {len(selected_objects)} objects to: {split_fbx_directory}")
        return {'FINISHED'}

# Register the operator
def register():
    bpy.utils.register_class(DH_OP_dcc_split_export)

def unregister():
    bpy.utils.unregister_class(DH_OP_dcc_split_export)

if __name__ == "__main__":
    register()
