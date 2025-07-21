from ..utlity.text_overlay import TextOverlay
import bpy

class DH_OP_CycleVertexGroups(bpy.types.Operator):
    """Cycle Vertex Groups and display as overlay"""
    bl_idname = 'dh.cycle_vertex_groups'
    bl_label = 'DH Cycle Vertex Groups'
    bl_options = {'REGISTER', 'UNDO'}

    group_index: bpy.props.IntProperty(default=0)

    def invoke(self, context, event):
        obj = context.object
        if not obj or obj.type != 'MESH' or not obj.vertex_groups:
            self.report({'ERROR'}, "Select a mesh with vertex groups.")
            return {'CANCELLED'}

        self.groups = obj.vertex_groups
        self.group_index = obj.vertex_groups.active_index if obj.vertex_groups.active_index >= 0 else 0
        obj.vertex_groups.active_index = self.group_index

        # Setup overlay
        self.text_overlay = TextOverlay(
            text=f"Active Vertex Group: {self.groups[self.group_index].name}",
            position="BOTTOM_CENTER",
            size=48,
            color=(1, 1, 1, 1),
            outline=True
        )
        self.text_overlay.setup_handler(context)
        
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        obj = context.object
        groups = self.groups

        if not groups or not obj:
            self.text_overlay.remove_handler()
            return {'CANCELLED'}

        redraw = False

        if event.type == 'WHEELUPMOUSE' and event.value == 'PRESS':
            self.group_index = (self.group_index + 1) % len(groups)
            obj.vertex_groups.active_index = self.group_index
            redraw = True
        elif event.type == 'WHEELDOWNMOUSE' and event.value == 'PRESS':
            self.group_index = (self.group_index - 1) % len(groups)
            obj.vertex_groups.active_index = self.group_index
            redraw = True
        elif event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            self.text_overlay.remove_handler()
            return {'FINISHED'}
        elif event.type in {'ESC', 'RIGHTMOUSE'}:
            self.text_overlay.remove_handler()
            return {'CANCELLED'}

        if redraw:
            self.text_overlay.update_text(f"Active Vertex Group: {groups[self.group_index].name}")

        return {'RUNNING_MODAL'}

    def cancel(self, context):
        self.text_overlay.remove_handler()