import bpy

class SetDiffuseColorOperator(bpy.types.Operator):
    """Set the diffuse color of the active material"""
    bl_idname = "object.set_diffuse_color"
    bl_label = "Set VP Color"

    def execute(self, context):
        material = bpy.context.object.active_material
        color_picker = bpy.ops.bpy.types.ColorPicker
        color_picker('INVOKE_DEFAULT')
        color = bpy.context.color
        material.diffuse_color = color
        return {'FINISHED'}