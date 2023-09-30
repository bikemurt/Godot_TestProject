@tool

extends Node

# Called when the node enters the scene tree for the first time.
func _ready():
	if Engine.is_editor_hint():
		applyMaterials(self)
		pass


func applyMaterials(node):
	
	if node is MeshInstance3D:
		var metas = node.get_meta_list()
		for meta in metas:
			if "material" in meta:
				var mtl_name = node.get_meta(meta)
				var surface_split = meta.split("_")
				if len(surface_split) > 0:
					var surface = surface_split[1]
					var material = load("res://Materials/"+mtl_name+".tres")
					#var material = ShaderMaterial.new()
					#material.resource_path = "res://Materials/"+mtl_name+".tres"
					
					var shader = load("res://Shaders/BlendTextures.gdshader")
					#var shader = Shader.new()
					#shader.resource_path = "res://Shaders/BlendMaterial.tres"
					
					material.set_shader(shader)
					
					node.set_surface_override_material(int(surface), material)
					
					#node.set_owner(get_tree().edited_scene_root)

	for child in node.get_children():
		applyMaterials(child)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
