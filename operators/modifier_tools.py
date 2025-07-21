import bpy


# copy modifiers with settings

class DH_OP_CopyModifiers(bpy.types.Operator):
    """Copy Modifiers from the First Selected Object to Others"""  # Tooltip
    bl_idname = "dh_op.copy_modifiers"
    bl_label = "DH_OP Copy Modifiers"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Ensure at least two objects are selected
        if len(context.selected_objects) < 2:
            self.report({'WARNING'}, "Select at least two objects.")
            return {'CANCELLED'}
        
        # Get the first selected object
        first_selected = context.selected_objects[0]
        selected_objects = context.selected_objects[1:]  # Exclude the first object

        for mod in first_selected.modifiers:
            for target_obj in selected_objects:
                # Create a new modifier of the same type
                new_mod = target_obj.modifiers.new(name=mod.name, type=mod.type)
                
                # Copy general attributes
                for attr in dir(mod):
                    try:
                        if not attr.startswith("_") and not callable(getattr(mod, attr)):
                            setattr(new_mod, attr, getattr(mod, attr))
                    except AttributeError:
                        pass  # Ignore incompatible attributes

                # Special handling for Geometry Nodes modifiers
                if mod.type == 'NODES':
                    # Copy the node group
                    new_mod.node_group = mod.node_group

                    # Copy dynamically named inputs like "Input_1", "Input_2", etc.
                    for key in mod.keys():
                        if key.startswith("Input_"):
                            new_mod[key] = mod[key]

        self.report({'INFO'}, f"Copied modifiers from {first_selected.name} to {len(selected_objects)} objects.")
        return {'FINISHED'}



## toggle modifier vis

class DH_OP_toggle_modifiers_visibility(bpy.types.Operator):
    bl_idname = "dh_op.toggle_modifiers_visibility"
    bl_label = "Toggle Modifiers Visibility"
    bl_description = "Toggles visibility of all modifiers in the viewport for selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Get the current state of the first object’s first modifier for toggle logic
        toggle_state = not context.selected_objects[0].modifiers[0].show_viewport if context.selected_objects else False

        # Toggle visibility for all modifiers of selected objects
        for obj in context.selected_objects:
            for mod in obj.modifiers:
                mod.show_viewport = toggle_state
        
        return {'FINISHED'}
