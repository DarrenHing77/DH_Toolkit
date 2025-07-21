import bpy
import os


class DH_OP_Open_Proj_Dir(bpy.types.Operator):
    """Open the project root directory in the system file manager."""
    bl_idname = "dh.open_proj_dir"
    bl_label = "Open Project"

    def execute(self, context):
        """Open the current project directory.

        If the current Blender file has not been saved, fall back to the
        default projects directory from the add-on preferences.
        """

        filepath = bpy.data.filepath

        if filepath:
            # Go up two folders from the .blend file location
            directory = os.path.abspath(
                os.path.join(os.path.dirname(filepath), os.pardir, os.pardir)
            )
        else:
            prefs = context.preferences.addons["DH_Toolkit"].preferences
            directory = prefs.default_projects_dir

        if directory and os.path.isdir(directory):
            os.startfile(directory)
            return {'FINISHED'}

        self.report({'WARNING'}, "Project directory not found")
        return {'CANCELLED'}
