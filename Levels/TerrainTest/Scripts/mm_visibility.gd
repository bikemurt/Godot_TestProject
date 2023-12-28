extends Node

@export var target_path = ""
@export var multimesh_path = ""
@export var distance_fade_start = 100
@export var distance_fade_end = 200

var multimesh_node : MultiMeshInstance3D
var target_node : Node3D
func _ready():
	target_node = get_node(target_path)
	multimesh_node = get_node(multimesh_path)
	pass # Replace with function body.

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	
	var distance = (multimesh_node.position - target_node.position).length()
	
	var percent_dist = (distance - distance_fade_start)/(distance_fade_end - distance_fade_start)
	percent_dist = clampf(percent_dist, 0, 1)
	
	var multimesh = multimesh_node.multimesh

	multimesh.visible_instance_count = (1 - percent_dist) * multimesh.instance_count
