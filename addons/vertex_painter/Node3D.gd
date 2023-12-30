@tool
extends Node3D


@onready var _space: PhysicsDirectSpaceState3D = get_world_3d().direct_space_state

var _mesh_data_array := {}

signal update_color
signal update_colors

# Called when the node enters the scene tree for the first time.
func _ready():
	get_parent().connect("mouse_3d", calc_hit)
	get_parent().connect("delete_debug_mesh", delete_debug_mesh)
	get_parent().connect("lock", lock)

func lock(node, state):
	for child in node.get_children():
		if child is Node3D:
			if state == false:
				state = null
			child.set_meta("_edit_lock_", state)
			#child.set_owner(get_tree().get_edited_scene_root())
		
		print(child)
		print(child.get_meta("_edit_lock_"))
		lock(child, state)

var m : MeshInstance3D = null
func calc_hit(from, to, active_node: Node3D, n=1, debug=false):
	var ray := PhysicsRayQueryParameters3D.create(
		from, to, 0x1)
	
	var hit := _space.intersect_ray(ray)
	if hit.is_empty(): return
	
	var mesh_i := _find_mesh(hit.collider)
	mesh_i.set_owner(get_tree().edited_scene_root)
	
	var mesh_id := mesh_i.get_instance_id()
	if not _mesh_data_array.has(mesh_id):
		var mdt := MeshDataTool.new()
		mdt.create_from_surface(mesh_i.mesh, 0)
		_mesh_data_array[mesh_id] = mdt
	
	var m_origin = mesh_i.global_transform.origin
	#var idx = _get_closest_vertex(_mesh_data_array[mesh_id], m_origin, hit.position)
	
	var mdt = _mesh_data_array[mesh_id]
	#update_color.emit(mdt, idx, mesh_i)
	
	var idxs = _get_n_closest_vertices(mdt, m_origin, hit.position, n)
	update_colors.emit(mdt, idxs, mesh_i)
	
	if debug:
		if m == null:
			m = MeshInstance3D.new()
			m.name = "DebugMesh"
			m.mesh = BoxMesh.new()
			active_node.get_parent().add_child(m)
			m.set_owner(get_tree().edited_scene_root)
			
		m.position = hit.position

func _find_mesh(node: Node) -> MeshInstance3D:
	var p := node.get_parent()
	if p == null: return p
	return p if p is MeshInstance3D else _find_mesh(p)

func _get_closest_vertex(mdt: MeshDataTool, mesh_pos: Vector3, hit_pos: Vector3) -> int:
	var closest_dist := INF
	var closest_vertex := -1

	for v in range(mdt.get_vertex_count()):
		var v_pos := mdt.get_vertex(v) + mesh_pos
		var tmp := hit_pos.distance_squared_to(v_pos)
		if tmp <= closest_dist:
			closest_dist = tmp
			closest_vertex = v

	return closest_vertex

func _get_n_closest_vertices(mdt: MeshDataTool, mesh_pos: Vector3, hit_pos: Vector3, n: int):
	var vertices = []
	for v in range(mdt.get_vertex_count()):
		var v_pos := mdt.get_vertex(v) + mesh_pos
		var dist = hit_pos.distance_squared_to(v_pos)
		
		if len(vertices) < n:
			# original fill of the 5 closest
			vertices.append([v, dist])
		else:
			# update array indices
			var changes = []
			var furthest_dist = 0
			var furthest_index = -1
			for index in range(len(vertices)):
				var vertex = vertices[index]
				var dist_2 = vertex[1]
				
				if dist_2 > furthest_dist:
					furthest_dist = dist_2
					furthest_index = index
			
			# if it's not the largest, then kick the
			# largest out
			if dist < furthest_dist:
				vertices[furthest_index] = [v, dist]
	
	# get indices
	var v_indices = []
	for vertex in vertices:
		v_indices.append(vertex[0])
	return v_indices
	
func delete_debug_mesh():
	if m != null:
		m.get_parent().remove_child(m)
		
		m = null

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
