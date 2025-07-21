import bpy

class DH_OP_OpenPrefsOperator(bpy.types.Operator):
    bl_idname = "dh.open_preferences"
    bl_label = "Open Preferences"

    def execute(self, context):
        bpy.ops.screen.userpref_show()  # Correct operator to open preferences in Blender 4.3
        return {'FINISHED'}

# Register the operator
def register():
    bpy.utils.register_class(DH_OP_OpenPrefsOperator)

# Unregister the operator
def unregister():
    bpy.utils.unregister_class(DH_OP_OpenPrefsOperator)

if __name__ == "__main__":
    register()
