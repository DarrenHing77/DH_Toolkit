import bpy
import os
import tempfile

# Store reference to the active project manager operator
_active_pm_op = None


class PM_FolderItem(bpy.types.PropertyGroup):
    path: bpy.props.StringProperty(name="Folder Path")
    expanded: bpy.props.BoolProperty(name="Expanded", default=True)

def create_project_directories(project_name, directory, folders):
    """Create all folders for the project on disk."""
    # Use the provided project name and directory
    project_path = os.path.join(directory, project_name)

    # Create the main project directory
    os.makedirs(project_path, exist_ok=True)


    # Create all subdirectories
    for subdir in folders:
        subdir_path = os.path.join(project_path, subdir)
        os.makedirs(subdir_path, exist_ok=True)


# Operator to get project name and directory from the user
class DH_OP_Proj_Manage(bpy.types.Operator):
    bl_idname = "dh.project_manage"
    bl_label = "Project Manager"

    project_name: bpy.props.StringProperty(name="Project Name", default="MyProject")
    directory: bpy.props.StringProperty(name="Directory", subtype='DIR_PATH')
    save_scene: bpy.props.BoolProperty(name="Save Current Scene", default=False)
    folder_items: bpy.props.CollectionProperty(type=PM_FolderItem)

    def _has_children(self, index):
        prefix = self.folder_items[index].path + os.sep
        next_index = index + 1
        return next_index < len(self.folder_items) and self.folder_items[next_index].path.startswith(prefix)

    def _is_item_visible(self, index):
        path = self.folder_items[index].path
        while os.sep in path:
            path = os.path.dirname(path)
            for i in range(index - 1, -1, -1):
                if self.folder_items[i].path == path:
                    if not self.folder_items[i].expanded:
                        return False
                    break
        return True

    def _add_default_folders(self):
        """Populate the folder list with a default hierarchy."""
        defaults = [
            "01_Ref",
            os.path.join("01_Ref", "PR"),
            "02_Photoshop",
            os.path.join("02_Photoshop", "PSD"),
            os.path.join("02_Photoshop", "images"),
            "03_Blender",
            os.path.join("03_Blender", "Scenes"),
            os.path.join("03_Blender", "FBX"),
            os.path.join("03_Blender", "Textures"),
            os.path.join("03_Blender", "Renders"),
            "04_Substance",
            os.path.join("04_Substance", "Scenes"),
            os.path.join("04_Substance", "FBX"),
            os.path.join("04_Substance", "Textures"),
            os.path.join("04_Substance", "Textures", "01_Painter"),
            os.path.join("04_Substance", "Textures", "02_Designer"),
            os.path.join("04_Substance", "SBS"),
            os.path.join("04_Substance", "SBSAR"),
            "05_Resolve",
            os.path.join("05_Resolve", "Resources"),
            os.path.join("05_Resolve", "Stills"),
            os.path.join("05_Resolve", "Videos"),
            "06_Daz",
        ]
        for path in defaults:
            item = self.folder_items.add()
            item.path = path
            item.expanded = True

    def execute(self, context):
        if not self.project_name or not self.directory:
            self.report({'ERROR'}, "Please enter a project name and directory")
            return {'CANCELLED'}

        folders = [item.path for item in self.folder_items]
        create_project_directories(self.project_name, self.directory, folders)

        if self.save_scene:
            project_path = os.path.join(self.directory, self.project_name)
            scene_dir = os.path.join(project_path, "03_Blender", "Scenes")
            os.makedirs(scene_dir, exist_ok=True)
            filepath = os.path.join(scene_dir, f"{self.project_name}_v001.blend")
            bpy.ops.wm.save_as_mainfile(filepath=filepath)

        bpy.ops.dh.project_manager_popup(
            'INVOKE_DEFAULT',
            project_name=self.project_name,
            directory=self.directory
        )
        global _active_pm_op
        _active_pm_op = None
        return {'FINISHED'}

    def invoke(self, context, event):
        global _active_pm_op
        _active_pm_op = self
        if not self.directory:
            prefs = context.preferences.addons["DH_Toolkit"].preferences
            self.directory = prefs.default_projects_dir
        if not self.folder_items:
            self._add_default_folders()
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "project_name")
        layout.prop(self, "directory")
        layout.prop(self, "save_scene")
        layout.separator()

        layout.operator("dh.pm_add_folder", icon='ADD', text="Add Folder")

        for i, item in enumerate(self.folder_items):
            if not self._is_item_visible(i):
                continue
            row = layout.row(align=True)
            indent = item.path.count(os.sep)
            sub = row.row(align=True)
            for _ in range(indent):
                sub.label(text="", icon='BLANK1')
            
            if self._has_children(i):
                icon = 'TRIA_DOWN' if item.expanded else 'TRIA_RIGHT'
                op = sub.operator("dh.pm_toggle_folder", text="", icon=icon, emboss=False)
                if op:
                    op.index = i
            else:
                sub.label(text="", icon='BLANK1')
            
            folder_icon = 'FILE_FOLDER' if indent == 0 else 'FILE_CACHE'
            sub.label(text=os.path.basename(item.path), icon=folder_icon)
            
            op = row.operator("dh.pm_add_subfolder", text="", icon='ADD')
            if op:
                op.index = i
            op = row.operator("dh.pm_remove_folder", text="", icon='REMOVE')
            if op:
                op.index = i

    def cancel(self, context):
        global _active_pm_op
        _active_pm_op = None

