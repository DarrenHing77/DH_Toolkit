import bpy

# Nuke all materials from selected objects
for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        # Clear all material slots
        obj.data.materials.clear()
        print(f"Nuked materials from: {obj.name}")

print("Material genocide complete.")