extends Node3D


# Called when the node enters the scene tree for the first time.
func _ready():
	
	for child in self.get_children():
		if child.name == "AnimationPlayer":
			child.play("Walking_1")
	
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
