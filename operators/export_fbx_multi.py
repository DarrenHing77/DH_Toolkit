import bpy
import os
import re  # Import the regular expression module
import subprocess  # Import for opening the folder
import sys  # Import for checking the operating system

class DH_OP_dcc_split_export(bpy.types.Operator):
    """Exports each selected object as its own FBX file with version control"""
    bl_idname = "dh.dcc_split_exporter"
    bl_label = "DCC Split Exporter"
    bl_options = {'REGISTER', 'UNDO'}

    overwrite: bpy.props.BoolProperty(
        name="Overwrite Latest Version",
        description="If unchecked, it will create a new versioned folder. If checked, it uses the latest version folder.",
        default=False,
    ) # type: ignore

    open_folder: bpy.props.BoolProperty(
        name="Open Folder After Export",
        description="Opens the containing folder in your file explorer after a successful export",
        default=True,
    ) # type: ignore

    def invoke(self, context, event):
        # Simply open the dialog for options
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "overwrite", text="Overwrite Latest")
        layout.prop(self, "open_folder", text="Open Folder After")

    def execute(self, context):
        # --- 1. Get Base Path ---
        filepath = bpy.data.filepath
        if not filepath:
            self.report({'ERROR'}, "Please save the .blend file before exporting.")
            return {'CANCELLED'}

        directory = os.path.dirname(filepath)
        parent_directory = os.path.abspath(os.path.join(directory, os.pardir))
        split_fbx_directory = os.path.join(parent_directory, "FBX_split")
        os.makedirs(split_fbx_directory, exist_ok=True)

        # --- 2. Check Selection & Store State ---
        selected_objects = context.selected_objects[:] # Make a copy
        active_object = context.view_layer.objects.active

        if not selected_objects:
            self.report({'ERROR'}, "No objects selected for export.")
            return {'CANCELLED'}

        # --- 3. Determine Version Folder ---
        version_num = 0
        latest_version_folder = ""

        # Find the highest existing version number
        try:
            version_pattern = re.compile(r"^v(\d{3})$") # Matches "v" followed by 3 digits
            for item in os.listdir(split_fbx_directory):
                item_path = os.path.join(split_fbx_directory, item)
                if os.path.isdir(item_path):
                    match = version_pattern.match(item)
                    if match:
                        num = int(match.group(1))
                        if num > version_num:
                            version_num = num
        except FileNotFoundError:
            pass # Folder exists or is created

        # Decide which version number to use
        if version_num > 0:
            latest_version_folder = os.path.join(
                split_fbx_directory, f"v{str(version_num).zfill(3)}"
            )

        if self.overwrite:
            version_to_use = max(1, version_num)
        else:
            if version_num == 0:
                version_to_use = 1
            else:
                file_exists = False
                for obj in selected_objects:
                    check_path = os.path.join(latest_version_folder, f"{obj.name}.fbx")
                    if os.path.exists(check_path):
                        file_exists = True
                        break
                if file_exists:
                    version_to_use = version_num + 1
                else:
                    version_to_use = version_num

        version_folder = os.path.join(split_fbx_directory, f"v{str(version_to_use).zfill(3)}")
        os.makedirs(version_folder, exist_ok=True)

        # --- 4. Loop Through and Export ---
        exported_count = 0
        try:
            for obj in selected_objects:
                # Only export mesh objects (optional, but good practice)
                if obj.type != 'MESH':
                    print(f"Skipping non-mesh object: {obj.name}")
                    continue

                # Deselect all objects
                bpy.ops.object.select_all(action='DESELECT')

                # Select and make active the current object
                obj.select_set(True)
                context.view_layer.objects.active = obj

                # Set the output FBX file path
                fbx_file = os.path.join(version_folder, f"{obj.name}.fbx")

                # Export the current object
                bpy.ops.export_scene.fbx(
                    filepath=fbx_file,
                    use_selection=True,
                    # Add any other specific FBX settings you need here
                    check_existing=False # Let it overwrite within the target folder
                )
                exported_count += 1

        except Exception as e:
            self.report({'ERROR'}, f"Export failed during loop: {e}")
            return {'CANCELLED'}
        finally:
            # --- 5. Restore Original Selection ---
            bpy.ops.object.select_all(action='DESELECT')
            for obj in selected_objects:
                obj.select_set(True)
            context.view_layer.objects.active = active_object


        self.report({'INFO'}, f"Exported {exported_count} objects to: {version_folder}")

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

