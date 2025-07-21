import bpy

# Import all menu classes
from .main_menu import DH_MT_Main_Menu
from .edit_menu import DH_MT_Edit_Menu
from .sculpt_menu import DH_MT_Sculpt_Menu
from .texture_paint_menu import DH_MT_Texture_Paint_Menu
from .weight_paint_menu import DH_MT_Weight_Paint_Menu
from .uv_edit_menu import DH_MT_UV_Edit_Menu
from .shader_editor_menu import DH_MT_Shader_Editor_Menu

# All menu classes
classes = (
    DH_MT_Main_Menu,
    DH_MT_Edit_Menu,
    DH_MT_Sculpt_Menu,
    DH_MT_Texture_Paint_Menu,
    DH_MT_Weight_Paint_Menu,
    DH_MT_UV_Edit_Menu,
    DH_MT_Shader_Editor_Menu,
)

def register_menus():
    """Register all menu classes"""
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

def unregister_menus():
    """Unregister all menu classes"""
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)