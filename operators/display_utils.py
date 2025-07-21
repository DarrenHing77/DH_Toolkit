import bpy


# TOGGLE WIREFRAME OVERRIDE

class DH_OP_ToggleWireframe(bpy.types.Operator):
    """Toggle Wireframe Display for Selected Objects"""
    bl_idname = "dh.toggle_wireframe"
    bl_label = "Toggle Wireframe Display"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Loop through all selected objects
        for obj in context.selected_objects:
            # Ensure the object is in Object Mode (optional safeguard)
            if obj.mode == 'OBJECT':
                # Toggle between WIRE and SOLID display types
                obj.display_type = 'SOLID' if obj.display_type == 'WIRE' else 'WIRE'
        
        # Report status
        self.report({'INFO'}, "Toggled wireframe display for selected objects.")
        return {'FINISHED'}




# HIDE OUTLINER SELECTTION




class DH_OT_ToggleVisibilityOutliner(bpy.types.Operator):
    """Toggle Visibility for Outliner Selection"""
    bl_idname = "dh.toggle_visibility_outliner"
    bl_label = "Toggle Visibility for Outliner Selection"
    bl_description = "Toggle the visibility (eye icon) for selected objects in the Outliner"

    def execute(self, context):
        # Prefer selected_ids from the passed-in context (Blender 3.6+)
        # but fall back to bpy.context for compatibility with older versions
        selected_ids = getattr(context, "selected_ids", None)
        if selected_ids is None:
            selected_ids = getattr(bpy.context, "selected_ids", None)

        if not selected_ids:
            self.report({'WARNING'}, "No objects selected in the Outliner.")
            return {'CANCELLED'}

        toggled_count = 0

        for item in selected_ids:
            if isinstance(item, bpy.types.Object):  # Ensure it's an object
                # Toggle the hide_viewport property
                item.hide_viewport = not item.hide_viewport
                toggled_count += 1

        if toggled_count > 0:
            self.report({'INFO'}, f"Toggled visibility for {toggled_count} object(s).")
        else:
            self.report({'WARNING'}, "No objects found to toggle.")

        return {'FINISHED'}




class DH_OP_toggle_lock_camera(bpy.types.Operator):
    """Toggle Lock Camera to View"""
    bl_idname = "dh_op.toggle_lock_camera"
    bl_label = "Toggle Lock Camera to View"
    
    def execute(self, context):
        region_3d = context.space_data.region_3d
        region_3d.view_camera_lock = not region_3d.view_camera_lock
        self.report({'INFO'}, f"Lock Camera to View: {'On' if region_3d.view_camera_lock else 'Off'}")
        return {'FINISHED'}
    



## SWITCH TO SHADER EDITOR

class DH_OP_SwitchToShaderEditor(bpy.types.Operator):
    """
    Operator to quickly switch the current window to the Shader Editor.
    """
    bl_idname = "dh.switch_to_shader_editor"
    bl_label = "Switch to Shader Editor"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        current_area = context.area

        if current_area.type != 'NODE_EDITOR':
            current_area.type = 'NODE_EDITOR'

        current_space = current_area.spaces.active
        if current_space.type == 'NODE_EDITOR':
            current_space.tree_type = 'ShaderNodeTree'
        else:
            self.report({'WARNING'}, "Cannot switch to Shader Editor. Current area does not support tree_type switching.")

        return {'FINISHED'}


