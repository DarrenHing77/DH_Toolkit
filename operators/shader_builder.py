import bpy
import os
import re

class DH_OP_BuildShader(bpy.types.Operator):
    bl_idname = "dh.build_shader"
    bl_label = "Build Shader From Selected Textures"
    bl_options = {'REGISTER', 'UNDO'}

    files: bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)
    directory: bpy.props.StringProperty(subtype='DIR_PATH')

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        if not self.files:
            self.report({'ERROR'}, "No files selected.")
            return {'CANCELLED'}

        self.build_shader(context)
        return {'FINISHED'}

    def get_addon_prefs(self):
        """Get addon preferences for custom patterns"""
        addon_prefs = bpy.context.preferences.addons["DH_Toolkit"].preferences
        return addon_prefs

    def get_texture_patterns(self):
        """Smart texture detection patterns - gets base patterns + user patterns from prefs"""
        base_patterns = {
            "basecolor": [
                r"(?:basecolor|albedo|diffuse|diff|col|color|bc)(?:_\d+k?)?",
                r".*_(?:basecolor|albedo|diffuse|diff|col|color|bc)(?:_\d+k?)?"
            ],
            "normal": [
                r"(?:normal|nrm|nor|bump|nml)(?:_\d+k?)?",
                r".*_(?:normal|nrm|nor|bump|nml)(?:_\d+k?)?"
            ],
            "orm": [
                r"(?:orm|occlusionroughnessmetallic|roughnessmetallic)(?:_\d+k?)?",
                r".*_(?:orm|occlusionroughnessmetallic|roughnessmetallic)(?:_\d+k?)?"
            ],
            "roughness": [
                r"(?:roughness|rough|rgh)(?:_\d+k?)?",
                r".*_(?:roughness|rough|rgh)(?:_\d+k?)?"
            ],
            "metallic": [
                r"(?:metallic|metal|met)(?:_\d+k?)?",
                r".*_(?:metallic|metal|met)(?:_\d+k?)?"
            ],
            "ao": [
                r"(?:ao|ambient|occlusion|ambientocclusion)(?:_\d+k?)?",
                r".*_(?:ao|ambient|occlusion|ambientocclusion)(?:_\d+k?)?"
            ],
            "height": [
                r"(?:height|disp|displacement)(?:_\d+k?)?",
                r".*_(?:height|disp|displacement)(?:_\d+k?)?"
            ],
            "emission": [
                r"(?:emission|emissive|emit|glow)(?:_\d+k?)?",
                r".*_(?:emission|emissive|emit|glow)(?:_\d+k?)?"
            ]
        }
        
        # Get user patterns from addon preferences
        try:
            prefs = self.get_addon_prefs()
            
            if prefs.use_advanced_patterns:
                # Use advanced regex patterns if enabled
                advanced_mappings = {
                    "basecolor": prefs.regex_basecolor,
                    "normal": prefs.regex_normal,
                    "roughness": prefs.regex_roughness, 
                    "metallic": prefs.regex_metallic,
                    "orm": prefs.regex_orm,
                    "height": prefs.regex_height,
                    "ao": prefs.regex_ao,
                    "emission": prefs.regex_emission
                }
                
                for tex_type, regex_pattern in advanced_mappings.items():
                    if regex_pattern.strip():
                        base_patterns[tex_type].append(regex_pattern.strip())
                        print(f"Added advanced pattern for {tex_type}: {regex_pattern.strip()}")
            else:
                # Build simple patterns from user inputs
                sep = prefs.naming_separator if prefs.naming_separator else ""
                escape_sep = re.escape(sep) if sep else ""
                
                suffix_mappings = {
                    "basecolor": prefs.suffix_basecolor,
                    "normal": prefs.suffix_normal,
                    "roughness": prefs.suffix_roughness, 
                    "metallic": prefs.suffix_metallic,
                    "orm": prefs.suffix_orm,
                    "height": prefs.suffix_height,
                    "ao": prefs.suffix_ao,
                    "emission": prefs.suffix_emission
                }
                
                for tex_type, suffix in suffix_mappings.items():
                    if suffix.strip():
                        # Create patterns for the user's naming convention
                        if sep:
                            # With separator: "material_d" or "material_d_4k"
                            pattern = f".*{escape_sep}{re.escape(suffix.strip())}(?:{escape_sep}\\d+k?)?$"
                        else:
                            # No separator: "materiald" 
                            pattern = f".*{re.escape(suffix.strip())}(?:\\d+k?)?$"
                        
                        base_patterns[tex_type].append(pattern)
                        print(f"Added simple pattern for {tex_type}: {pattern}")
                        
        except Exception as e:
            # Fallback if preferences aren't available yet
            print(f"Using default patterns only: {e}")
        
        return base_patterns

    def get_node_layout(self):
        """Standard node positioning - modify these coordinates for different layouts"""
        return {
            "output": (600, 0),
            "bsdf": (300, 0),
            "basecolor": (-400, 300),
            "normal": (-400, 0),
            "normal_map": (0, -100),
            "orm": (-400, -300),
            "orm_separate": (0, -400),
            "roughness": (-400, -200),
            "metallic": (-400, -500),
            "ao": (-400, 100),
            "height": (-400, -100),
            "emission": (-400, 400),
            "mix_ao": (0, 200),
            "displacement": (300, -200)
        }

    def detect_texture_type(self, filename):
        """Smarter texture type detection using regex patterns"""
        filename_clean = os.path.splitext(filename.lower())[0]
        patterns = self.get_texture_patterns()
        
        for tex_type, regex_list in patterns.items():
            for pattern in regex_list:
                if re.search(pattern, filename_clean):
                    return tex_type
        return None

    def build_shader(self, context):
        obj = context.active_object
        if not obj or not obj.data or not hasattr(obj.data, 'materials'):
            self.report({'ERROR'}, "Select a goddamn mesh object first.")
            return

        # Create material
        clean_name = self.clean_material_name(obj.name)
        mat = bpy.data.materials.new(name=clean_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        layout = self.get_node_layout()

        # Create standard nodes
        output_node = nodes.new(type='ShaderNodeOutputMaterial')
        output_node.location = layout["output"]

        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf.location = layout["bsdf"]
        links.new(bsdf.outputs['BSDF'], output_node.inputs['Surface'])

        # Process textures
        detected_textures = {}
        
        for file_elem in self.files:
            file = file_elem.name
            filepath = os.path.join(self.directory, file)
            tex_type = self.detect_texture_type(file)
            
            if not tex_type:
                print(f"Skipping {file} — no matching pattern found.")
                continue
                
            detected_textures[tex_type] = filepath

        if not detected_textures:
            self.report({'WARNING'}, "No matching textures found with current patterns.")
            return

        # Build shader nodes based on detected textures
        self.build_standard_setup(nodes, links, detected_textures, output_node, layout)

        # Assign material
        if obj.data.materials:
            obj.data.materials[0] = mat
        else:
            obj.data.materials.append(mat)

        print(f"Built shader with textures: {list(detected_textures.keys())}")

    def build_standard_setup(self, nodes, links, textures, output_node, layout):
        """Build different setups based on texture types found"""
        bsdf = nodes.get("Principled BSDF")
        
        # Determine setup type
        has_orm = "orm" in textures
        has_separate_metal_rough = "roughness" in textures or "metallic" in textures
        has_height = "height" in textures
        
        print(f"Building setup: ORM={has_orm}, Separate R/M={has_separate_metal_rough}, Height={has_height}")
        
        # Base Color
        if "basecolor" in textures:
            tex_node = self.create_texture_node(nodes, textures["basecolor"], layout["basecolor"])
            tex_node.image.colorspace_settings.name = "sRGB"
            
            # Mix with AO if available and not using ORM
            if "ao" in textures and not has_orm:
                ao_node = self.create_texture_node(nodes, textures["ao"], layout["ao"])
                ao_node.image.colorspace_settings.name = "Non-Color"
                
                mix_node = nodes.new(type='ShaderNodeMixRGB')
                mix_node.location = layout["mix_ao"]
                mix_node.blend_type = 'MULTIPLY'
                mix_node.inputs['Fac'].default_value = 0.5
                
                links.new(tex_node.outputs['Color'], mix_node.inputs['Color1'])
                links.new(ao_node.outputs['Color'], mix_node.inputs['Color2'])
                links.new(mix_node.outputs['Color'], bsdf.inputs['Base Color'])
            else:
                links.new(tex_node.outputs['Color'], bsdf.inputs['Base Color'])

        # Handle different roughness/metallic setups
        if has_orm:
            self.setup_orm_workflow(nodes, links, textures, bsdf, layout)
        elif has_separate_metal_rough:
            self.setup_separate_workflow(nodes, links, textures, bsdf, layout)

        # Normal Map
        if "normal" in textures:
            self.setup_normal_map(nodes, links, textures, bsdf, layout, has_height)

        # Displacement chain
        if has_height:
            self.setup_displacement(nodes, links, textures, output_node, layout)

        # Emission
        if "emission" in textures:
            tex_node = self.create_texture_node(nodes, textures["emission"], layout["emission"])
            tex_node.image.colorspace_settings.name = "sRGB"
            links.new(tex_node.outputs['Color'], bsdf.inputs['Emission'])

    def setup_orm_workflow(self, nodes, links, textures, bsdf, layout):
        """Unreal-style ORM workflow"""
        tex_node = self.create_texture_node(nodes, textures["orm"], layout["orm"])
        tex_node.image.colorspace_settings.name = "Non-Color"
        
        separate = nodes.new(type="ShaderNodeSeparateRGB")
        separate.location = layout["orm_separate"]
        links.new(tex_node.outputs['Color'], separate.inputs['Image'])
        
        # R = AO, G = Roughness, B = Metallic
        links.new(separate.outputs['G'], bsdf.inputs['Roughness'])
        links.new(separate.outputs['B'], bsdf.inputs['Metallic'])
        
        # If we have base color, multiply AO from ORM
        if "basecolor" in textures and bsdf.inputs['Base Color'].is_linked:
            mix_node = nodes.new(type='ShaderNodeMixRGB')
            mix_node.location = (layout["mix_ao"][0], layout["mix_ao"][1] - 100)
            mix_node.blend_type = 'MULTIPLY'
            mix_node.inputs['Fac'].default_value = 0.8
            
            # Get existing base color connection
            base_input = bsdf.inputs['Base Color'].links[0].from_socket
            bsdf.inputs['Base Color'].links[0].from_node.links.clear()
            
            links.new(base_input, mix_node.inputs['Color1'])
            links.new(separate.outputs['R'], mix_node.inputs['Color2'])
            links.new(mix_node.outputs['Color'], bsdf.inputs['Base Color'])

    def setup_separate_workflow(self, nodes, links, textures, bsdf, layout):
        """Individual roughness/metallic maps workflow"""
        if "roughness" in textures:
            tex_node = self.create_texture_node(nodes, textures["roughness"], layout["roughness"])
            tex_node.image.colorspace_settings.name = "Non-Color"
            links.new(tex_node.outputs['Color'], bsdf.inputs['Roughness'])
            
        if "metallic" in textures:
            tex_node = self.create_texture_node(nodes, textures["metallic"], layout["metallic"])
            tex_node.image.colorspace_settings.name = "Non-Color"
            links.new(tex_node.outputs['Color'], bsdf.inputs['Metallic'])

    def setup_normal_map(self, nodes, links, textures, bsdf, layout, has_height):
        """Setup normal map with optional height influence"""
        tex_node = self.create_texture_node(nodes, textures["normal"], layout["normal"])
        tex_node.image.colorspace_settings.name = "Non-Color"
        
        if has_height:
            # Combine normal and height for better detail
            height_node = self.create_texture_node(nodes, textures["height"], layout["height"])
            height_node.image.colorspace_settings.name = "Non-Color"
            
            # Convert height to normal
            bump_node = nodes.new(type='ShaderNodeBump')
            bump_node.location = (layout["normal_map"][0], layout["normal_map"][1] - 200)
            bump_node.inputs['Strength'].default_value = 0.1
            links.new(height_node.outputs['Color'], bump_node.inputs['Height'])
            
            # Main normal map
            normal_map = nodes.new(type='ShaderNodeNormalMap')
            normal_map.location = layout["normal_map"]
            links.new(tex_node.outputs['Color'], normal_map.inputs['Color'])
            links.new(bump_node.outputs['Normal'], normal_map.inputs['Normal'])
            links.new(normal_map.outputs['Normal'], bsdf.inputs['Normal'])
        else:
            normal_map = nodes.new(type='ShaderNodeNormalMap')
            normal_map.location = layout["normal_map"]
            links.new(tex_node.outputs['Color'], normal_map.inputs['Color'])
            links.new(normal_map.outputs['Normal'], bsdf.inputs['Normal'])

    def setup_displacement(self, nodes, links, textures, output_node, layout):
        """Setup proper displacement chain"""
        height_tex = None
        for node in nodes:
            if node.type == 'TEX_IMAGE' and node.image and node.image.filepath.endswith(os.path.basename(textures["height"])):
                height_tex = node
                break
        
        if not height_tex:
            height_tex = self.create_texture_node(nodes, textures["height"], layout["height"])
            height_tex.image.colorspace_settings.name = "Non-Color"
        
        # Displacement node
        disp_node = nodes.new(type='ShaderNodeDisplacement')
        disp_node.location = (layout["output"][0] - 200, layout["output"][1] - 200)
        disp_node.inputs['Scale'].default_value = 0.1
        disp_node.inputs['Midlevel'].default_value = 0.5
        
        links.new(height_tex.outputs['Color'], disp_node.inputs['Height'])
        links.new(disp_node.outputs['Displacement'], output_node.inputs['Displacement'])

    def create_texture_node(self, nodes, filepath, location):
        """Helper to create and position texture nodes"""
        image = bpy.data.images.load(filepath)
        tex_node = nodes.new(type='ShaderNodeTexImage')
        tex_node.image = image
        tex_node.location = location
        return tex_node

    def clean_material_name(self, name):
        return name.split(".")[0]


# Add-on registration shit
def register():
    bpy.utils.register_class(DH_OP_BuildShader)

def unregister():
    bpy.utils.unregister_class(DH_OP_BuildShader)

if __name__ == "__main__":
    register()