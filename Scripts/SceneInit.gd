@tool

extends Node

var reparent_nodes = []
var delete_nodes = []

# Called when the node enters the scene tree for the first time.
func _ready():
	if Engine.is_editor_hint():
		if get_meta("run"):
			print("Running scene init")
			iterate_scene(self)
			
			reparent_pass()
			delete_pass()
			
			set_meta("run", false)

func reparent_pass():
	for node in reparent_nodes:
		node[0].reparent(node[1], true)
		node[0].set_owner(get_tree().edited_scene_root)
		
		set_children_scene_root(node[0])
		
func delete_pass():
	for node in delete_nodes:
		node.queue_free()

func set_children_scene_root(node):
	for child in node.get_children():
		set_children_scene_root(child)
		child.set_owner(get_tree().edited_scene_root)

func set_generic_collision(node : Node3D, rigid_body=false, collision_only=false):
	
	var collision = CollisionShape3D.new()
	collision.name = node.name + "_CollisionShape3D"
	
	if collision_only:
		reparent_nodes.append([collision, node.get_parent()])
		delete_nodes.append(node)
		return [node, collision]
	
	else:
		var body = StaticBody3D.new()
		body.name = node.name + "_StaticBody3D"
	
		if rigid_body:
			body = RigidBody3D.new()
			body.name = node.name + "_RigidBody3D"
			#body.transform = node.transform
			
			reparent_nodes.append([node, body])
			
			node.get_parent().add_child(body)
		else:
			node.add_child(body)
	
		body.set_owner(get_tree().edited_scene_root)
		
		return [body, collision]	

func set_shape(col, shape):
	col[1].shape = shape
	
	col[0].add_child(col[1])
	col[1].set_owner(get_tree().edited_scene_root)

func iterate_scene(node):
	
	if node is MeshInstance3D:		
		var mesh_inst : MeshInstance3D = node
		
		var metas = node.get_meta_list()
		for meta in metas:
			
			var meta_val = node.get_meta(meta)
			if "material" in meta:
				var surface_split = meta.split("_")
				if len(surface_split) > 0:
					var surface = surface_split[1]
					var material = load(meta_val)
					
					var shader = load(node.get_meta("shader"))
					material.set_shader(shader)
					
					node.set_surface_override_material(int(surface), material)
			
			if meta == "script":
				node.set_script(load(meta_val))
			
			if meta == "collision":
				var rigid_body = false
				var col_only = false
				
				if "-r" in meta_val:
					rigid_body = true
					meta_val = meta_val.replace("-r", "")
				
				if "-c" in meta_val:
					col_only = true
					meta_val = meta_val.replace("-c", "")
					
				if meta_val == "simple":
					mesh_inst.create_convex_collision()
					mesh_inst.set_owner(get_tree().edited_scene_root)
					
					if rigid_body:
						var body = RigidBody3D.new()
						body.name = node.name + "_RigidBody3D"
						#body.transform = node.transform
												
						var col = node.get_children()[0].get_children()[0]
						reparent_nodes.append([col, body])
						
						reparent_nodes.append([node, body])
						
						delete_nodes.append(node.get_children()[0])
						
						node.get_parent().add_child(body)
						body.set_owner(get_tree().edited_scene_root)
				
				if meta_val == "trimesh":
					mesh_inst.create_trimesh_collision()
				
				if meta_val == "cylinder":
					if "height" in metas and "radius" in metas:
						var col = set_generic_collision(node)
						
						var cyl = CylinderShape3D.new()
						
						var height = float(node.get_meta("height"))
						var radius = float(node.get_meta("radius"))
						
						cyl.height = height
						cyl.radius = radius
						
						set_shape(col, cyl)
				
				if meta_val == "box":
					if "size_x" in metas and "size_x" in metas \
					and "size_z" in metas:
						var col = set_generic_collision(node, rigid_body, col_only)
						
						var box = BoxShape3D.new()
						
						var size_x = float(node.get_meta("size_x"))
						var size_y = float(node.get_meta("size_y"))
						var size_z = float(node.get_meta("size_z"))
						
						box.size = Vector3(size_x, size_y, size_z)
						
						set_shape(col, box)
				
			if meta == "state":
				if meta_val == "hide":
					node.hide()
					
			if meta == "multimesh":
				var full_path = node.get_parent().get_name() + "/" + meta_val
				
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
		iterate_scene(child)

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
