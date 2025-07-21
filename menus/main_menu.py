import bpy

from .mesh_menu import draw_mesh, draw_mask
from .display_menu import draw_display
from .project_menu import draw_project
from ..icons.icons import load_icons
from ..icons.icons import *
from .modifers_multires_menu import draw_modifiers_multires_menu
from ..operators.open_proj_dir import DH_OP_Open_Proj_Dir
from ..operators.project_manager import DH_OP_Proj_Manage, DH_OP_Project_Manager_Popup, DH_OP_CreateProjectDirectories
from ..operators.multires_tools import SetMultiresViewportLevelsZero, SetMultiresViewportLevelsMax



class DH_MT_Main_Menu(bpy.types.Menu):
    bl_idname = "DH_MT_Main_Menu"
    bl_label = "DH Toolkit"

    def draw(self, context):
        pie = self.layout.menu_pie()
        
        # Left column
        col_left = pie.column()
        box = col_left.box()
        col_left.operator("dh.move_to_new_collection", text="Move to New Collection")
        col_left.operator("dh.select_all_in_collection", text="Select Collection Objects")
        icons = load_icons()
        draw_mesh(box, context)
        col_left.separator()
        draw_mask(box, context)

        # Right column
        col_right = pie.column()
        row = col_right.row()  # Create a row to place items side by side
        row.scale_y = 1.5
        
        box_sculpt = row.box()
       

        box_display = row.box()
        draw_display(box_display, context)

        

        # Add buttons directly to the pie menu
        col_center = pie.column()
        col_center.alignment = 'CENTER' # Align items in this column to the center
        box = col_center.box()
        draw_project(box, context)

         # Add an empty space to push "Project Manager" to the bottom
        col_center.separator()
        col_center.separator()

        # Add "Project Manager" to the bottom center
        col_center.operator("dh.open_proj_dir", text="Open Project", icon='FILE_FOLDER')
        col_center.operator("dh.create_project_directories", text="Project Manager", icon='FILE_FOLDER')
        col_center.operator("screen.userpref_show", text="Open Preferences")
        col_center.separator()
        icons = load_icons()
        icon = icons.get("icon_shaderball")
        col_center.operator("dh.build_shader", text="Build Shader",icon_value=icon.icon_id)
        col_center.separator()
        col_center.operator("dh.cleanup_dialog", text="Clean Up")
        

        # Top center menu
        col_top_center = pie.column()
        col_top_center.alignment = 'CENTER'
        box = col_top_center.box()
        draw_modifiers_multires_menu(box,context)
        
        

       

        # Add "Open Project" to the middle
        

       
       
        

        
        

        
