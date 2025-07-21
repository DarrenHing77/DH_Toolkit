bl_info = {
    "name": "DH_Toolkit",
    "description": "DH Tools",
    "author": "Darren Hing",
    "version": (1, 3),
    "blender": (4, 5, 0),  # Updated for 4.5
    "location": "View3D",
    "category": "3D View"
}

def register():
    try:
        from .register import register_addon
        register_addon()
        print("DH_Toolkit: Registration successful")
    except Exception as e:
        print(f"DH_Toolkit registration failed: {e}")
        import traceback
        traceback.print_exc()
        raise

def unregister():
    try:
        from .register import unregister_addon
        unregister_addon()
        print("DH_Toolkit: Unregistration successful")
    except Exception as e:
        print(f"DH_Toolkit unregistration failed: {e}")
        import traceback
        traceback.print_exc()