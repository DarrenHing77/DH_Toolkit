import bpy
from mathutils import Vector

class DH_OP_cleanup_dialog(bpy.types.Operator):
    """Dialog to choose what cleanup operations to perform"""
    bl_idname = "dh.cleanup_dialog"
    bl_label = "DH Cleanup Options"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Properties for checkboxes
    remove_overlapping: bpy.props.BoolProperty(
        name="Remove Overlapping Objects",
        description="Delete objects that occupy the same space with identical geometry",
        default=True
    )
    
    remove_datablock_dupes: bpy.props.BoolProperty(
        name="Remove Data-block Duplicates",
        description="Delete objects that share the same mesh data (usually .001, .002 names)",
        default=True
    )
    
    cleanup_meshes: bpy.props.BoolProperty(
        name="Clean Mesh Data",
        description="Merge vertices, remove doubles, dissolve degenerate faces",
        default=True
    )
    
    remove_unused_materials: bpy.props.BoolProperty(
        name="Remove Unused Materials",
        description="Delete materials with no users",
        default=True
    )
    
    remove_unused_images: bpy.props.BoolProperty(
        name="Remove Unused Images",
        description="Delete images and textures with no users",
        default=True
    )
    
    purge_orphan_data: bpy.props.BoolProperty(
        name="Purge Orphan Data",
        description="Remove unused meshes, curves, armatures, actions",
        default=True
    )
    
    # Preview data
    overlapping_count: bpy.props.IntProperty(default=0)
    datablock_count: bpy.props.IntProperty(default=0)
    
    def invoke(self, context, event):
        # Scan for duplicates first to show counts
        self.scan_duplicates(context)
        return context.window_manager.invoke_props_dialog(self, width=400)
    
    def draw(self, context):
        layout = self.layout
        
        # Header
        layout.label(text="🔥 Choose Cleanup Operations:", icon='TRASH')
        layout.separator()
        
        # Duplicate objects section
        box = layout.box()
        box.label(text="Duplicate Objects:", icon='DUPLICATE')
        
        row = box.row()
        row.prop(self, "remove_overlapping")
        if self.overlapping_count > 0:
            row.label(text=f"({self.overlapping_count} found)", icon='ERROR')
        else:
            row.label(text="(none found)", icon='CHECKMARK')
        
        row = box.row()
        row.prop(self, "remove_datablock_dupes")
        if self.datablock_count > 0:
            row.label(text=f"({self.datablock_count} found)", icon='ERROR')
        else:
            row.label(text="(none found)", icon='CHECKMARK')
        
        # Mesh cleanup section
        box = layout.box()
        box.label(text="Mesh Cleanup:", icon='MESH_DATA')
        box.prop(self, "cleanup_meshes")
        
        # Data cleanup section
        box = layout.box()
        box.label(text="Unused Data:", icon='ORPHAN_DATA')
        box.prop(self, "remove_unused_materials")
        box.prop(self, "remove_unused_images")
        box.prop(self, "purge_orphan_data")
        
        layout.separator()
        layout.label(text="⚠️ This operation cannot be undone!", icon='ERROR')
    
    def scan_duplicates(self, context):
        """Quick scan to count duplicates for preview using same logic as main functions"""
        self.overlapping_count = 0
        self.datablock_count = 0
        
        mesh_objects = [ob for ob in context.view_layer.objects if ob.type == 'MESH']
        
        # Count overlapping duplicates using bounding box method
        def get_world_bbox_quick(obj):
            if obj.type != 'MESH' or not obj.data:
                return None
            bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
            min_x = min(corner.x for corner in bbox_corners)
            max_x = max(corner.x for corner in bbox_corners)
            min_y = min(corner.y for corner in bbox_corners)
            max_y = max(corner.y for corner in bbox_corners)
            min_z = min(corner.z for corner in bbox_corners)
            max_z = max(corner.z for corner in bbox_corners)
            return (min_x, max_x, min_y, max_y, min_z, max_z)
        
        def bboxes_overlap_quick(bbox1, bbox2):
            if not (bbox1 and bbox2):
                return False
            min_x1, max_x1, min_y1, max_y1, min_z1, max_z1 = bbox1
            min_x2, max_x2, min_y2, max_y2, min_z2, max_z2 = bbox2
            x_overlap = not (max_x1 + 0.1 < min_x2 or max_x2 + 0.1 < min_x1)
            y_overlap = not (max_y1 + 0.1 < min_y2 or max_y2 + 0.1 < min_y1)
            z_overlap = not (max_z1 + 0.1 < min_z2 or max_z2 + 0.1 < min_z1)
            return x_overlap and y_overlap and z_overlap
        
        def get_basic_signature(obj):
            if obj.type != 'MESH' or not obj.data:
                return None
            mesh = obj.data
            return (len(mesh.vertices), len(mesh.edges), len(mesh.polygons))
        
        processed = set()
        for i, obj1 in enumerate(mesh_objects):
            if obj1.name in processed:
                continue
            bbox1 = get_world_bbox_quick(obj1)
            sig1 = get_basic_signature(obj1)
            if not (bbox1 and sig1):
                continue
                
            for obj2 in mesh_objects[i+1:]:
                if obj2.name in processed:
                    continue
                bbox2 = get_world_bbox_quick(obj2)
                sig2 = get_basic_signature(obj2)
                if not (bbox2 and sig2):
                    continue
                    
                if sig1 == sig2 and bboxes_overlap_quick(bbox1, bbox2):
                    self.overlapping_count += 1
                    processed.add(obj2.name)
        
        # Count data-block duplicates (same as before)
        mesh_data_users = {}
        for obj in mesh_objects:
            mesh_name = obj.data.name
            if mesh_name not in mesh_data_users:
                mesh_data_users[mesh_name] = []
            mesh_data_users[mesh_name].append(obj)
        
        for mesh_name, users in mesh_data_users.items():
            if len(users) > 1:
                for obj in users[1:]:
                    if any(suffix in obj.name for suffix in ['.001', '.002', '.003', '.004', '.005']):
                        self.datablock_count += 1
    
    def execute(self, context):
        # Run the actual cleanup with selected options
        bpy.ops.dh_op.comprehensive_cleanup(
            'INVOKE_DEFAULT',
            remove_overlapping=self.remove_overlapping,
            remove_datablock_dupes=self.remove_datablock_dupes,
            cleanup_meshes=self.cleanup_meshes,
            remove_unused_materials=self.remove_unused_materials,
            remove_unused_images=self.remove_unused_images,
            purge_orphan_data=self.purge_orphan_data
        )
        return {'FINISHED'}

