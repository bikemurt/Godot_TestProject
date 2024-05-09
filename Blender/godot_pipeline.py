bl_info = {
    "name": "Godot Pipeline",
    "description": "A 3D pipeline for exporting from Blender and importing into Godot 4+.",
    "author": "Michael Jared",
    "version": (2,0),
    "location": "View3D > Properties > Godot Pipeline",
    "doc_url": "https://www.michaeljared.ca",
    "blender": (2, 80, 0),
    "category": "Object"
}

import bpy, math

from bpy.types import (
            Operator, 
            PropertyGroup, 
            Panel
        )
from bpy.props import (
            IntProperty,
            EnumProperty,
            BoolProperty,
            FloatProperty,
            StringProperty,
            PointerProperty,
            CollectionProperty
        )

# this is a full list of pipeline customs - helps with displaying and clearing data
custom_list = ["collision", "size_x", "size_y", "size_z", "height", "radius", "script",\
    "material_0", "material_1", "material_2", "material_3", "shader", "nav_mesh", "multimesh",\
    "prop_file", "name_override", "physics_mat"]

class GodotPipelineProperties(PropertyGroup):
    ## GLOBAL
    global_UI : BoolProperty(name = "Global Settings", default = False)
    mesh_data : BoolProperty(name = "Assign to Mesh instead of Object", default = False)
    object_name : StringProperty(name = "Name Override", default = "")
    
    ## COLLISION
    collision_UI : BoolProperty(name = "Collisions", default=False)
    collision_margin : FloatProperty(name = 'Collision Margin', default = 1.00)
    col_types : EnumProperty(
        name =  "Collision",
        items = (
            ("BOX", "Box", ""),
            ("CYLINDER", "Cylinder", ""),
            ("SPHERE", "Sphere", ""),
            ("TRIMESH", "Trimesh", ""),
            ("SIMPLE", "Simple", ""),
            ("BODYONLY", "None", "")
        ),
        default = "BOX"
    )
    body_types : EnumProperty(
        name = "Body",
        items = (
            ("STATIC", "Static Body", ""),
            ("RIGID", "Rigid Body", ""),
            ("AREA", "Area 3D", ""),
            ("COLONLY", "None", "")
        ),
        default = "STATIC"
    )
    display_wire: BoolProperty(name = "Display Wireframe", default = False)
    discard_mesh: BoolProperty(name = "Discard Mesh", default = False)
    
    ## SET PATHS
    path_UI : BoolProperty(name = "Path Setter", default = False)
    set_path : StringProperty(name = "Set Path", default = "")
    path_options : EnumProperty(
        name =  "Path Type",
        items = (
            ("script", "Script", ""),
            ("material_0", "Material 0", ""),
            ("material_1", "Material 1", ""),
            ("material_2", "Material 2", ""),
            ("material_3", "Material 3", ""),
            ("shader", "Shader", ""),
            ("nav_mesh", "Nav Mesh", ""),
            ("multimesh", "Multimesh", ""),
            ("physics_mat", "Physics Material", "")
        ),
        default = "script"
    )
    
    # SCRIPT PARAM UI
    script_param_UI : BoolProperty(name = "Script Parameters", default = False)
    prop_path : StringProperty(name = "Param File", default = "")
    
    ## Multimesh
    multimesh_UI : BoolProperty(name = "Multimesh", default = False)
    multimesh_UI_dynamic_inst : BoolProperty(name = "Dynamic Instancing", default = False)
    occlusion_culling : BoolProperty(name = "Occlusion Culling", default = False)
    camera_node_path : StringProperty(name = "Camera Node", default = "")
    dynamic_script : StringProperty(name = "Script", default = "")
    vertex_painter : BoolProperty(name = "Vertex Painter Addon", default = False)
    
    # SAVE
    export_UI : BoolProperty(name = "Export", default = False)
    use_object_suffix : BoolProperty(name = "Append '_ObjectName.gltf' to Filename", default = False)
    save_path : StringProperty(name = "", description = "Select file", default="", maxlen=1024, subtype='FILE_PATH')

class GodotPipelinePanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_godot_pipeline"
    bl_label = "Godot Pipeline"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = "objectmode"
    bl_category = "Godot Pipeline"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.GodotPipelineProps
        obj = context.object
        
        # GLOBAL SETTINGS
        box = layout.box()
        
        row = box.row()
        
        row.prop(props, "global_UI",
            icon="TRIA_DOWN" if props.global_UI else "TRIA_RIGHT",
            icon_only=False, emboss=False
        )
        
        if props.global_UI:
            row = box.row()
            row.prop(props, "mesh_data")
        
            row = box.split(factor=0.4)
            row.label(text='Name Override:')
            row.prop(props, "object_name", text='')
            
            row = box.row()
            row.operator("object.name_override", icon='NONE', text="Apply Name Override")
            
            row = box.row()
            row.operator("object.show_all_customs", icon='NONE', text="Display Addon Data")
            
            row = box.row()
            row.operator("object.clear_all_customs", icon='NONE', text="Clear Addon Data")
            
        # COLLISIONS
        box = layout.box()
        
        row = box.row()
        
        row.prop(props, "collision_UI",
            icon="TRIA_DOWN" if props.collision_UI else "TRIA_RIGHT",
            icon_only=False, emboss=False
        )
        
        if props.collision_UI:
            row = box.row()
            
            row = box.row()
            row.prop(props, "col_types")
            
            row = box.row()
            row.prop(props, "body_types")
            
            row = box.row()
            row.prop(props, "display_wire")
            
            row = box.row()
            row.prop(props, "discard_mesh")
            
            row = box.row()
            row.prop(props, "collision_margin")
            
            row = box.row()
            row.operator("object.set_collisions", icon='NONE', text="Set Collisions")
            
        
        # PATH SETTER
        box = layout.box()
        
        row = box.row()
        row.prop(props, "path_UI",
            icon="TRIA_DOWN" if props.path_UI else "TRIA_RIGHT",
            icon_only=False, emboss=False
        )
        
        if props.path_UI:
            row = box.row()
            row.prop(props, "set_path")
            
            row = box.row()
            row.prop(props, "path_options")
            
            row = box.row()
            row.operator("object.set_path", icon='NONE', text="Set Path")
            
        
        # SCRIPT PARAMS
        box = layout.box()
        
        row = box.row()
        row.prop(props, "script_param_UI",
            icon="TRIA_DOWN" if props.script_param_UI else "TRIA_RIGHT",
            icon_only=False, emboss=False
        )
        
        if props.script_param_UI:
            row = box.row()
            row.prop(props, "prop_path")
            
            row = box.row()
            row.operator("object.set_script_properties", icon='NONE', text="Set Script Parameters")
        
        
        # LEGACY MULTIMESH
        if False:
            box = layout.box()
            
            row = box.row()
            row.prop(props, "multimesh_UI",
                icon="TRIA_DOWN" if props.multimesh_UI else "TRIA_RIGHT",
                icon_only=False, emboss=False
            )
            
            if props.multimesh_UI:
                row = box.row()
                row.prop_search(context.scene, "target", context.scene, "objects", text="Mesh")

                row = box.row()
                row.prop(props, "occlusion_culling")
                
                row = box.row()
                row.prop(props, "multimesh_UI_dynamic_inst")
                
                if props.multimesh_UI_dynamic_inst:
                    row = box.split(factor=0.4)
                    row.label(text='Camera Node:')
                    row.prop(props, "camera_node_path", text='')
                
                if props.multimesh_UI_dynamic_inst:
                    row = box.row()
                    row.prop(props, "dynamic_script")
                
                row = box.row()
                row.prop(props, "vertex_painter")
                
                row = box.row()
                row.operator("object.set_multimesh", icon='NONE', text="Set Multimesh")
        
        # EXPORT
        box = layout.box()
        
        row = box.row()
        row.prop(props, "export_UI",
            icon="TRIA_DOWN" if props.multimesh_UI else "TRIA_RIGHT",
            icon_only=False, emboss=False
        )
        
        if props.export_UI:
            row = box.row()
            row.prop(props, "save_path")
            
            row = box.row()
            row.prop(props, "use_object_suffix")
            
            row = box.row()
            row.operator("object.godot_export", icon='NONE', text="Export for Godot")
        ###


### CORE ADDON CLASSES

