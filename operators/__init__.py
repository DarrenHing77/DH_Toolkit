import bpy

# operator classes
from .DCC_Import import DH_OP_dcc_import
from .simple_decimate import DH_OP_Decimate
from .color_picker import SetDiffuseColorOperator
from .open_proj_dir import DH_OP_Open_Proj_Dir
from .DCC_Export import DH_OP_dcc_export
from .mask_tools import DH_OP_MaskExtract
from .export_fbx_multi import DH_OP_dcc_split_export
from .collection_tools import (DH_OP_MoveToNewCollection,DH_OP_SelectAllInCollection)
from .project_manager import (
    DH_OP_CreateProjectDirectories,
    DH_OP_Proj_Manage,
    DH_OP_Project_Manager_Popup,
    PM_FolderItem,
    DH_PM_AddFolder,
    DH_PM_AddSubfolder,
    DH_PM_RemoveFolder,
)
from .multires_tools import (
    SetMultiresViewportLevelsMax,
    SetMultiresViewportLevelsZero,
    ApplyMultiresBase,DH_OP_multires_level_modal, DH_OP_MultiresSubdivide, DH_OP_AddMultires
)
from .modifier_tools import DH_OP_CopyModifiers, DH_OP_toggle_modifiers_visibility
from .transform_utils import DH_OP_ResetTransforms
from .display_utils import DH_OP_ToggleWireframe, DH_OT_ToggleVisibilityOutliner, DH_OP_toggle_lock_camera, DH_OP_SwitchToShaderEditor
from .utils import DH_OT_smart_hide
from .cycle_vertex_groups import DH_OP_CycleVertexGroups
from .shader_builder import DH_OP_BuildShader
from .weight_fill_shell import DH_OP_WeightFillModal
from .scene_cleanup import DH_OP_comprehensive_cleanup, DH_OP_cleanup_dialog


# classes tuple
classes = (
    PM_FolderItem,
    DH_OP_dcc_import,
    DH_OP_Decimate,
    SetDiffuseColorOperator,
    DH_OP_CopyModifiers,
    DH_OP_ResetTransforms,
    DH_OP_Open_Proj_Dir,
    DH_OP_dcc_export,
    DH_OP_MaskExtract,
    DH_OP_dcc_split_export, 
    SetMultiresViewportLevelsMax,
    SetMultiresViewportLevelsZero,
    ApplyMultiresBase,
    DH_OP_CreateProjectDirectories,
    DH_OP_Proj_Manage,
    DH_OP_Project_Manager_Popup,
    DH_PM_AddFolder,
    DH_PM_AddSubfolder,
    DH_PM_RemoveFolder,
    DH_OP_ToggleWireframe,
    DH_OT_ToggleVisibilityOutliner,
    DH_OP_toggle_lock_camera,
    DH_OP_SwitchToShaderEditor,
    DH_OT_smart_hide,
    DH_OP_toggle_modifiers_visibility,
    DH_OP_CycleVertexGroups,
    DH_OP_BuildShader,
    DH_OP_WeightFillModal,
    DH_OP_comprehensive_cleanup,
    DH_OP_multires_level_modal,
    DH_OP_cleanup_dialog,
    DH_OP_MultiresSubdivide,
    DH_OP_AddMultires,
    DH_OP_MoveToNewCollection,
    DH_OP_SelectAllInCollection,
    
    
    
    
)

# Registering the operators
def register_operators():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

# Unregistering the operators
def unregister_operators():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)

