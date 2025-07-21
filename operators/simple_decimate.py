import bpy

class DH_OP_Decimate(bpy.types.Operator):
    bl_idname = 'dh.decimate'
    bl_label = 'Decimate Selected'
    bl_description = 'Decimate all selected mesh objects'
    bl_options = {'REGISTER', 'UNDO'}

    ratio: bpy.props.FloatProperty(
        name='Ratio',
        description='Percentage to keep (0.5 = 50% of original)',
        min=0.01,
        max=1.0,
        default=0.5
    )

    @classmethod
    def poll(cls, context):
        return any(obj.type == 'MESH' for obj in context.selected_objects)

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        # Store original selection
        selected_meshes = [obj for obj in context.selected_objects if obj.type == 'MESH']
        
        if not selected_meshes:
            self.report({'WARNING'}, "No mesh objects selected")
            return {'CANCELLED'}
        
        # Ensure we're in object mode
        bpy.ops.object.mode_set(mode='OBJECT')
        
        modifier_count = 0
        
        for obj in selected_meshes:
            # Check if decimate modifier already exists
            existing_decimate = None
            for mod in obj.modifiers:
                if mod.type == 'DECIMATE':
                    existing_decimate = mod
                    break
            
            if existing_decimate:
                # Update existing modifier
                existing_decimate.ratio = self.ratio
                modifier_count += 1
            else:
                # Add new decimate modifier
                modifier = obj.modifiers.new(name="Decimate", type='DECIMATE')
                modifier.ratio = self.ratio
                modifier_count += 1
        
        self.report({'INFO'}, f"Added/updated decimate modifiers on {modifier_count} objects ({self.ratio * 100:.1f}%)")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(DH_OP_Decimate)

def unregister():
    bpy.utils.unregister_class(DH_OP_Decimate)

if __name__ == "__main__":
    register()