class SetCollisions(bpy.types.Operator):
    """Set Collisions"""
    bl_idname = "object.set_collisions"
    bl_label = "Set Collision Type"
    bl_options = {'REGISTER', 'UNDO'}
    
    clear_fields = ["radius", "height", "size_x", "size_y", "size_z"]
    shape_fields = ["BOX", "CYLINDER", "SPHERE"]

    def execute(self, context):
        scene = context.scene
        props = scene.GodotPipelineProps
        
        
        # compose collision string
        
        col_string = props.col_types.lower()
        if props.col_types == "BODYONLY":
            col_string = "bodyonly"
        if props.body_types == "STATIC":
            col_string += ""
        if props.body_types == "RIGID":
            col_string += "-r"
        if props.body_types == "AREA":
            col_string += "-a"
        if props.body_types == "COLONLY":
            col_string += "-c"
        
        if props.discard_mesh:
            col_string += "-d"
        
        for obj in context.selected_objects:
            if props.display_wire:
                obj.display_type = "WIRE"
            else:
                obj.display_type = "TEXTURED"
            
            # apply data to mesh, not object
            if props.mesh_data: obj = obj.data
            
            if props.object_name != "":
                obj["name_override"] = props.object_name
            
            obj["collision"] = col_string

            # clear existing fields
            for field in self.clear_fields:
                if field in obj:
                    del obj[field]
            
        # reset origin to bounding box and set collision sizes
        if props.col_types in self.shape_fields:
            bpy.ops.object.reset_origin_bb()
            bpy.ops.object.set_collision_size()

        return {'FINISHED'}

class SetCollisionSize(bpy.types.Operator):
    """Set Collision Size Script"""
    bl_idname = "object.set_collision_size"
    bl_label = "Set Collision Size"
    bl_options = {'REGISTER', 'UNDO'}

    def set_size(self, obj, dim_obj, margin):
        _items = obj.items()
        for key, value in _items:
            if key == "collision":
                
                # clear all flags to check collision shape
                value = value.replace("-r", "").replace("-c", "").replace("-a", "").replace("-d", "")
                if value == "box":
                    # divide out by scale, because the collision object in godot is parented to the actual mesh,
                    # so it will get the parent's scale (basically we are preventing the scale from being applied twice)
                    obj["size_x"] = str(round(margin * dim_obj.dimensions[0] / dim_obj.scale[0], 4))
                    obj["size_z"] = str(round(margin * dim_obj.dimensions[1] / dim_obj.scale[1], 4))
                    obj["size_y"] = str(round(margin * dim_obj.dimensions[2] / dim_obj.scale[2], 4))
                
                if value == "cylinder":
                    obj["height"] = str(round(margin * dim_obj.dimensions[2] / dim_obj.scale[2], 4))
                    
                    # radius is calculated in x, y plane
                    # take larger value
                    r = 0.5 * dim_obj.dimensions[0] / dim_obj.scale[0]
                    if dim_obj.dimensions[1] > dim_obj.dimensions[0]:
                        r = 0.5 * dim_obj.dimensions[1] / dim_obj.scale[1]
                    
                    obj["radius"] = str(round(margin * r, 4))
                
                if value == "sphere":
                    # radius is taken to be largest of x,y,z side lengths
                    r = 0.5 * dim_obj.dimensions[0] / dim_obj.scale[0]
                    
                    if dim_obj.dimensions[1] > dim_obj.dimensions[0]:
                        r = 0.5 * dim_obj.dimensions[1] / dim_obj.scale[1]
                        
                    if dim_obj.dimensions[2] > dim_obj.dimensions[0]:
                        r = 0.5 * dim_obj.dimensions[2] / dim_obj.scale[2]
                    
                    obj["radius"] = str(round(margin * r, 4))
                    
                    

    def execute(self, context):
        scene = context.scene
        props = scene.GodotPipelineProps
        
        margin = props.collision_margin
        
        for obj in context.selected_objects:
            dim_obj = obj
            if props.mesh_data: obj = obj.data
            self.set_size(obj, dim_obj, margin)
        
        return {'FINISHED'}

class ResetOriginBB(bpy.types.Operator):
    """Reset Origin Bounding Box"""
    bl_idname = "object.reset_origin_bb"
    bl_label = "Reset Origin Bounding Box"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        props = scene.GodotPipelineProps
        
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        
        return {'FINISHED'}


class SetPath(bpy.types.Operator):
    """Set Path"""
    bl_idname = "object.set_path"
    bl_label = "Set Path"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        props = scene.GodotPipelineProps
        
        for obj in context.selected_objects:
            if props.mesh_data: obj = obj.data
            if props.object_name != "":
                obj["name_override"] = props.object_name
            
            obj[props.path_options] = props.set_path
        
        return {'FINISHED'}

