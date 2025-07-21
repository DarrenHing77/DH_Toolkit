import bpy

class DH_OP_ClearCustomSplitNormals(bpy.types.Operator):
    """Clear Custom Split Normals for Selected Mesh Objects"""
    bl_idname = "dh_op.clear_custom_split_normals"
    bl_label = "Clear Custom Split Normals"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                # Make the object active
                context.view_layer.objects.active = obj
                # Switch to Edit Mode
                bpy.ops.object.mode_set(mode='EDIT')
                # Clear custom split normals
                bpy.ops.mesh.customdata_custom_splitnormals_clear()
                # Return to Object Mode
                bpy.ops.object.mode_set(mode='OBJECT')
                self.report({'INFO'}, f"Cleared custom split normals for: {obj.name}")
        return {'FINISHED'}

# Registration
def register():
    bpy.utils.register_class(DH_OP_ClearCustomSplitNormals)

def unregister():
    bpy.utils.unregister_class(DH_OP_ClearCustomSplitNormals)

if __name__ == "__main__":
    register()
