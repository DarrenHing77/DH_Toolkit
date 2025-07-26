import bpy

def register_addon():
    # Register components in sequence - PREFERENCES FIRST!
    from .preferences import register_preferences
    from ..property import register_properties
    from ..operators import register_operators
    from ..menus import register_menus
    from .keymap import register_keymap
    
    # Register preferences FIRST so keymap can access them
    print("🔥 DH Toolkit: Registering preferences...")
    register_preferences()
    
    # Then register other components
    print("🔥 DH Toolkit: Registering properties...")
    register_properties()
    
    print("🔥 DH Toolkit: Registering operators...")
    register_operators()
    
    print("🔥 DH Toolkit: Registering menus...")
    register_menus()
    
    # Register keymaps LAST so they can read preferences
    print("🔥 DH Toolkit: Registering keymaps...")
    register_keymap()

def unregister_addon():
    # Unregister in reverse order
    from .keymap import unregister_keymap
    from ..menus import unregister_menus
    from ..operators import unregister_operators
    from ..property import unregister_properties
    from .preferences import unregister_preferences
    
    # Unregister keymap first
    print("🔥 DH Toolkit: Unregistering keymaps...")
    unregister_keymap()
    
    # Then unregister other components
    print("🔥 DH Toolkit: Unregistering menus...")
    unregister_menus()
    
    print("🔥 DH Toolkit: Unregistering operators...")
    unregister_operators()
    
    print("🔥 DH Toolkit: Unregistering properties...")
    unregister_properties()
    
    # Unregister preferences last
    print("🔥 DH Toolkit: Unregistering preferences...")
    unregister_preferences()