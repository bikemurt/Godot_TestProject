# Blender Addon
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


