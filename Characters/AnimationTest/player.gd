extends CharacterBody3D

@onready var camera_mount = $camera_mount
@onready var animation_player = $visuals/PolyModel2/AnimationPlayer
@onready var visuals = $visuals
@onready var camera_3d = $camera_mount/Camera3D

const SPEED = 3.0
const JUMP_VELOCITY = 4.5

var rotation_speed = 1.0

@export var sens_horizontal = 0.5
@export var sens_vertical = 0.5

var cam_max = 2.7
var cam_min = 2.023
var cam_lerp_rate = 0.03

# Get the gravity from the project settings to be synced with RigidBody nodes.
var gravity = ProjectSettings.get_setting("physics/3d/default_gravity")

func _ready():
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _input(event):
	if event is InputEventMouseMotion:
		rotate_y(deg_to_rad(-event.relative.x * sens_horizontal))
		camera_mount.rotate_x(deg_to_rad(-event.relative.y * sens_vertical))
		
		#visuals.rotate_y(deg_to_rad(event.relative.x*-0.15))

func _physics_process(delta):
	# Add the gravity.
	if not is_on_floor():
		velocity.y -= gravity * delta

	# Handle Jump.
	if Input.is_action_just_pressed("ui_accept") and is_on_floor():
		velocity.y = JUMP_VELOCITY

	# Get the input direction and handle the movement/deceleration.
	# As good practice, you should replace UI actions with custom gameplay actions.
	var input_dir = Input.get_vector("left", "right", "forward", "backward")
	var direction = (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()
	
	if direction:
		if animation_player.current_animation != "Walking_1":
			animation_player.play("Walking_1")
		
		#visuals.look_at(visuals.position + direction)
		#visuals.rotation.y = lerp_angle(visuals.rotation.y, position.angle_to(position+direction), delta*rotation_speed)
		visuals.rotation.y = lerp_angle(visuals.rotation.y, atan2(input_dir.x, input_dir.y), .1)
		
		var cam_lerp = clamp(camera_3d.position.z, cam_min, cam_max)
		camera_3d.position.z = lerp(cam_lerp, cam_max, cam_lerp_rate)
		
		velocity.x = direction.x * SPEED
		velocity.z = direction.z * SPEED
	else:
		animation_player.play("Idle_1")
		velocity.x = move_toward(velocity.x, 0, SPEED)
		velocity.z = move_toward(velocity.z, 0, SPEED)
		
		var cam_lerp = clamp(camera_3d.position.z, cam_min, cam_max)
		camera_3d.position.z = lerp(cam_lerp, cam_min, cam_lerp_rate)

	move_and_slide()
