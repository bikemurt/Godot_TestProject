@tool
extends Node3D


@onready var _space: PhysicsDirectSpaceState3D = get_world_3d().direct_space_state

# Called when the node enters the scene tree for the first time.
func _ready():
	get_parent().connect("mouse_3d", calc_hit)
	pass # Replace with function body.

var m = null
func calc_hit(from, to, active_node: Node3D):
	var ray := PhysicsRayQueryParameters3D.create(
		from, to, 0x1)
	
	var hit := _space.intersect_ray(ray)
	
	if m == null:
		m = MeshInstance3D.new()
		m.name = "DebugMesh"
		m.mesh = BoxMesh.new()
		active_node.get_parent().add_child(m)
		
	m.position = hit.position
	
	m.set_owner(get_tree().edited_scene_root)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