# Operators to modify the folder list while the popup is open
class DH_PM_AddFolder(bpy.types.Operator):
    bl_idname = "dh.pm_add_folder"
    bl_label = "Add Folder"

    def execute(self, context):
        global _active_pm_op
        op = _active_pm_op
        if op:
            item = op.folder_items.add()
            item.path = f"New_Folder_{len(op.folder_items)}"
            item.expanded = True
            # ensure new folders are root level by moving after the last
            # existing top level item
            insert_index = len(op.folder_items) - 1
            last_root = -1
            for i, it in enumerate(op.folder_items[:-1]):
                if os.sep not in it.path:
                    last_root = i
            if last_root != -1:
                insert_index = last_root + 1
            op.folder_items.move(len(op.folder_items) - 1, insert_index)
        return {'FINISHED'}


class DH_PM_AddSubfolder(bpy.types.Operator):
    bl_idname = "dh.pm_add_subfolder"
    bl_label = "Add Subfolder"

    index: bpy.props.IntProperty()

    def execute(self, context):
        global _active_pm_op
        op = _active_pm_op
        if op and 0 <= self.index < len(op.folder_items):
            parent = op.folder_items[self.index].path
            parent_indent = parent.count(os.sep)
            item = op.folder_items.add()
            item.path = os.path.join(parent, f"New_Folder_{len(op.folder_items)}")
            item.expanded = True

            # insert the new item directly after the parent's existing subtree
            insert_index = self.index + 1
            for i in range(self.index + 1, len(op.folder_items) - 1):
                indent = op.folder_items[i].path.count(os.sep)
                if indent <= parent_indent:
                    break
                insert_index = i + 1
            op.folder_items.move(len(op.folder_items) - 1, insert_index)
        return {'FINISHED'}


class DH_PM_RemoveFolder(bpy.types.Operator):
    bl_idname = "dh.pm_remove_folder"
    bl_label = "Remove Folder"

    index: bpy.props.IntProperty()

    def execute(self, context):
        global _active_pm_op
        op = _active_pm_op
        if op and 0 <= self.index < len(op.folder_items):
            target = op.folder_items[self.index].path
            prefix = target + os.sep
            # remove children first
            idx = self.index + 1
            while idx < len(op.folder_items) and op.folder_items[idx].path.startswith(prefix):
                op.folder_items.remove(idx)
            op.folder_items.remove(self.index)
        return {'FINISHED'}


class DH_PM_ToggleFolder(bpy.types.Operator):
    bl_idname = "dh.pm_toggle_folder"
    bl_label = "Toggle Folder"

    index: bpy.props.IntProperty()

    def execute(self, context):
        global _active_pm_op
        op = _active_pm_op
        if op and 0 <= self.index < len(op.folder_items):
            item = op.folder_items[self.index]
            item.expanded = not item.expanded
        return {'FINISHED'}

# Popup operator to display the success message
class DH_OP_Project_Manager_Popup(bpy.types.Operator):
    bl_idname = "dh.project_manager_popup"
    bl_label = "Project Created"

    project_name: bpy.props.StringProperty()
    directory: bpy.props.StringProperty()

    def execute(self, context):
        return context.window_manager.invoke_popup(self, width=400)

    def draw(self, context):
        layout = self.layout
        layout.label(text=f"Project '{self.project_name}' created in: {self.directory}")

# Register the popup operator
class DH_OP_CreateProjectDirectories(bpy.types.Operator):
    bl_idname = "dh.create_project_directories"
    bl_label = "Create Project Directories"

    def execute(self, context):
        bpy.ops.dh.project_manage('INVOKE_DEFAULT')
        return {'FINISHED'}