extends CharacterBody3D

@onready var camera_mount = $camera_mount
@onready var animation_player = $visuals/PolyModel2/AnimationPlayer
@onready var visuals = $visuals
@onready var camera_3d = $camera_mount/Camera3D

var SPEED = 2.0
const JUMP_VELOCITY = 4.5

var running = false
var walking_speed = 2.0
var running_speed = 4.0

var rotation_speed = 1.0

@export var sens_horizontal = 0.5
@export var sens_vertical = 0.5

var cam_max = 2.7
var cam_min = 1.7
var cam_lerp_rate = 0.03

# Get the gravity from the project settings to be synced with RigidBody nodes.
var gravity = ProjectSettings.get_setting("physics/3d/default_gravity")

func _ready():
	Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

var input_x = 0
func _input(event):
	if event is InputEventMouseMotion:
		rotate_y(deg_to_rad(-event.relative.x * sens_horizontal))
		
		camera_mount.rotate_x(deg_to_rad(-event.relative.y * sens_vertical))
		
		# capture x rotation for head turning
		input_x = event.relative.x

var anim_rev = false
func switch_anim(name, rev = false, speed = 1.0):
	if animation_player.speed_scale != speed:
		animation_player.speed_scale = speed
	
	if animation_player.current_animation != name or anim_rev != rev:
		print(name)		
		if rev:
			anim_rev = true
			animation_player.play_backwards(name)
		else:
			anim_rev = false
			animation_player.play(name)
	

var input_x_sum = 0
var input_x_count = 0
var turning = 0

var turn_debounce_samples = 0
var turn_retrigger_samples = 0
var head_lerp_to = 0
var head_lerp_from = 0

var jumping = false
var jumping_samples = 0
func _physics_process(delta):
	
	# head turn
	input_x_sum += input_x
	input_x = 0 # clear input from event system
	
	input_x_count += 1
	
	# register head turn
	if input_x_count >= 15:
		if input_x_sum > 50 and turning == 0:
			turning = 1
		
		if input_x_sum <= -50 and turning == 0:
			turning = -1

		input_x_sum = 0
		input_x_count = 0
	
	# head turned registered. clear after 30 frames
	if turning == 1 or turning == -1:
		turn_debounce_samples += 1
		if turn_debounce_samples >= 30:
			
			head_lerp_from = visuals.rotation.y
			head_lerp_to = visuals.rotation.y + deg_to_rad(-45*turning)
		
			turning = -2
			turn_debounce_samples = 0
	
	# prevent re-trigger
	if turning == -2:
		
		turn_retrigger_samples += 1
		
		# update player rotation by fixed animation amount
		visuals.rotation.y = lerp_angle(head_lerp_from, head_lerp_to, 0.1)
		
		if turn_retrigger_samples >= 30:
			turning = 0
			turn_retrigger_samples = 0
	
	# running
	if Input.is_action_pressed("run"):
		running = true
		SPEED = running_speed
	else:
		running = false
		SPEED = walking_speed
	
	# Handle Jump.
	if Input.is_action_pressed("jump") and is_on_floor():
		jumping = true
	
	if jumping:
		jumping_samples += 1
		
		# lift off the ground after 14 frames
		if jumping_samples >= 14 and jumping_samples <= 25:
			velocity.y = JUMP_VELOCITY
		
		if jumping_samples >= 100:
			jumping = false
			jumping_samples = 0
			
	# Add the gravity.
	if not is_on_floor():
		velocity.y -= gravity * delta

	# Get the input direction and handle the movement/deceleration.
	# As good practice, you should replace UI actions with custom gameplay actions.
	var input_dir = Input.get_vector("left", "right", "forward", "backward")
	var direction = (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()
	
	if jumping:
		var jump_rev = false
		#if jumping_samples >= 25:
		#	jump_rev = true
		
		#print(animation_player.current_animation_length)
		#print(jumping)
		#print(jumping_samples)
		switch_anim("Jumping")
	else:
		if direction:
			if running:
				switch_anim("Running")
			else:
				switch_anim("Walking")

			visuals.rotation.y = lerp_angle(visuals.rotation.y, atan2(input_dir.x, input_dir.y), .07)
			
			var cam_lerp = clamp(camera_3d.position.z, cam_min, cam_max)
			camera_3d.position.z = lerp(cam_lerp, cam_max, cam_lerp_rate)
			
			velocity.x = direction.x * SPEED
			velocity.z = direction.z * SPEED
		else:
			if turning == 0 or turning == -2:
				switch_anim("Idle")
			if turning == 1:
				switch_anim("TurnRight", false, 0.5)
			if turning == -1:
				switch_anim("TurnLeft", false, 0.5)

			velocity.x = move_toward(velocity.x, 0, SPEED)
			velocity.z = move_toward(velocity.z, 0, SPEED)
			
			var cam_lerp = clamp(camera_3d.position.z, cam_min, cam_max)
			camera_3d.position.z = lerp(cam_lerp, cam_min, cam_lerp_rate)

	move_and_slide()
