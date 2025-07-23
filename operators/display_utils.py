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


class DH_OP_ToggleVisibilityOutliner(bpy.types.Operator):
    """Toggle Visibility for Outliner Selection"""
    bl_idname = "dh.toggle_visibility_outliner"
    bl_label = "Toggle Visibility"

    def execute(self, context):
        # Try outliner selection first
        selected_ids = getattr(context, "selected_ids", [])
        objects = [item for item in selected_ids if isinstance(item, bpy.types.Object)]
        
        # Fallback to viewport selection
        if not objects:
            objects = context.selected_objects
        
        # If still nothing selected, try to unhide stored hidden objects
        if not objects:
            hidden_names = context.scene.get('DH_hidden_objects', [])
            if hidden_names:
                objects = [bpy.data.objects.get(name) for name in hidden_names if bpy.data.objects.get(name)]
                objects = [obj for obj in objects if obj]  # Filter out None
                
                if objects:
                    # Unhide stored objects
                    for obj in objects:
                        obj.hide_viewport = False
                        obj.hide_select = False
                        obj.hide_render = False
                        obj.hide_set(False)
                        obj.select_set(True)
                    
                    # Clear the stored list
                    del context.scene['DH_hidden_objects']
                    
                    self.report({'INFO'}, f"Unhid {len(objects)} stored objects.")
                    return {'FINISHED'}
        
        if not objects:
            self.report({'WARNING'}, "Nothing selected and no hidden objects stored.")
            return {'CANCELLED'}

        # Store object names before hiding
        hiding_objects = []
        
        for obj in objects:
            is_visible = not obj.hide_viewport and not obj.hide_get()
            
            if is_visible:
                # Hide it and store name
                obj.hide_viewport = True
                hiding_objects.append(obj.name)
            else:
                # Show it
                obj.hide_viewport = False
                obj.hide_select = False
                obj.hide_render = False
                obj.hide_set(False)
        
        # Store hidden object names
        if hiding_objects:
            context.scene['DH_hidden_objects'] = hiding_objects
        
        # Force updates
        context.view_layer.update()
        for area in context.screen.areas:
            area.tag_redraw()

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