class SetScriptProperties(bpy.types.Operator):
    """Set Script Properties"""
    bl_idname = "object.set_script_properties"
    bl_label = "Set Script Properties"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        props = scene.GodotPipelineProps
        
        for obj in context.selected_objects:
            if props.mesh_data: obj = obj.data
            if props.object_name != "":
                obj["name_override"] = props.object_name
            
            obj["prop_file"] = props.prop_path
        
        return {'FINISHED'}


# LEGACY???
class SetMultimesh(bpy.types.Operator):
    """Set Multimesh"""
    bl_idname = "object.set_multimesh"
    bl_label = "Set Multimesh"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        props = scene.GodotPipelineProps

        # this is not necessarily a good idea since script "prop file" could be set
        #bpy.ops.object.clear_all_customs()

        for obj in context.selected_objects:
            obj.display_type = "BOUNDS"
            bpy.ops.object.reset_origin_bb()
            obj["size_x"] = str(round(obj.dimensions[0] / obj.scale[0], 4))
            obj["size_z"] = str(round(obj.dimensions[1] / obj.scale[1], 4))
            obj["size_y"] = str(round(obj.dimensions[2] / obj.scale[2], 4))
            obj["multimesh_target"] = scene.target.name
            obj.data.materials.clear()
            
            if props.occlusion_culling:
                obj["occlusion_culling"] = "true"
            
            if props.multimesh_UI_dynamic_inst:
                if props.camera_node_path != "":
                    obj["camera_node"] = props.camera_node_path
                    obj["dynamic_script"] = props.dynamic_script
            
            if props.vertex_painter:
                obj["group"] = "vertex_painter"

        return {'FINISHED'}

class ClearAllCustoms(bpy.types.Operator):
    """Clear All Customs"""
    bl_idname = "object.clear_all_customs"
    bl_label = "Clear All Customs"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        props = scene.GodotPipelineProps
        
        for obj in context.selected_objects:
            if props.mesh_data: obj = obj.data
            
            clear_list = []
            for key, value in obj.items():
                if key in custom_list:
                    clear_list.append(key)
            
            for key in clear_list:
                del obj[key]
                    
            #obj.id_properties_clear()
        
        return {'FINISHED'}


class NameOverride(bpy.types.Operator):
    """Name Override"""
    bl_idname = "object.name_override"
    bl_label = "Name Override"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        props = scene.GodotPipelineProps
        
        for obj in context.selected_objects:
            if props.mesh_data: obj = obj.data
            if props.object_name != "":
                obj["name_override"] = props.object_name
            else:
                if "name_override" in obj:
                    del obj["name_override"]
            
            props.object_name = ""
        
        return {'FINISHED'}


# EXPORT
class GodotExport(bpy.types.Operator):
    """Godot Export"""
    bl_idname = "object.godot_export"
    bl_label = "Godot Export"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scene = context.scene
        props = scene.GodotPipelineProps
        
        temp_save_path = props.save_path
        
        if props.use_object_suffix and context.active_object:
            temp_save_path = temp_save_path.replace(".gltf", "_" + context.active_object.name + ".gltf")
        
        bpy.ops.export_scene.gltf(filepath=bpy.path.abspath(temp_save_path), export_format='GLTF_SEPARATE', export_extras=True, use_visible=True, export_apply=True)
        return {'FINISHED'}
    
### INFO

class ShowAllCustoms(bpy.types.Operator):
    """Show All Customs"""
    bl_idname = "object.show_all_customs"
    bl_label = "Show All Customs"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        props = scene.GodotPipelineProps
        
        obj = context.active_object
        
        obj_str = "Assigned to OBJECT"
        if props.mesh_data: obj_str = "Assigned to MESH"
        
        ShowCustoms(obj, obj.name + " Customs ("+obj_str+")")
        
        return {'FINISHED'}

def ShowCustoms(obj, title = "Message Box", icon = 'INFO'):

    def draw(self, context):
        scene = context.scene
        props = scene.GodotPipelineProps
        
        objx = obj
        if props.mesh_data: objx = obj.data
        
        for key, value in objx.items():
            if key in custom_list:
                self.layout.label(text=str(key)+"="+str(value))

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

###

classes = [GodotPipelineProperties, GodotPipelinePanel,\
    SetCollisions, SetCollisionSize, ResetOriginBB, SetPath, SetMultimesh, ClearAllCustoms, SetScriptProperties,\
    ShowAllCustoms, NameOverride, \
    GodotExport]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.target = bpy.props.PointerProperty(type=bpy.types.Object)    
    bpy.types.Scene.GodotPipelineProps = PointerProperty(type = GodotPipelineProperties)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()