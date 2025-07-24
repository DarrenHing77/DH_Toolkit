import bpy
import bmesh
import numpy as np
from mathutils import Vector
from os import path
from ..utlity.draw_2d import *
import blf
import gpu
from gpu_extras.batch import batch_for_shader
import blf

class DH_OP_MaskExtract(bpy.types.Operator):
    """Extract and solidify Masked region as a new object"""
    bl_idname = 'dh.mask_extract'
    bl_label = 'Extract Mask'
    bl_options = {'REGISTER', 'UNDO'}

    smooth_factor: bpy.props.FloatProperty(name="Smooth", default=0.5, min=0, max=1)
    skip_modal: bpy.props.BoolProperty(default=False, options={'HIDDEN'})

    def invoke(self, context, event):
        if event.alt:
            self.skip_modal = True
        return self.execute(context)

    def execute(self, context):
        original_obj = context.active_object
        if not original_obj or original_obj.type != 'MESH':
            self.report({'ERROR'}, "Select a mesh object")
            return {'CANCELLED'}

        # Check for multires modifier
        multires_mod = None
        for mod in original_obj.modifiers:
            if mod.type == 'MULTIRES':
                multires_mod = mod
                break

        self.temp_obj_to_delete = None  # Store for later cleanup

        if multires_mod:
            # Multires workflow: duplicate, store mask, apply multires, restore mask, extract
            try:
                # Switch to Object mode for duplication
                bpy.ops.object.mode_set(mode='OBJECT')
                
                # Deselect manually
                for obj in context.selected_objects:
                    obj.select_set(False)
                
                # Select and duplicate
                original_obj.select_set(True)
                context.view_layer.objects.active = original_obj
                bpy.ops.object.duplicate()
                
                duplicate_obj = context.active_object
                duplicate_obj.name = f"{original_obj.name}_extract_temp"
                
                # Store mask as vertex colors on duplicate BEFORE applying multires
                bpy.ops.object.mode_set(mode='SCULPT')
                try:
                    bpy.ops.sculpt.mask_to_vertex_colors()
                    self.report({'INFO'}, "Stored mask as vertex colors")
                except:
                    self.report({'WARNING'}, "Could not store mask - extraction may not work correctly")
                
                # Switch back to Object mode to apply multires
                bpy.ops.object.mode_set(mode='OBJECT')
                
                # Apply multires on duplicate (loses mask, keeps vertex colors)
                for mod in duplicate_obj.modifiers:
                    if mod.type == 'MULTIRES':
                        bpy.ops.object.modifier_apply(modifier=mod.name)
                        self.report({'INFO'}, f"Applied multires - now {len(duplicate_obj.data.vertices)} vertices")
                        break
                
                # Switch to sculpt mode and restore mask from vertex colors
                bpy.ops.object.mode_set(mode='SCULPT')
                try:
                    bpy.ops.sculpt.vertex_colors_to_mask()
                    self.report({'INFO'}, "Restored mask from vertex colors")
                except:
                    self.report({'WARNING'}, "Could not restore mask from vertex colors")
                
                # Now extract with the restored mask on high-poly mesh
                bpy.ops.sculpt.paint_mask_extract(
                    mask_threshold=0.5,
                    add_boundary_loop=True,
                    smooth_iterations=4,
                    apply_shrinkwrap=False,
                    add_solidify=True
                )
                
                # Store temp object for cleanup after modal
                self.temp_obj_to_delete = duplicate_obj
                
                # Get extracted object
                extracted_obj = context.active_object
                bpy.ops.object.mode_set(mode='OBJECT')
                
                self.obj = extracted_obj
                
            except Exception as e:
                self.report({'ERROR'}, f"Multires extraction failed: {e}")
                return {'CANCELLED'}
        else:
            # Normal workflow: no multires
            try:
                bpy.ops.sculpt.paint_mask_extract(
                    mask_threshold=0.5,
                    add_boundary_loop=True,
                    smooth_iterations=0,
                    apply_shrinkwrap=False,
                    add_solidify=True
                )
                self.obj = context.active_object
            except RuntimeError as e:
                self.report({'ERROR'}, f"Mask extraction failed: {e}")
                return {'CANCELLED'}

        # If Alt was held, clean up and finish
        if self.skip_modal:
            self.cleanup_temp_objects()
            self.report({'INFO'}, "Mask extracted with multires detail" if multires_mod else "Mask extracted")
            return {'FINISHED'}

        # Modal setup for thickness adjustment
        if not self.obj:
            self.report({'ERROR'}, "No active object found after extraction.")
            return {'CANCELLED'}

        # Find solidify modifier (added by extraction)
        self.solidify = None
        for mod in self.obj.modifiers:
            if mod.type == 'SOLIDIFY':
                self.solidify = mod
                break

        if self.solidify:
            self.thickness = self.solidify.thickness
        else:
            # Fallback: add our own if extraction didn't add one
            self.solidify = self.obj.modifiers.new(name="Solidify", type='SOLIDIFY')
            self.solidify.thickness = 0.01
            self.thickness = 0.01

        # Add Smooth modifier
        self.smooth = self.obj.modifiers.new(type='SMOOTH', name='SMOOTH')
        self.smooth.factor = self.smooth_factor
        self.smooth.iterations = 5

        # Set up visual slider
        self.slider = VerticalSlider(center=Vector((context.region.width / 2, context.region.height / 2)))
        self.slider.setup_handler()
        
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cleanup_temp_objects(self):
        """Clean up temporary objects after modal finishes"""
        if hasattr(self, 'temp_obj_to_delete') and self.temp_obj_to_delete:
            try:
                # Also clean up any temp vertex colors
                if self.temp_obj_to_delete.data and "Col" in self.temp_obj_to_delete.data.vertex_colors:
                    self.temp_obj_to_delete.data.vertex_colors.remove(self.temp_obj_to_delete.data.vertex_colors["Col"])
                
                # Remove the temp object
                if self.temp_obj_to_delete.name in bpy.data.objects:
                    bpy.data.objects.remove(self.temp_obj_to_delete, do_unlink=True)
            except:
                pass

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':
            mouse_co = Vector((event.mouse_region_x, event.mouse_region_y))
            scale_factor = 20 if event.shift else 100
            
            self.thickness = self.slider.eval(
                mouse_co, 
                "Thickness", 
                color=(1, 0.5, 0, 0.8),
                unit_scale=scale_factor, 
                digits=4
            )
            
            self.solidify.thickness = self.thickness
            context.area.tag_redraw()

        elif event.type in {'LEFTMOUSE', 'SPACE'}:
            self.slider.remove_handler()
            self.cleanup_temp_objects()
            return {'FINISHED'}

        elif event.type in {'ESC', 'RIGHTMOUSE'}:
            if self.obj and self.obj.name in context.view_layer.objects:
                bpy.data.objects.remove(self.obj, do_unlink=True)
            self.slider.remove_handler()
            self.cleanup_temp_objects()
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def cancel(self, context):
        if hasattr(self, 'slider'):
            self.slider.remove_handler()
        self.cleanup_temp_objects()