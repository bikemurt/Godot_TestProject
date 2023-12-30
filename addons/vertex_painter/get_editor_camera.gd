@tool
extends Control

const NODE_3D_VIEWPORT_CLASS_NAME = "Node3DEditorViewport"

var _editor_interface : EditorInterface
var _editor_viewports : Array = []
var _editor_cameras : Array = []

signal mouse_3d
signal delete_debug_mesh
signal lock

var debug_mesh := false
var color_vals := {
	"Red": 1.0,
	"Green": 1.0,
	"Blue": 1.0
}
var _enable_painting := false
var _brush_size : int = 5

var last_position := Vector2(0,0)
func init(editor_interface : EditorInterface):
	_editor_interface = editor_interface
	last_position = Vector2(0,0)

@onready var node_3d = $Node3D
func _ready():
	_find_viewports(_editor_interface.get_base_control())
	for v in _editor_viewports:
		_find_cameras(v)
		
	node_3d.connect("update_color", update_color)
	node_3d.connect("update_colors", update_colors)

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

var last_3d_node
var _coloring = false
func color(event):
	var selection = _editor_interface.get_selection()
	var node = selection.get_selected_nodes()[0]
	if node is Node3D:
		last_3d_node = node
		var camera = _editor_cameras[0]
		
		var offset = _editor_interface.get_editor_main_screen().global_position
		# the 30 is a magical offset number
		offset.y += 30
		#print(offset)
		var mouse_coords = event.position - offset
		var from = camera.project_ray_origin(mouse_coords)
		var to = from + camera.project_ray_normal(mouse_coords) * 1_000
		
		mouse_3d.emit(from, to, node, _brush_size, debug_mesh)
		
var _move_coloring := false
func _input(event):
	if not _enable_painting: return
	
	
	if event is InputEventMouseButton:
		var ms = _editor_interface.get_editor_main_screen()
		var pos = ms.global_position
		if event.position.x < pos.x or \
			event.position.y < pos.y + 30 or \
			event.position.x > pos.x + ms.size.x or \
			event.position.y > pos.y + ms.size.y:
				return
		
		if event.button_index == 1:
			if event.pressed:
				color(event)
				_coloring = true
			else:
				_coloring = false
				get_tree().call_group("test", "_update()")
			
			_move_coloring = false
	
	if event is InputEventMouse:
		if event.position != last_position:
			if _coloring and not _move_coloring:
				_move_coloring = true
				var store_event = event
				await get_tree().create_timer(0.01).timeout
				
				color(store_event)
				
				_move_coloring = false
		
		last_position = event.position

var prev_mat
var last_set_node
func _on_check_box_toggled(button_pressed):
	if last_3d_node is MeshInstance3D:
		var mesh = last_3d_node.mesh
		var id = mesh.get_instance_id()
		if button_pressed:
			print(last_3d_node.get_surface_override_material(0))
			prev_mat = last_3d_node.get_surface_override_material(0)
			print(prev_mat)
			var material = load("res://addons/vertex_painter/shaders/vertex_color.tres")		
			var shader = load("res://addons/vertex_painter/shaders/vertex_color.gdshader")
			material.set_shader(shader)
			
			last_set_node = last_3d_node
			
			last_3d_node.set_surface_override_material(int(0), material)
		else:
			last_set_node.set_surface_override_material(int(0), prev_mat)

func _on_check_box_toggled2(button_pressed):
	debug_mesh = button_pressed
	if not button_pressed:
		delete_debug_mesh.emit()

func _on_line_edit_text_submitted(new_text, color):
	color_vals[color] = clampf(float(new_text), 0, 1)
	
	var line_edit = get_node(color + "LineEdit")
	line_edit.text = str(color_vals[color])

func _on_brush_size_text_submitted(new_text):
	_brush_size = clampi(int(new_text), 1, 100)
	
	var line_edit = get_node("BrushSizeLineEdit")
	line_edit.text = str(_brush_size)
	
func update_color(mdt, idx, mesh_i):
	var red = color_vals["Red"]
	var green = color_vals["Green"]
	var blue = color_vals["Blue"]
	var color = Color(red, green, blue)
	mdt.set_vertex_color(idx, color)
	
	mesh_i.mesh.clear_surfaces()
	mdt.commit_to_surface(mesh_i.mesh)

func update_colors(mdt, idxs, mesh_i: MeshInstance3D):
	var red = color_vals["Red"]
	var green = color_vals["Green"]
	var blue = color_vals["Blue"]
	var color = Color(red, green, blue)
	for idx in idxs:
		mdt.set_vertex_color(idx, color)

	mesh_i.mesh.clear_surfaces()
	mdt.commit_to_surface(mesh_i.mesh)
	
	get_tree().call_group("test", "_update")
	
	var mi_id = mesh_i.get_instance_id()
	get_tree().call_group("test", "_update_mesh_data", mi_id, mdt)


func _on_enable_painting_toggled(button_pressed):
	_enable_painting = button_pressed
	
	lock.emit(_editor_interface.get_edited_scene_root(), button_pressed)
	
	if _enable_painting:
		_editor_interface.set_main_screen_editor("3D")

