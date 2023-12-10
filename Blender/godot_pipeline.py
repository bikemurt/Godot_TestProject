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
    object_selection : EnumProperty(
        name =  "Objects",
        items = (
            ("COL", "Collision Types Set", ""),
            ("SEL", "Selected Objects", "")
        ),
        default = "COL"
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
        row.prop(props, "rigid")
        
        row = col.row()
        row.operator("object.select_collisions", icon='NONE', text="Select Collisions")
        
        row = col.row()
        row.operator("object.set_collisions", icon='NONE', text="Set Collisions")
        
        col.separator()
        
        ###
        
        row = col.row()
        row.label(text="Object Selection:")
        
        row = col.row()
        row.prop(props, "object_selection")
        
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
        
        for obj in context.selected_objects:
            if props.col_types == "NONE":
                found = False
                for key, value in obj.items():    
                    if key == "collision":
                        found = True
                
                if found:
                    del obj["collision"]
                
            else:
                obj["collision"] = props.col_types.lower()+rigid

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
                    if key == "collision" and value == props.col_types.lower()+rigid:
                        found = True
                    
                if found:
                    obj.select_set(True)
                
        return {'FINISHED'}


class SetCollisionSize(bpy.types.Operator):
    """Set Collision Size Script"""
    bl_idname = "object.set_collision_size"
    bl_label = "Set Collision Size"
    bl_options = {'REGISTER', 'UNDO'}

    def set_size(self, obj, margin):
        for key, value in obj.items():    
            if key == "collision":
                
                if value == "box":
                    # divide out by scale, because the collision object in godot is parented to the actual mesh,
                    # so it will get the parent's scale (basically we are preventing the scale from being applied twice)
                    obj["size_x"] = str(round(margin * obj.dimensions[0] / obj.scale[0], 4))
                    obj["size_z"] = str(round(margin * obj.dimensions[1] / obj.scale[1], 4))
                    obj["size_y"] = str(round(margin * obj.dimensions[2] / obj.scale[2], 4))
                
                if value == "cylinder":
                    obj["height"] = str(round(margin * obj.dimensions[2] / obj.scale[2], 4))
                    
                    # radius is calculated in x, y plane
                    # take larger value
                    r = 0.5 * obj.dimensions[0] / obj.scale[0]
                    if obj.dimensions[1] > obj.dimensions[0]:
                        r = 0.5 * obj.dimensions[1] / obj.scale[1]
                    
                    obj["radius"] = str(round(margin * r, 4))
                    

    def execute(self, context):
        scene = context.scene
        props = scene.GodotPipelineProps
        
        margin = props.collision_margin
        
        if props.object_selection == "SEL":
            for obj in context.selected_objects:
                self.set_size(obj, margin)
        
        if props.object_selection == "COL":
            for obj in scene.objects:
                self.set_size(obj, margin)
                
    
        return {'FINISHED'}



class ResetOriginBB(bpy.types.Operator):
    """Reset Origin Bounding Box"""
    bl_idname = "object.reset_origin_bb"
    bl_label = "Reset Origin Bounding Box"
    bl_options = {'REGISTER', 'UNDO'}

    def set_bb(self):
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

    def execute(self, context):
        scene = context.scene
        props = scene.GodotPipelineProps
        
        if props.object_selection == "SEL":
            self.set_bb()
        
        if props.object_selection == "COL":
            for obj in scene.objects:
                for key, value in obj.items():    
                    if key == "collision":
                        obj.select_set(True)
                        self.set_bb()
        
        return {'FINISHED'}

class SetScript(bpy.types.Operator):
    """Set Script Path"""
    bl_idname = "object.set_script"
    bl_label = "Set Script Path"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        props = scene.GodotPipelineProps
        
        
        if props.object_selection == "SEL":
            for obj in context.selected_objects:
                obj["script"] = props.script_path
        
        if props.object_selection == "COL":
            for obj in scene.objects:
                for key, value in obj.items():    
                    if key == "collision":
                        obj["script"] = props.script_path
        
        return {'FINISHED'}

def menu_func1(self, context):
    self.layout.operator(SetCollisionSize.bl_idname)

def menu_func2(self, context):
    self.layout.operator(ResetOriginBB.bl_idname)

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