bl_info = {
    "name": "Godot Pipeline",
    "blender": (2, 80, 0),
    "category": "Object",
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

class GodotPipelineProperties(PropertyGroup):
    ## COLLISION
    collision_UI : BoolProperty(name = "Collisions", default=False)
    collision_margin : FloatProperty(name = 'Collision Margin', default = 1.03)
    col_types : EnumProperty(
        name =  "Collision",
        items = (
            ("BOX", "Box", ""),
            ("CYLINDER", "Cylinder", ""),
            ("TRIMESH", "Trimesh", ""),
            ("SIMPLE", "Simple", ""),
            ("BODYONLY", "Body Only", ""),
            ("NONE", "None", "")
        ),
        default = "BOX"
    )
    rigid : BoolProperty(name = "Rigid Body", default = False)
    mesh_data : BoolProperty(name = "Apply to Mesh", default = False)
    col_only: BoolProperty(name = "Collision Only", default = False)
    display_wire: BoolProperty(name = "Display Wireframe", default = False)
    
    ## SET PATHS
    path_UI : BoolProperty(name = "Set Scripts, Materials, etc.", default = False)
    set_path : StringProperty(name = "Set Path", default = "")
    path_options : EnumProperty(
        name =  "Path Type",
        items = (
            ("script", "Script", ""),
            ("material_0", "Material 0", ""),
            ("material_1", "Material 1", ""),
            ("material_2", "Material 2", ""),
            ("shader", "Shader", "")
        ),
        default = "script"
    )
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
    use_object_suffix : BoolProperty(name = "Use Object Name Suffix", default = False)
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
        
        ###
        box = layout.box()
        
        row = box.row()
        row.label(text="Global Settings:")
        
        row = box.row()
        row.prop(props, "mesh_data")
        
        row = box.row()
        row.operator("object.clear_all_customs", icon='NONE', text="Clear Custom Data")
            
        ###
        
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
            row.operator("object.select_collisions", icon='NONE', text="Select Collisions")
            
            row = box.row()
            row.prop(props, "rigid")
            
            row = box.row()
            row.prop(props, "col_only")
            
            row = box.row()
            row.prop(props, "display_wire")
            
            row = box.row()
            row.prop(props, "collision_margin")
            
            row = box.row()
            row.operator("object.set_collisions", icon='NONE', text="Set Collisions")
            
            #row = box.row()
            #row.operator("object.reset_origin_bb", icon='NONE', text="Set Origins to Bounding Box")
            
            #box.separator()
            
            #row = box.row()
            #row.operator("object.set_collision_size", icon='NONE', text="Set Collision Sizes")
        
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
            
            row = box.row()
            row.prop(props, "prop_path")
            
            row = box.row()
            row.operator("object.set_script_properties", icon='NONE', text="Set Script Parameters")
        
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
        
class SetCollisions(bpy.types.Operator):
    """Set Collisions"""
    bl_idname = "object.set_collisions"
    bl_label = "Set Collision Type"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        props = scene.GodotPipelineProps

        rigid = ""
        if props.rigid: rigid = "-r"
        
        col_only = ""
        if props.col_only: col_only = "-c"
        
        for obj in context.selected_objects:
            if props.display_wire:
                obj.display_type = "WIRE"
            else:
                obj.display_type = "TEXTURED"
            
            if props.mesh_data: obj = obj.data
            
            if props.col_types == "NONE":
                found = False
                for key, value in obj.items():    
                    if key == "collision":
                        found = True
                
                if found:
                    del obj["collision"]
                
            else:
                obj["collision"] = props.col_types.lower()+rigid+col_only

        ## this is somewhat hacked in here, and could be optimized
        if props.col_types == "BOX" or props.col_types == "CYLINDER":
            bpy.ops.object.reset_origin_bb()
            bpy.ops.object.set_collision_size()

        return {'FINISHED'}

class SelectCollisions(bpy.types.Operator):
    """Select Collisions"""
    bl_idname = "object.select_collisions"
    bl_label = "Set Objects with No Collisions"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        props = scene.GodotPipelineProps
        
        rigid = ""
        if props.rigid: rigid = "-r"
        
        col_only = ""
        if props.col_only: col_only = "-c"
        
        for obj in scene.objects:
            
            if obj.visible_get() == False:
                continue
            
            found = False
            if props.col_types == "NONE":
                
                # only show objects with no collision
                for key, value in obj.items():    
                    if key == "collision":
                        found = True
                
                if not found:
                    obj.select_set(True)
            else:
                for key, value in obj.items():    
                    if key == "collision" and value == props.col_types.lower()+rigid+col_only:
                        found = True
                    
                if found:
                    obj.select_set(True)
                
        return {'FINISHED'}


class SetCollisionSize(bpy.types.Operator):
    """Set Collision Size Script"""
    bl_idname = "object.set_collision_size"
    bl_label = "Set Collision Size"
    bl_options = {'REGISTER', 'UNDO'}

    def set_size(self, obj, dim_obj, margin):
        
        for key, value in obj.items():
            
            value = value.replace("-r", "").replace("-c", "")
            if key == "collision":
                if value == "box":
                    # divide out by scale, because the collision object in godot is parented to the actual mesh,
                    # so it will get the parent's scale (basically we are preventing the scale from being applied twice)
                    obj["size_x"] = str(round(margin * dim_obj.dimensions[0] / dim_obj.scale[0], 4))
                    obj["size_z"] = str(round(margin * dim_obj.dimensions[1] / dim_obj.scale[1], 4))
                    obj["size_y"] = str(round(margin * dim_obj.dimensions[2] / dim_obj.scale[2], 4))
                
                if value == "cylinder":
                    obj["height"] = str(round(margin * obj.dimensions[2] / obj.scale[2], 4))
                    
                    # radius is calculated in x, y plane
                    # take larger value
                    r = 0.5 * dim_obj.dimensions[0] / dim_obj.scale[0]
                    if dim_obj.dimensions[1] > dim_obj.dimensions[0]:
                        r = 0.5 * dim_obj.dimensions[1] / dim_obj.scale[1]
                    
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
            obj["prop_file"] = props.prop_path
        
        return {'FINISHED'}

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
            obj.id_properties_clear()
        
        return {'FINISHED'}

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

classes = [GodotPipelineProperties, GodotPipelinePanel, SelectCollisions,\
    SetCollisions, SetCollisionSize, ResetOriginBB, SetPath, SetMultimesh, ClearAllCustoms, SetScriptProperties, GodotExport]

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