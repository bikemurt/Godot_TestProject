extends RigidBody3D

# Get the gravity from the project settings to be synced with RigidBody nodes.
var gravity = ProjectSettings.get_setting("physics/3d/default_gravity")

var collision_pos : Vector3 = Vector3(0, 0, 0)
func _integrate_forces(state):
	if state.get_contact_count() > 0 :
		collision_pos = to_local(state.get_contact_local_position(0))


# Called when the node enters the scene tree for the first time.
func _ready():
	pass # Replace with function body.

func _physics_process(delta):
	if Input.is_action_pressed("test"):
		#apply_impulse(Vector3(1, 0, 0), Vector3(0, 0, 0))
		apply_central_force(Vector3(1, 0, 0))
	
	

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass


func _on_body_entered(body):
	print(collision_pos)
	print(to_global(collision_pos))
	
	if body is CharacterBody3D:
		if body.name == "player2":
			#apply_central_impulse(collision_pos * 10))
			print(body)
		
	pass # Replace with function body.