class DH_OP_comprehensive_cleanup(bpy.types.Operator):
    """Comprehensive scene cleanup with options"""
    bl_idname = "dh_op.comprehensive_cleanup"
    bl_label = "DH Comprehensive Cleanup"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Options passed from dialog
    remove_overlapping: bpy.props.BoolProperty(default=True)
    remove_datablock_dupes: bpy.props.BoolProperty(default=True)
    cleanup_meshes: bpy.props.BoolProperty(default=True)
    remove_unused_materials: bpy.props.BoolProperty(default=True)
    remove_unused_images: bpy.props.BoolProperty(default=True)
    purge_orphan_data: bpy.props.BoolProperty(default=True)
    
    def execute(self, context):
        stats = {
            'overlapping_objects': 0,
            'datablock_dupes': 0,
            'merged_vertices': 0,
            'cleaned_meshes': 0,
            'unused_materials': 0,
            'unused_images': 0,
            'purged_data': 0
        }
        
        self.report({'INFO'}, "🔥 Starting cleanup...")
        
        # 1. Remove overlapping duplicates
        if self.remove_overlapping:
            stats['overlapping_objects'] = self.remove_overlapping_objects(context)
        
        # 2. Remove data-block duplicates
        if self.remove_datablock_dupes:
            stats['datablock_dupes'] = self.remove_datablock_duplicates(context)
        
        # 3. Clean mesh data
        if self.cleanup_meshes:
            stats['merged_vertices'], stats['cleaned_meshes'] = self.cleanup_mesh_data(context)
        
        # 4. Remove unused materials
        if self.remove_unused_materials:
            stats['unused_materials'] = self.cleanup_materials()
        
        # 5. Remove unused images
        if self.remove_unused_images:
            stats['unused_images'] = self.cleanup_images()
        
        # 6. Purge orphan data
        if self.purge_orphan_data:
            stats['purged_data'] = self.purge_orphan_data_blocks()
        
        self.report_results(stats)
        return {'FINISHED'}
    
    def remove_overlapping_objects(self, context):
        """Remove objects that have overlapping bounding boxes and similar geometry"""
        
        def get_world_bbox(obj):
            """Get world-space bounding box corners"""
            if obj.type != 'MESH' or not obj.data:
                return None
            # Transform local bounding box to world space
            bbox_corners = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
            
            # Get min/max for each axis
            min_x = min(corner.x for corner in bbox_corners)
            max_x = max(corner.x for corner in bbox_corners)
            min_y = min(corner.y for corner in bbox_corners)
            max_y = max(corner.y for corner in bbox_corners)
            min_z = min(corner.z for corner in bbox_corners)
            max_z = max(corner.z for corner in bbox_corners)
            
            return (min_x, max_x, min_y, max_y, min_z, max_z)
        
        def bboxes_overlap(bbox1, bbox2, tolerance=0.1):
            """Check if two bounding boxes overlap with tolerance"""
            if not (bbox1 and bbox2):
                return False
            
            min_x1, max_x1, min_y1, max_y1, min_z1, max_z1 = bbox1
            min_x2, max_x2, min_y2, max_y2, min_z2, max_z2 = bbox2
            
            # Check overlap on each axis with tolerance
            x_overlap = not (max_x1 + tolerance < min_x2 or max_x2 + tolerance < min_x1)
            y_overlap = not (max_y1 + tolerance < min_y2 or max_y2 + tolerance < min_y1)
            z_overlap = not (max_z1 + tolerance < min_z2 or max_z2 + tolerance < min_z1)
            
            return x_overlap and y_overlap and z_overlap
        
        def get_mesh_signature(obj):
            """Get simplified mesh signature for comparison"""
            if obj.type != 'MESH' or not obj.data:
                return None
            mesh = obj.data
            
            # Basic stats
            stats = (len(mesh.vertices), len(mesh.edges), len(mesh.polygons))
            
            # Sample some vertices for geometry comparison
            vert_count = len(mesh.vertices)
            if vert_count <= 50:
                # Small mesh - check all vertices in local space
                verts = tuple(sorted((round(v.co.x, 3), round(v.co.y, 3), round(v.co.z, 3)) 
                                   for v in mesh.vertices))
            else:
                # Large mesh - sample vertices
                sample_rate = max(1, vert_count // 30)
                verts = tuple(sorted((round(mesh.vertices[i].co.x, 3), 
                                    round(mesh.vertices[i].co.y, 3), 
                                    round(mesh.vertices[i].co.z, 3)) 
                                   for i in range(0, vert_count, sample_rate)))
            
            return (stats, verts)
        
        bpy.ops.object.select_all(action='DESELECT')
        mesh_objects = [ob for ob in context.view_layer.objects if ob.type == 'MESH']
        overlapping_dupes = []
        
        print(f"🔍 Checking {len(mesh_objects)} objects for overlapping bounding boxes...")
        
        processed = set()
        for i, obj1 in enumerate(mesh_objects):
            if obj1.name in processed:
                continue
                
            bbox1 = get_world_bbox(obj1)
            sig1 = get_mesh_signature(obj1)
            if not (bbox1 and sig1):
                continue
                
            for obj2 in mesh_objects[i+1:]:
                if obj2.name in processed:
                    continue
                    
                bbox2 = get_world_bbox(obj2)
                sig2 = get_mesh_signature(obj2)
                if not (bbox2 and sig2):
                    continue
                
                # Check if they have similar geometry first (faster)
                if sig1[0] == sig2[0]:  # Same basic stats
                    # Now check if bounding boxes overlap
                    if bboxes_overlap(bbox1, bbox2, tolerance=0.1):
                        # If they also have similar vertex data, they're overlapping duplicates
                        if sig1 == sig2:
                            overlapping_dupes.append(obj2)
                            processed.add(obj2.name)
                            print(f"💀 Overlapping bboxes: '{obj2.name}' overlaps '{obj1.name}'")
                        else:
                            # Same basic stats and overlapping but different geometry - just warn
                            print(f"⚠️ Bbox overlap but different geometry: '{obj2.name}' and '{obj1.name}'")
        
        # Delete overlapping duplicates
        for obj in overlapping_dupes:
            if obj.name in context.view_layer.objects:
                obj.select_set(True)
        
        if overlapping_dupes:
            bpy.ops.object.delete(use_global=False)
        
        return len(overlapping_dupes)
    
    def remove_datablock_duplicates(self, context):
        """Remove objects sharing mesh data with auto-generated names"""
        mesh_objects = [ob for ob in context.view_layer.objects if ob.type == 'MESH']
        datablock_dupes = []
        
        mesh_data_users = {}
        for obj in mesh_objects:
            mesh_name = obj.data.name
            if mesh_name not in mesh_data_users:
                mesh_data_users[mesh_name] = []
            mesh_data_users[mesh_name].append(obj)
        
        for mesh_name, users in mesh_data_users.items():
            if len(users) > 1:
                for obj in users[1:]:
                    if any(suffix in obj.name for suffix in ['.001', '.002', '.003', '.004', '.005']):
                        datablock_dupes.append(obj)
                        print(f"📐 Data-block dupe: '{obj.name}' shares mesh '{mesh_name}'")
        
        for obj in datablock_dupes:
            if obj.name in context.view_layer.objects:
                obj.select_set(True)
        
        if datablock_dupes:
            bpy.ops.object.delete(use_global=False)
        
        return len(datablock_dupes)
    
    def cleanup_mesh_data(self, context):
        """Clean mesh data - merge vertices, remove doubles"""
        if context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        
        mesh_objects = [ob for ob in context.view_layer.objects if ob.type == 'MESH']
        if not mesh_objects:
            return 0, 0
        
        merged_verts = 0
        cleaned_count = 0
        
        bpy.ops.object.select_all(action='DESELECT')
        
        for obj in mesh_objects:
            try:
                if obj.name not in context.view_layer.objects:
                    continue
                
                obj.select_set(True)
                context.view_layer.objects.active = obj
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='SELECT')
                
                before_count = len(obj.data.vertices)
                bpy.ops.mesh.remove_doubles(threshold=0.0001)
                after_count = len(obj.data.vertices)
                merged_verts += (before_count - after_count)
                
                bpy.ops.mesh.dissolve_degenerate()
                bpy.ops.mesh.delete_loose()
                bpy.ops.object.mode_set(mode='OBJECT')
                obj.select_set(False)
                cleaned_count += 1
                
            except Exception as e:
                print(f"⚠️ Error cleaning '{obj.name}': {e}")
                try:
                    bpy.ops.object.mode_set(mode='OBJECT')
                except:
                    pass
        
        return merged_verts, cleaned_count
    
    def cleanup_materials(self):
        """Remove unused materials"""
        before_count = len(bpy.data.materials)
        unused = [mat for mat in bpy.data.materials if mat.users == 0]
        for mat in unused:
            bpy.data.materials.remove(mat)
        return len(unused)
    
    def cleanup_images(self):
        """Remove unused images and textures"""
        unused_images = [img for img in bpy.data.images if img.users == 0 and not img.use_fake_user]
        for img in unused_images:
            bpy.data.images.remove(img)
        return len(unused_images)
    
    def purge_orphan_data_blocks(self):
        """Purge orphaned data"""
        before_total = len(bpy.data.meshes) + len(bpy.data.curves) + len(bpy.data.armatures)
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
        after_total = len(bpy.data.meshes) + len(bpy.data.curves) + len(bpy.data.armatures)
        return before_total - after_total
    
    def report_results(self, stats):
        """Report cleanup results"""
        total = sum(stats.values())
        print("\n" + "="*50)
        print("🔥 DH CLEANUP RESULTS 🔥")
        print("="*50)
        
        if total > 0:
            if stats['overlapping_objects'] > 0:
                print(f"💀 Overlapping Objects: {stats['overlapping_objects']}")
            if stats['datablock_dupes'] > 0:
                print(f"📐 Data-block Dupes: {stats['datablock_dupes']}")
            if stats['merged_vertices'] > 0:
                print(f"🔗 Vertices Merged: {stats['merged_vertices']}")
            if stats['cleaned_meshes'] > 0:
                print(f"🧹 Meshes Cleaned: {stats['cleaned_meshes']}")
            if stats['unused_materials'] > 0:
                print(f"🎨 Materials Removed: {stats['unused_materials']}")
            if stats['unused_images'] > 0:
                print(f"🖼️ Images Removed: {stats['unused_images']}")
            if stats['purged_data'] > 0:
                print(f"🗑️ Data Blocks Purged: {stats['purged_data']}")
            
            print(f"\n🎯 TOTAL ITEMS CLEANED: {total}")
            self.report({'INFO'}, f"Cleaned {total} items!")
        else:
            print("✅ Scene is clean!")
            self.report({'INFO'}, "Scene is already clean!")
        print("="*50)

