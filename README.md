# Godot 4 Pipeline Blender Addon
I think the most useful thing in this repo right now is the Blender add-on that I'm developing - it's a Godot GLTF Import pipeline.

You can download the add-on here:
- https://github.com/bikemurt/Godot_TestProject/blob/main/Blender/godot_pipeline.py

It works with two Godot scripts in this project:
- A [GLTF import](https://github.com/bikemurt/Godot_TestProject/blob/main/Scripts/GLTFImporter.gd) script which is meant to be attached to your GLTF file
- A [Scene Init](https://github.com/bikemurt/Godot_TestProject/blob/main/Scripts/SceneInit.gd) script which automatically gets attached to your scene when the GLTF import script is ran

## How to Use
Install the blender add-on as per usual: Edit -> Preferences -> Add-ons -> Install.

After installation, you can hit the N-key in object mode to see the new panel:

![Godot Pipeline Panel](https://github.com/bikemurt/Godot_TestProject/assets/23486102/57042c3f-4112-4bd9-bf44-fd89665b39ed)

The add-on modifies the Custom properties of the object:

![Custom Properties](https://github.com/bikemurt/Godot_TestProject/assets/23486102/3de54906-eaa0-46ee-9045-47a329309f7f)

When imported, these get attached as "Metas" in the Godot object. The GLTF script parses the GLTF file and adds the metas, then the Scene Init script does various actions with those metas.

## Blender Add-on functions
- Select and Set Collisions: the main purpose of this is to set the "collision" custom property of many objects at once. You can use the "select" option to see which objects don't have collisions applied. Everything should get a collision, even if it is set to "Skip". Use the "None" option to select all remaining objects with no collisions
- 
  ![image](https://github.com/bikemurt/Godot_TestProject/assets/23486102/66541e81-78bb-40ed-9c45-6b9bfc9acba6)

- Object Selection - the most useful setting for this right now is "Select Objects", since you can select which collisions you want from the previous step. "Collision Types Set" will apply the operation to every object that has a "collision" key (something you might not want to do)
- Set Origins to Bounding Box - this step needs to be done prior to setting collision sizes as it places the collision object at the exact center of the object
- Set Collision Sizes - this calculates the size of the collision object, when PARENTED to the main mesh


## GLTF/Scene Init functions
- GLTF sets metas on objects in Godot equal to the custom properties defined in Blender. If custom properties are set on the mesh in Blender, then it will be applied to each object that uses that mesh data
- Scene init:
- -  "collision" - Set various collision types as defined above from the blender add-on
-   "material" - right now this is a custom function for my project (a custom blend shader which uses two PBR materials)
-   "script" - attaches a Godot script based on the script file path set in Blender
