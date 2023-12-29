@tool
extends Control

const NODE_3D_VIEWPORT_CLASS_NAME = "Node3DEditorViewport"

var _editor_interface : EditorInterface
var _editor_viewports : Array = []
var _editor_cameras : Array = []

signal mouse_3d

func init(editor_interface : EditorInterface):
	_editor_interface = editor_interface


func _ready():
	_find_viewports(_editor_interface.get_base_control())
	for v in _editor_viewports:
		_find_cameras(v)


func _find_viewports(n : Node):
	if n.get_class() == NODE_3D_VIEWPORT_CLASS_NAME:
		_editor_viewports.append(n)
	
	for c in n.get_children():
		_find_viewports(c)


func _find_cameras(n : Node):
	if n is Camera3D:
		_editor_cameras.append(n)
		return
	
	for c in n.get_children():
		_find_cameras(c)

func _input(event):
		
	if event is InputEventMouseButton:
		if event.pressed and event.button_index == 1:
			var selection = _editor_interface.get_selection()
			# only ever work with 1st node
			var node = selection.get_selected_nodes()[0]
			if node is Node3D:
				var camera = _editor_cameras[0]
				
				var offset = _editor_interface.get_editor_main_screen().global_position
				# the 30 is a magical offset number
				offset.y += 30
				#print(offset)
				var mouse_coords = event.position - offset
				var from = camera.project_ray_origin(mouse_coords)
				var to = from + camera.project_ray_normal(mouse_coords) * 1_000
				
				mouse_3d.emit(from, to, node)

func _on_button_pressed():
	if len(_editor_cameras) > 0:
		print(_editor_cameras[0].position)
