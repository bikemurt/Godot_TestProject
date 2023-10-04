@tool
extends Node3D

var some_data = RefCountedExt.new()

# Called when the node enters the scene tree for the first time.
func _ready():
	some_data.data = "test2"
	print(some_data.data)


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
	
