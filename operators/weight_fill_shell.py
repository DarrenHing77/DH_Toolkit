import bpy
import bmesh
from bpy.props import FloatProperty
from mathutils import Vector
from bpy_extras import view3d_utils
from ..utlity.text_overlay import TextOverlay

class DH_OP_WeightFillModal(bpy.types.Operator):
    """Click to flood fill connected vertices with current brush weight"""
    bl_idname = "dh.weight_fill_modal"
    bl_label = "Weight Fill Shell"
    bl_description = "Click to flood fill connected vertices with weight"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return (context.active_object and 
                context.active_object.type == 'MESH' and
                context.mode == 'PAINT_WEIGHT' and
                context.active_object.vertex_groups.active)
    
    def modal(self, context, event):
        context.area.tag_redraw()
        
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.cleanup(context)
            return {'CANCELLED'}
        
        elif event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            # Raycast to find clicked vertex
            clicked_vert = self.raycast_vertex(context, event)
            if clicked_vert is not None:
                self.flood_fill_from_vertex(context, clicked_vert)
            return {'RUNNING_MODAL'}
        
        return {'RUNNING_MODAL'}
    
    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            # Set cursor
            context.window.cursor_set('EYEDROPPER')
            
            # Setup text overlay
            current_weight = context.tool_settings.unified_paint_settings.weight
            active_group = context.active_object.vertex_groups.active.name
            
            self.text_overlay = TextOverlay(
                text=f"Weight Fill Shell Active | Group: {active_group} | Weight: {current_weight:.2f} | LMB: Fill | RMB/ESC: Cancel",
                position="BOTTOM_CENTER",
                size=24,
                color=(0, 0.8, 1, 1),
                outline=True
            )
            self.text_overlay.setup_handler(context)
            
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found")
            return {'CANCELLED'}
    
    def cleanup(self, context):
        context.window.cursor_set('DEFAULT')
        if hasattr(self, 'text_overlay'):
            self.text_overlay.remove_handler()
    
    def cancel(self, context):
        self.cleanup(context)
    
    def raycast_vertex(self, context, event):
        """Find the closest vertex to mouse click"""
        region = context.region
        rv3d = context.region_data
        coord = event.mouse_region_x, event.mouse_region_y
        
        # Get view vector
        view_vector = view3d_utils.region_2d_to_vector_3d(region, rv3d, coord)
        ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, coord)
        
        # Raycast against object
        obj = context.active_object
        matrix = obj.matrix_world
        matrix_inv = matrix.inverted()
        
        # Transform ray to object space
        ray_origin_obj = matrix_inv @ ray_origin
        ray_direction_obj = matrix_inv.to_3x3() @ view_vector
        
        # Create bmesh from mesh
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        bm.verts.ensure_lookup_table()
        bm.transform(matrix)
        
        # Find closest vertex to ray
        closest_vert = None
        min_dist = float('inf')
        
        for vert in bm.verts:
            # Calculate distance from vertex to ray
            to_vert = vert.co - ray_origin
            proj_length = to_vert.dot(view_vector)
            if proj_length > 0:  # In front of camera
                proj_point = ray_origin + view_vector * proj_length
                dist = (vert.co - proj_point).length
                
                if dist < min_dist:
                    min_dist = dist
                    closest_vert = vert.index
        
        bm.free()
        
        # Only return if reasonably close to click
        if min_dist < 0.1:  # Adjust threshold as needed
            return closest_vert
        return None
    
    def flood_fill_from_vertex(self, context, start_vert_idx):
        """Flood fill connected vertices with current brush weight"""
        obj = context.active_object
        mesh = obj.data
        
        if not obj.vertex_groups.active:
            self.report({'ERROR'}, "No active vertex group")
            return
        
        # Get current weight from unified paint settings - BLENDER 4.4 FIX!
        current_weight = context.tool_settings.unified_paint_settings.weight
        
        # Switch to edit mode to access bmesh
        bpy.ops.object.mode_set(mode='EDIT')
        
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bm.verts.ensure_lookup_table()
        
        # Flood fill algorithm
        visited = set()
        to_visit = {bm.verts[start_vert_idx]}
        connected_verts = set()
        
        while to_visit:
            current = to_visit.pop()
            if current in visited:
                continue
                
            visited.add(current)
            connected_verts.add(current.index)
            
            # Add connected vertices
            for edge in current.link_edges:
                other_vert = edge.other_vert(current)
                if other_vert not in visited:
                    to_visit.add(other_vert)
        
        bm.free()
        
        # Back to weight paint mode
        bpy.ops.object.mode_set(mode='WEIGHT_PAINT')
        
        # Apply weights using current brush weight
        for vert_idx in connected_verts:
            obj.vertex_groups.active.add([vert_idx], current_weight, 'REPLACE')
        
        mesh.update()
        
        # Update overlay with result
        active_group = obj.vertex_groups.active.name
        self.text_overlay.update_text(
            f"Filled {len(connected_verts)} vertices | Group: {active_group} | Weight: {current_weight:.2f} | LMB: Fill Again | RMB/ESC: Exit"
        )
        
        self.report({'INFO'}, f"Filled {len(connected_verts)} vertices with weight {current_weight:.2f}")