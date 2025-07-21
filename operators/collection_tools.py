import bpy

class DH_OP_MoveToNewCollection(bpy.types.Operator):
    """Move selected objects to a new collection"""
    bl_idname = "dh.move_to_new_collection"
    bl_label = "Move to New Collection"
    bl_options = {'REGISTER', 'UNDO'}
    
    collection_name: bpy.props.StringProperty(
        name="Collection Name",
        default="New Collection"
    )
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def execute(self, context):
        selected = context.selected_objects
        if not selected:
            self.report({'ERROR'}, "No objects selected")
            return {'CANCELLED'}
        
        # Create new collection
        new_collection = bpy.data.collections.new(self.collection_name)
        context.scene.collection.children.link(new_collection)
        
        # Move objects to new collection
        for obj in selected:
            # Remove from all current collections
            for col in obj.users_collection:
                col.objects.unlink(obj)
            # Add to new collection
            new_collection.objects.link(obj)
        
        self.report({'INFO'}, f"Moved {len(selected)} objects to '{self.collection_name}'")
        return {'FINISHED'}


class DH_OP_SelectAllInCollection(bpy.types.Operator):
    """Select all objects in the active object's collection"""
    bl_idname = "dh.select_all_in_collection"
    bl_label = "Select All in Collection"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        active_obj = context.active_object
        if not active_obj:
            self.report({'ERROR'}, "No active object")
            return {'CANCELLED'}
        
        # Get the first collection the active object is in
        if not active_obj.users_collection:
            self.report({'ERROR'}, "Active object not in any collection")
            return {'CANCELLED'}
        
        target_collection = active_obj.users_collection[0]
        
        # Deselect all first
        bpy.ops.object.select_all(action='DESELECT')
        
        # Select all objects in the collection
        count = 0
        for obj in target_collection.objects:
            if obj.type in {'MESH', 'CURVE', 'SURFACE', 'META', 'FONT', 'ARMATURE', 'LATTICE', 'EMPTY', 'GPENCIL', 'CAMERA', 'LIGHT', 'SPEAKER'}:
                obj.select_set(True)
                count += 1
        
        self.report({'INFO'}, f"Selected {count} objects from '{target_collection.name}'")
        return {'FINISHED'}