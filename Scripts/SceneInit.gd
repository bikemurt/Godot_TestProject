@tool

extends Node

# Called when the node enters the scene tree for the first time.
func _ready():
	if Engine.is_editor_hint():
		if get_meta("run"):
			print("Running scene init")
			iterateScene(self)
			set_meta("run", false)


func setGenericCollision(node):
	var staticbody = StaticBody3D.new()
	staticbody.name = "StaticBody3D"
	node.add_child(staticbody)
	staticbody.set_owner(get_tree().edited_scene_root)
	
	var collision = CollisionShape3D.new()
	collision.name = "CollisionShape3D"
	
	return [staticbody, collision]

func setShape(col, shape):
	col[1].shape = shape
	
	col[0].add_child(col[1])
	col[1].set_owner(get_tree().edited_scene_root)

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
				node.set_script(load(meta_val))
			
			if meta == "collision":
				if meta_val == "simple":
					mesh_inst.create_convex_collision()
					mesh_inst.set_owner(get_tree().edited_scene_root)
				
				if meta_val == "trimesh":
					mesh_inst.create_trimesh_collision()
				
				if meta_val == "cylinder":
					if "height" in metas and "radius" in metas:
						var col = setGenericCollision(node)
						
						var cyl = CylinderShape3D.new()
						
						var height = float(node.get_meta("height"))
						var radius = float(node.get_meta("radius"))
						
						cyl.height = height
						cyl.radius = radius
						
						setShape(col, cyl)
				
				if meta_val == "box":
					if "size_x" in metas and "size_x" in metas \
					and "size_z" in metas:
						var col = setGenericCollision(node)
						
						var box = BoxShape3D.new()
						
						var size_x = float(node.get_meta("size_x"))
						var size_y = float(node.get_meta("size_y"))
						var size_z = float(node.get_meta("size_z"))
						
						box.size = Vector3(size_x, size_y, size_z)
						
						setShape(col, box)
				
			if meta == "state":
				if meta_val == "hide":
					node.hide()
					
			if meta == "multimesh":
				var full_path = node.get_parent().get_name() + "/" + meta_val
				print(full_path)
				
				var source_node = node
				
				var target_node = node.get_parent().get_node(meta_val)
				
				var mm : MultiMesh = MultiMesh.new()
				
				mm.transform_format = MultiMesh.TRANSFORM_3D
				mm.instance_count = 128
				mm.visible_instance_count = -1
				
				mm.mesh = node.mesh
				
				for i in range(mm.instance_count):
					var position = Transform3D()
					position = position.translated(Vector3(randf() * 100 - 50, randf() * 50 - 25, randf() * 50 - 25))
					
					mm.set_instance_transform(i, position)
				
				var mm_inst : MultiMeshInstance3D = MultiMeshInstance3D.new()
				mm_inst.multimesh = mm
				
				node.get_parent().add_child(mm_inst)
				mm_inst.set_owner(get_tree().edited_scene_root)
				
				
	for child in node.get_children():
		iterateScene(child)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
