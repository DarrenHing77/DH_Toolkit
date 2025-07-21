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









def create_object_from_bm(bm, matrix_world, name='new_mesh', set_active=False):
    mesh = bpy.data.meshes.new(name=name)
    bm.to_mesh(mesh)
    obj = bpy.data.objects.new(name=name, object_data=mesh)
    obj.matrix_world = matrix_world
    bpy.context.collection.objects.link(obj)
    if set_active:
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
    return obj


def get_bm_and_mask(mesh):
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    bm.faces.ensure_lookup_table()

    # Access the sculpt mask data from faces
    for face in bm.faces:
        if not face.select:  # If the face is not selected by the mask
            bm.faces.remove(face) # Remove the face

    return bm, None  # You don't need to return a separate mask layer


def boundary_loops_create(bm, loops=2, smoothing=6, smooth_depth=3):
    edges = [e for e in bm.edges if e.is_boundary]
    for _ in range(loops):
        geom = bmesh.ops.extrude_edge_only(bm, edges=edges)['geom']
        edges = [e for e in geom if isinstance(e, bmesh.types.BMEdge)]
    boundary_verts = set(v for v in geom if isinstance(v, bmesh.types.BMVert))
    seen_verts = boundary_verts.copy()
    curr_layer = boundary_verts
    new_layer = set()
    choosen_ones = set()
    for _ in range(smooth_depth + loops):
        for vert in curr_layer:
            for other in (e.other_vert(vert) for e in vert.link_edges):
                if other not in seen_verts:
                    new_layer.add(other)
                    seen_verts.add(other)
                    choosen_ones.add(other)
        curr_layer.clear()
        new_layer, curr_layer = curr_layer, new_layer
    choosen_ones = list(choosen_ones)
    while smooth_depth > 0:
        factor = min(smooth_depth, 0.5)
        smooth_depth -= 0.5
        bmesh.ops.smooth_vert(bm, verts=choosen_ones, use_axis_x=True,
                              use_axis_y=True,
                              use_axis_z=True,
                              factor=factor)


class BoundaryPolish:
    def __init__(self, bm):
        bm.verts.ensure_lookup_table()

        class NeighborData:
            def __init__(self, vert, others):
                self.vert = vert
                self.others = others
                self.disp_vec = Vector()

            def update_vec(self):
                self.disp_vec *= 0
                for other in self.others:
                    self.disp_vec += other.co
                self.disp_vec /= len(self.others)
                self.disp_vec = self.vert.co - self.disp_vec
                self.disp_vec -= self.vert.normal.dot(self.disp_vec) * self.vert.normal

        self.boundary_mapping = {}
        for vert in bm.verts:
            if vert.is_boundary:
                others = []
                for other in (edge.other_vert(vert) for edge in vert.link_edges if edge.is_boundary):
                    if other.is_boundary:
                        others.append(other)
                self.boundary_mapping[vert] = NeighborData(vert, others)

        self.original_coords = [vert.co.copy() for vert in self.boundary_mapping.keys()]

    def reset(self):
        for vert, co in zip(self.boundary_mapping.keys(), self.original_coords):
            vert.co.xyz = co.xyz

    def polish(self, iterations=30):
        for _ in range(iterations):
            for dt in self.boundary_mapping.values():
                dt.update_vec()

            for vert, dt in self.boundary_mapping.items():
                avg_vec = Vector()
                avg_vec -= dt.disp_vec * 0.5
                for other in dt.others:
                    avg_vec += self.boundary_mapping[other].disp_vec * 0.25
                vert.co += avg_vec * 0.5

    def back_to_mesh(self, mesh):
        for vert in self.boundary_mapping.keys():
            mesh.vertices[vert.index].co = vert.co





class DH_OP_MaskExtract(bpy.types.Operator):
    """Extract and solidify Masked region as a new object"""
    bl_idname = 'dh.mask_extract'
    bl_label = 'Extract Mask'
    bl_options = {'REGISTER', 'UNDO'}

    smooth_factor: bpy.props.FloatProperty(name="Smooth", default=0.5, min=0, max=1) # type: ignore

    def execute(self, context):
        try:
            bpy.ops.mesh.paint_mask_extract(mask_threshold=0.5, smooth_iterations=0)
        except RuntimeError as e:
            self.report({'ERROR'}, f"Mask extraction failed: {e}")
            return {'CANCELLED'}

        self.obj = context.active_object
        if not self.obj:
            self.report({'ERROR'}, "No active object found.")
            return {'CANCELLED'}

        # Add or retrieve Solidify modifier
        if "geometry_extract_solidify" not in self.obj.modifiers:
            self.solidify = self.obj.modifiers.new(name="geometry_extract_solidify", type='SOLIDIFY')
        else:
            self.solidify = self.obj.modifiers["geometry_extract_solidify"]
        
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

    def modal(self, context, event):
        if event.type == 'MOUSEMOVE':
            mouse_co = Vector((event.mouse_region_x, event.mouse_region_y))
            
            # Scale factor - reduced if shift is held
            scale_factor = 20 if event.shift else 100
            
            # Use slider to calculate and display thickness
            self.thickness = self.slider.eval(
                mouse_co, 
                "Thickness", 
                color=(1, 0.5, 0, 0.8),  # Orange color
                unit_scale=scale_factor, 
                digits=4
            )
            
            self.solidify.thickness = self.thickness
            context.area.tag_redraw()

        elif event.type in {'LEFTMOUSE', 'SPACE'}:
            self.slider.remove_handler()
            return {'FINISHED'}

        elif event.type in {'ESC', 'RIGHTMOUSE'}:
            bpy.ops.object.delete(use_global=False)
            self.slider.remove_handler()
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}

    def cancel(self, context):
        if hasattr(self, 'slider'):
            self.slider.remove_handler()



