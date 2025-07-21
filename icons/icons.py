import bpy
import os

# Try explicit import for 4.5
try:
    import bpy.utils.previews
except ImportError as e:
    print(f"Failed to import bpy.utils.previews: {e}")
    bpy.utils.previews = None

_icon_collection = None

def load_icons():
    global _icon_collection
    
    # Check if previews module is available
    if not hasattr(bpy.utils, 'previews') or bpy.utils.previews is None:
        print("⚠️ bpy.utils.previews not available, using fallback")
        return create_fallback_collection()
    
    if _icon_collection is None:
        try:
            _icon_collection = bpy.utils.previews.new()
            icons_dir = os.path.join(os.path.dirname(__file__))
            
            # Load all your icons
            icon_files = [
                ("icon_separate", "separate.png"),
                ("icon_cube", "cube.png"),
                ("icon_shaderball", "shaderBall.png"),
                ("icon_knife", "knife.png"),
                ("icon_subdcube", "subdCube.png"),
                ("icon_brush", "brush.png"),
                ("icon_mask", "mask.png"),
                ("icon_grid", "grid.png"),
                ("icon_extract", "extract.png"),
                ("icon_delete", "delete.png"),
                ("icon_undo", "undo.png"),
                ("icon_switcharrow", "switchArrow.png"),
                ("icon_camera", "camera.png"),
                ("icon_disk", "disk.png"),
            ]
            
            for icon_name, filename in icon_files:
                icon_path = os.path.join(icons_dir, filename)
                if os.path.exists(icon_path):
                    try:
                        _icon_collection.load(icon_name, icon_path, 'IMAGE')
                    except Exception as e:
                        print(f"Failed to load icon {filename}: {e}")
                else:
                    print(f"Icon file not found: {icon_path}")
            
            print("✅ Successfully loaded custom icons")
            
        except Exception as e:
            print(f"❌ Failed to create preview collection: {e}")
            return create_fallback_collection()
    
    return _icon_collection

def create_fallback_collection():
    """Create fake collection using builtin icons"""
    class FakeIcon:
        def __init__(self, builtin_name='FILE_BLANK'):
            # Map to builtin icon IDs 
            self.icon_id = hash(builtin_name) % 1000 + 1  # Simple hash to ID
    
    class FakeCollection:
        def __init__(self):
            self.icon_mapping = {
                "icon_separate": FakeIcon('ARROW_LEFTRIGHT'),
                "icon_cube": FakeIcon('MESH_CUBE'),
                "icon_shaderball": FakeIcon('MATERIAL'),
                "icon_knife": FakeIcon('KNIFE'),
                "icon_subdcube": FakeIcon('MESH_UVSPHERE'),
                "icon_brush": FakeIcon('BRUSH_DATA'),
                "icon_mask": FakeIcon('SCULPTMODE_HLT'),
                "icon_grid": FakeIcon('GRID'),
                "icon_extract": FakeIcon('MODIFIER'),
                "icon_delete": FakeIcon('TRASH'),
                "icon_undo": FakeIcon('LOOP_BACK'),
                "icon_switcharrow": FakeIcon('ARROW_LEFTRIGHT'),
                "icon_camera": FakeIcon('CAMERA_DATA'),
                "icon_disk": FakeIcon('DISK_DRIVE'),
            }
        
        def get(self, icon_name, default=None):
            return self.icon_mapping.get(icon_name, FakeIcon('FILE_BLANK'))
    
    return FakeCollection()

def dh_tools_clear_icons():
    global _icon_collection
    if _icon_collection and hasattr(bpy.utils, 'previews') and bpy.utils.previews:
        try:
            bpy.utils.previews.remove(_icon_collection)
        except:
            pass
    _icon_collection = None