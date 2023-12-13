extends RigidBody3D

var l = Lib.new()

## START/STOP CONTROL
@export var start = true

## POSITION CONTROL
@export var position_control = false
@export var position_setpoint = Vector3(1, 0, 0)
@export var x_motion_planner : Curve
@export var y_motion_planner : Curve
@export var z_motion_planner : Curve

@export var start_position = Vector3(0,0,0)

## SPEED CONTROL
@export var speed_kp = Vector3(0, 0, 0)
@export var speed_ki = Vector3(0, 0, 0)
@export var speed_setpoint = Vector3(0, 0, 0)

var output_threshold = 0.01

@export var force_limits = 1

func _ready():
	pass

func get_motion_sample(sample):
	var result = Vector3(0,0,0)
	
	if x_motion_planner != null:
		result.x = x_motion_planner.sample(sample.x)
	if y_motion_planner != null:
		result.y = y_motion_planner.sample(sample.y)
	if z_motion_planner != null:
		result.z = z_motion_planner.sample(sample.z)
	
	return result

var speed_control_output = Vector3(0, 0, 0)

var speed_i_term = Vector3(0, 0, 0)
func _process(delta):
	
	if Input.is_action_just_pressed("test"):
		start = not start
	
	var speed_p_term = Vector3(0, 0, 0)
	var speed_setpoint_internal = Vector3(0, 0, 0)
	
	var motion_sample = Vector3(0,0,0)
	
	## POSITION CONTROL
	if position_control:
		
		# only sample motion planner if motion started
		if start:
			var pos_range = position_setpoint - start_position
			
			var percent_of_position = (position - start_position)/pos_range
			var clamp_percent_pos = l.V3_clampf(percent_of_position, 0, 1)
			
			# this is used for speed control
			motion_sample = get_motion_sample(clamp_percent_pos)
		
		# set direction of speed - always go to end point target
		var speed_pos_error = position_setpoint - position
		var speed_dir = Vector3(1, 1, 1)
		if speed_pos_error.x < 0: speed_dir.x = -1
		if speed_pos_error.y < 0: speed_dir.y = -1
		if speed_pos_error.z < 0: speed_dir.z = -1
		
		speed_setpoint_internal = speed_dir * motion_sample * speed_setpoint
	
	else:
		if start:
			speed_setpoint_internal = speed_setpoint
	
	## SPEED CONTROL
	
	var speed_error = speed_setpoint_internal - linear_velocity
	
	speed_p_term = speed_kp * speed_error
	speed_i_term += speed_ki * speed_error * delta
	speed_i_term = l.V3_clampf(speed_i_term, -force_limits, force_limits)
	
	speed_control_output = speed_p_term + speed_i_term
	
	apply_central_impulse(speed_control_output)
