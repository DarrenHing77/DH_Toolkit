import bpy

class DH_OP_ResetTransforms(bpy.types.Operator):
    """
    Resets the location, rotation, and scale of the selected objects to their default values.
    """
    bl_idname = "dh_op.reset_transforms"
    bl_label = "Reset Transforms"
    bl_description = "Reset all transforms (location, rotation, scale) to zero or default"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Loop through all selected objects
        for obj in context.selected_objects:
            # Reset location, rotation, and scale
            obj.location = (0.0, 0.0, 0.0)
            obj.rotation_euler = (0.0, 0.0, 0.0)
            obj.scale = (1.0, 1.0, 1.0)

        self.report({'INFO'}, "Transforms reset to defaults")
        return {'FINISHED'}







