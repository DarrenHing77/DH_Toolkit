import bpy

def register_addon():
    # Register components in sequence
    from .preferences import register_preferences
    from ..property import register_properties
    from ..operators import register_operators
    from ..menus import register_menus
    from .keymap import register_keymap
    
    # Register preferences first to make them available to other components
    register_preferences()
    
    # Then register other components
    register_properties()
    register_operators()
    register_menus()
    register_keymap()

def unregister_addon():
    # Unregister in reverse order
    from .keymap import unregister_keymap
    from ..menus import unregister_menus
    from ..operators import unregister_operators
    from ..property import unregister_properties
    from .preferences import unregister_preferences
    
    # Unregister keymap first
    unregister_keymap()
    
    # Then unregister other components
    unregister_menus()
    unregister_operators()
    unregister_properties()
    
    # Unregister preferences last
    unregister_preferences()