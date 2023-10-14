extends CharacterBody3D

@onready var camera_mount = $camera_mount
@onready var animation_player = $visuals/PolyModel2/AnimationPlayer
@onready var visuals = $visuals
@onready var camera_3d = $camera_mount/Camera3D

var SPEED = 2.0
const JUMP_VELOCITY = 3.5

var running = false
var walking_speed = 2.0
var running_speed = 4.0

var rotation_speed = 1.0

@export var sens_horizontal = 0.05
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

var anim_blend = 0.2
func switch_anim(name, speed = 1.0, blend = 0.2):
	if animation_player.speed_scale != speed:
		animation_player.speed_scale = speed
		#print("Speed " + str(speed))
	
	if animation_player.current_animation != name or blend != anim_blend:
		#print("Anim " + name)
		animation_player.play(name, blend)
		anim_blend = blend

var input_x_sum = 0
var input_x_count = 0
var input_x_thresh = 100

var turn_debounce_samples = 0
var turn_retrigger_samples = 0
var head_lerp_to = 0
var head_lerp_from = 0

var turning = 0
func registerTurn():
	# head turn
	
	input_x_sum += input_x
	input_x = 0 # clear input from event system
	
	input_x_count += 1
	
	# register head turn
	if input_x_count >= 15:
		if turning == 0:
			# only perform lerp if 90 < visuals y angle < 270
			#if PI/2 < visuals.rotation.y and visuals.rotation.y < 3*PI/2:
			if input_x_sum > input_x_thresh: turning = 1
			if input_x_sum <= -input_x_thresh: turning = -1
			
		input_x_sum = 0
		input_x_count = 0
	
	# clear head turn after 30 frames
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
		if animation_player.current_animation == "Idle":
			visuals.rotation.y = lerp_angle(head_lerp_from, head_lerp_to, 0.3)
		
		# reset head turn
		if turn_retrigger_samples >= 30:
			turning = 0
			turn_retrigger_samples = 0

var jumping = false
var jumping_samples = 0
func _physics_process(delta):
	registerTurn()
	
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
		if jumping_samples >= 23 and jumping_samples <= 35:
			velocity.y = JUMP_VELOCITY
		
		if jumping_samples >= 65:
			jumping = false
			jumping_samples = 0
			
	# Add the gravity.
	if not is_on_floor():
		velocity.y -= gravity * delta

	# Get the input direction and handle the movement/deceleration.
	# As good practice, you should replace UI actions with custom gameplay actions.
	var input_dir = Input.get_vector("left", "right", "forward", "backward")
	var direction = (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()
	
	var cam_zoomout = false
	if jumping:
		cam_zoomout = true
		if jumping_samples <= 25:
			switch_anim("Jumping", 1)
		if jumping_samples >= 50:
			switch_anim("Idle", 1, 0.5)
	else:
		if direction:
			if running:
				switch_anim("Running", 1)
				cam_zoomout = true
			else:
				switch_anim("Walking")

			visuals.rotation.y = lerp_angle(visuals.rotation.y, atan2(input_dir.x, input_dir.y), .07)

			velocity.x = direction.x * SPEED
			velocity.z = direction.z * SPEED
		else:
			if turning == 0 or turning == -2:
				switch_anim("Idle")
			if turning == 1:
				switch_anim("TurnRight", 0.5)
			if turning == -1:
				switch_anim("TurnLeft", 0.5)

			velocity.x = move_toward(velocity.x, 0, SPEED)
			velocity.z = move_toward(velocity.z, 0, SPEED)

	# cam zoom effect
	if cam_zoomout:
		# lerp to cam_max
		var cam_lerp = clamp(camera_3d.position.z, cam_min, cam_max)
		camera_3d.position.z = lerp(cam_lerp, cam_max, cam_lerp_rate)
	else:
		# lerp to cam min
		var cam_lerp = clamp(camera_3d.position.z, cam_min, cam_max)
		camera_3d.position.z = lerp(cam_lerp, cam_min, cam_lerp_rate)
	
	# ensure angle is between 0 and 360 degrees
	#if visuals.rotation.y >= 2*PI: visuals.rotation.y -= 2*PI
	#if visuals.rotation.y <= 0: visuals.rotation.y += 2*PI
	
	move_and_slide()
