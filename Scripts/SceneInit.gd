@tool

extends Node

# Called when the node enters the scene tree for the first time.
func _ready():
	if Engine.is_editor_hint():
		iterateScene(self)


func iterateScene(node):
	
	if node is MeshInstance3D:		
		var mesh_inst : MeshInstance3D = node
		
		var metas = node.get_meta_list()
		for meta in metas:
			var meta_val = node.get_meta(meta)
			if "material" in meta:
				var surface_split = meta.split("_")
				if len(surface_split) > 0:
					var surface = surface_split[1]
					var material = load("res://Materials/"+meta_val+".tres")
					
					var shader = load("res://Shaders/BlendTextures.gdshader")
					material.set_shader(shader)
					
					node.set_surface_override_material(int(surface), material)
			
			if meta == "script":
				print(meta + " " + meta_val)
				node.set_script(load(meta_val))
			
			if meta == "collision":
				if meta_val == "simple":
					mesh_inst.create_convex_collision()
					mesh_inst.set_owner(get_tree().edited_scene_root)
				if meta_val == "trimesh":
					mesh_inst.create_trimesh_collision()
	for child in node.get_children():
		iterateScene(child)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
