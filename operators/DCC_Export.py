import bpy
import os
import re # Import the regular expression module
import subprocess # Import for opening the folder
import sys # Import for checking the operating system

class DH_OP_dcc_export(bpy.types.Operator):
    """Exports selected objects to an FBX file with version control"""
    bl_idname = "dh.dcc_exporter"
    bl_label = "DCC Exporter"
    bl_options = {'REGISTER', 'UNDO'}

    export_name: bpy.props.StringProperty(
        name="Export Name",
        description="Name of the exported FBX file (without version/suffix)",
        default="exported"
    ) # type: ignore

    mesh_option: bpy.props.EnumProperty(
        name="Mesh Option",
        items=[("LOW", "Low", "Save as low-poly"), ("HIGH", "High", "Save as high-poly")],
        default="LOW",
    ) # type: ignore

    overwrite: bpy.props.BoolProperty(
        name="Overwrite Latest Version",
        description="If unchecked, it will create a new versioned folder. If checked, it uses the latest version folder.",
        default=False,
    ) # type: ignore

    open_folder: bpy.props.BoolProperty(
        name="Open Folder After Export",
        description="Opens the containing folder in your file explorer after a successful export",
        default=True, # Set to True by default
    ) # type: ignore

    ignore_suffix: bpy.props.BoolProperty(
        name="Ignore _low/_high Suffix",
        description="Export without automatically appending the mesh option",
        default=False,
    ) # type: ignore

    def invoke(self, context, event):
        # If there is a single selected object, set the default export name
        if len(context.selected_objects) == 1:
            active_object = context.view_layer.objects.active
            if active_object:
                self.export_name = active_object.name
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "export_name", text="File Name")
        layout.prop(self, "mesh_option", text="Mesh Option")
        layout.prop(self, "overwrite", text="Overwrite Latest")
        layout.prop(self, "open_folder", text="Open Folder After")
        layout.prop(self, "ignore_suffix", text="Ignore Suffix")

    def execute(self, context):
        # --- 1. Get Base Path ---
        filepath = bpy.data.filepath
        if not filepath:
            self.report({'ERROR'}, "Please save the .blend file before exporting.")
            return {'CANCELLED'}

        directory = os.path.dirname(filepath)
        parent_directory = os.path.abspath(os.path.join(directory, os.pardir))
        fbx_directory = os.path.join(parent_directory, "FBX")
        os.makedirs(fbx_directory, exist_ok=True)

        # --- 2. Determine File Name ---
        if self.ignore_suffix:
            object_name = self.export_name
        else:
            object_name = f"{self.export_name}_{self.mesh_option.lower()}"
        fbx_filename = f"{object_name}.fbx"

        # --- 3. Determine Version Folder ---
        version_num = 0
        latest_version_folder = ""

        # Find the highest existing version number
        try:
            version_pattern = re.compile(r"^v(\d{3})$") # Matches "v" followed by 3 digits
            for item in os.listdir(fbx_directory):
                item_path = os.path.join(fbx_directory, item)
                if os.path.isdir(item_path):
                    match = version_pattern.match(item)
                    if match:
                        num = int(match.group(1))
                        if num > version_num:
                            version_num = num
        except FileNotFoundError:
             # This shouldn't happen since we create fbx_directory, but handle just in case
             pass

        # Decide which version number to use
        if version_num > 0:
            latest_version_folder = os.path.join(
                fbx_directory, f"v{str(version_num).zfill(3)}"
            )

        if self.overwrite:
            version_to_use = max(1, version_num)
        else:
            if version_num == 0:
                version_to_use = 1
            else:
                latest_file = os.path.join(latest_version_folder, fbx_filename)
                if os.path.exists(latest_file):
                    version_to_use = version_num + 1
                else:
                    version_to_use = version_num

        version_folder = os.path.join(fbx_directory, f"v{str(version_to_use).zfill(3)}")
        os.makedirs(version_folder, exist_ok=True) # Create the folder if it doesn't exist

        # --- 4. Set Full Export Path ---
        export_path = os.path.join(version_folder, fbx_filename)

        # --- 5. Export ---
        try:
            bpy.ops.export_scene.fbx(
                filepath=export_path,
                use_selection=True,
                # Add any other specific FBX settings you need here
                # e.g., apply_scale_options='FBX_SCALE_ALL', object_types={'MESH', 'ARMATURE'}, etc.
                check_existing=False # We handle versioning, let Blender overwrite if needed
            )
        except Exception as e:
            self.report({'ERROR'}, f"Export failed: {e}")
            return {'CANCELLED'}

        self.report({'INFO'}, f"FBX exported to: {export_path}")

        # --- 6. Open Folder (Optional) ---
        if self.open_folder:
            self.open_file_explorer(version_folder)

        return {'FINISHED'}

    def open_file_explorer(self, path):
        """Opens the given path in the system's file explorer."""
        real_path = os.path.realpath(path) # Get the absolute path
        try:
            if sys.platform == "win32":
                subprocess.Popen(['explorer', real_path])
            elif sys.platform == "darwin": # macOS
                subprocess.Popen(['open', real_path])
            else: # Linux and other Unix-like systems
                subprocess.Popen(['xdg-open', real_path])
        except Exception as e:
            print(f"Could not open folder: {e}")
            self.report({'WARNING'}, f"Could not open folder: {e}")


