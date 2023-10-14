extends MeshInstance3D

@onready var player = $"../../player"
@onready var door_anim = $"../AnimationPlayer"

var door_unlocked = false
var door_open = false

# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	
	var dist = position.distance_to(player.position)
	
	if Input.is_action_pressed("test"):
		door_unlocked = not door_unlocked
	
	if door_unlocked:
		if dist <= 4 and door_anim.current_animation != "OpenDoor" \
			and not door_open:
			door_anim.play("OpenDoor")
			door_open = true
	
	# door is always able to close
	if dist >= 10 and door_anim.current_animation != "OpenDoor" \
		and door_open:
		door_anim.play_backwards("OpenDoor")
		door_open = false
