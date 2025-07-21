import bpy

class DH_OT_smart_hide(bpy.types.Operator):
    """Smart hide toggle (Outliner or 3D View)"""
    bl_idname = "object.dh_smart_hide"
    bl_label = "Smart Toggle Hide"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene

        # Try getting Outliner selection first
        selected_ids = getattr(context, "selected_ids", [])
        selected = [id for id in selected_ids if isinstance(id, bpy.types.Object)]

        # Fallback to 3D View selection
        if not selected:
            selected = context.selected_objects

        # Get list of hidden object names
        hidden_names = scene.get('DH_hidden_objects', [])

        if selected:
            for obj in selected:
                obj.hide_set(True)
            # Store names, not object references
            scene['DH_hidden_objects'] = [obj.name for obj in selected]

        elif hidden_names:
            for name in hidden_names:
                obj = bpy.data.objects.get(name)
                if obj:
                    obj.hide_set(False)
                    obj.select_set(True)
            del scene['DH_hidden_objects']

        return {'FINISHED'}
