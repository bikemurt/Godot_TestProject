@tool
extends Node3D


# Called when the node enters the scene tree for the first time.
func _ready():
	if Engine.is_editor_hint():
		animTest(self)


func animTest(node):
	var walking = load("res://Characters/AnimationTest/walking.res")
	
	var trackNodePath = NodePath("rig_deform/Skeleton3D:DEF-forearm.L.001")
	
	#print(trackNodePath)
	var trackID = walking.find_track(trackNodePath, Animation.TYPE_ROTATION_3D)
	
	print(walking.track_get_key_count(trackID))
	#print(walking is Animation)
	
	for child in node.get_children():
		if child is AnimationPlayer:
			#print(child.name)
			pass
	pass

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
