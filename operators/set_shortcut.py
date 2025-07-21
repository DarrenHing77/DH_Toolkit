import bpy




class DH_OP_SetShortcut(bpy.types.Operator):
    bl_idname = 'dh.set_shortcut'
    bl_label = 'Click to choose a new shortcut'
    bl_description = 'Change DH toolkit shortcut'
    bl_options = {'REGISTER', 'INTERNAL'}

    button_text = 'Change Shortcut'

    @classmethod
    def set_button_text(cls, text, context):
        context.area.tag_redraw()
        cls.button_text = text

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        alt = event.alt
        shift = event.shift
        ctrl = event.ctrl

        if event.value in {'PRESS', 'RELEASE'}:
            txt = ''
            if ctrl:
                txt += 'Ctrl '
            if alt:
                txt += 'Alt '
            if shift:
                txt += 'Shift'
            self.set_button_text(txt, context)

        if not (alt or shift or ctrl):
            self.set_button_text('Press the new shortcut', context)

        if event.type not in {'MOUSEMOVE',
                              'INBETWEEN_MOUSEMOVE',
                              'LEFT_CTRL',
                              'LEFT_ALT',
                              'LEFT_SHIFT',
                              'RIGHT_ALT',
                              'RIGHT_CTRL',
                              'RIGHT_SHIFT', }:
            prefs = context.preferences.addons[ADDON_NAME].preferences
            prefs.ctrl = ctrl
            prefs.alt = alt
            prefs.shift = shift
            prefs.key = event.type
            self.set_button_text('Click to choose a new shortcut', context)
            return {'FINISHED'}

        elif event.type == 'ESC':
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}
