extends Node
class_name Lib

func V3_MIN(vector1: Vector3, vector2: Vector3):
	var result = Vector3(0,0,0)
	result.x = min(vector1.x, vector2.x)
	result.y = min(vector1.y, vector2.y)
	result.z = min(vector1.z, vector2.z)
	return result

func V3_clamp(input: Vector3, min: Vector3, max: Vector3):
	var result = Vector3(0,0,0)
	result.x = clamp(input.x, min.x, max.x)
	result.y = clamp(input.y, min.y, max.y)
	result.z = clamp(input.z, min.z, max.z)
	return result

func V3_clampf(input: Vector3, min: float, max: float):
	var result = Vector3(0,0,0)
	result.x = clamp(input.x, min, max)
	result.y = clamp(input.y, min, max)
	result.z = clamp(input.z, min, max)
	return result
	
func lookup(text_file_contents : String, lookup_key : String):
	var lines = text_file_contents.split("\n")
	
	for line in lines:
		var parts = line.split(",")
		if parts.size() == 2:
			var index = parts[0]
			if index == lookup_key:
				return parts[1].strip_edges()

	return ""

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
