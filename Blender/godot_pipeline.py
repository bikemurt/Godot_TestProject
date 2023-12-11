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
    collision_margin : FloatProperty(
        name = 'Collision Margin',
        default = 1.03
    )
    col_types : EnumProperty(
        name =  "Collision",
        items = (
            ("BOX", "Box", ""),
            ("CYLINDER", "Cylinder", ""),
            ("SKIP", "Skip", ""),
            ("TRIMESH", "Trimesh", ""),
            ("SIMPLE", "Simple", ""),
            ("NONE", "None", "")
        ),
        default = "BOX"
    )
    rigid : BoolProperty(
        name = "Rigid Body",
        default = False
    )
    script_path : StringProperty(
        name = "Script Path",
        default = ""
    )
    mesh_data : BoolProperty(
        name = "Apply to Mesh",
        default = False
    )
    col_only: BoolProperty(
        name = "Collision Only",
        default = False
    )

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
        
        col = layout.column()
        
        ###
        
        row = col.row()
        row.label(text="Collision Selecting and Setting:")
        
        row = col.row()
        row.prop(props, "col_types")
        
        row = col.row()
        row.operator("object.select_collisions", icon='NONE', text="Select Collisions")
        
        row = col.row()
        row.prop(props, "rigid")
        
        row = col.row()
        row.prop(props, "mesh_data")
        
        row = col.row()
        row.prop(props, "col_only")
        
        row = col.row()
        row.operator("object.set_collisions", icon='NONE', text="Set Collisions")
        
        col.separator()
        
        ###
        
        row = col.row()
        row.label(text="Collisions:")
        
        row = col.row()
        row.operator("object.reset_origin_bb", icon='NONE', text="Set Origins to Bounding Box")
        
        col.separator()
        
        row = col.row()
        row.prop(props, "collision_margin")
        
        row = col.row()
        row.operator("object.set_collision_size", icon='NONE', text="Set Collision Sizes")
        
        col.separator()
        
        ###
        
        row = col.row()
        row.label(text="Scripting:")
        
        row = col.row()
        row.prop(props, "script_path")
        
        row = col.row()
        row.operator("object.set_script", icon='NONE', text="Set Script Path")
        
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
                    if key == "collision" and value == props.col_types.lower()+rigid+colonly:
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

class SetScript(bpy.types.Operator):
    """Set Script Path"""
    bl_idname = "object.set_script"
    bl_label = "Set Script Path"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        props = scene.GodotPipelineProps
        
        for obj in context.selected_objects:
            if props.mesh_data: obj = obj.data
            obj["script"] = props.script_path
        
        return {'FINISHED'}

def register():
    
    # props
    bpy.utils.register_class(GodotPipelineProperties)
    bpy.types.Scene.GodotPipelineProps = PointerProperty(type = GodotPipelineProperties)

    # UI
    bpy.utils.register_class(GodotPipelinePanel)

    # functions
    bpy.utils.register_class(SelectCollisions)
    bpy.utils.register_class(SetCollisions)
    bpy.utils.register_class(SetCollisionSize)
    bpy.utils.register_class(ResetOriginBB)
    bpy.utils.register_class(SetScript)

def unregister():
    # props
    bpy.utils.unregister_class(GodotPipelineProperties)
    
    # UI
    bpy.utils.unregister_class(GodotPipelinePanel)
    
    # functions
    bpy.utils.unregister_class(SelectCollisions)
    bpy.utils.unregister_class(SetCollisions)
    bpy.utils.unregister_class(SetCollisionSize)
    bpy.utils.unregister_class(ResetOriginBB)
    bpy.utils.unregister_class(SetScript)


# This allows you to run the script directly from Blender's Text editor
# to test the add-on without having to install it.
if __name__ == "__main__":
    register()