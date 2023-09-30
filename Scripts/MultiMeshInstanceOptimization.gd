@tool

extends Node

var mesh_dict = {}

# Called when the node enters the scene tree for the first time.

func _ready():
	if Engine.is_editor_hint():
		var topnode = get_parent()
		findMeshInstance3D(topnode)
		print(mesh_dict)
		print("---")
		applyMultiMesh(topnode.get_children()[0])

func findMeshInstance3D(node):
	for child in node.get_children():
		if child is MeshInstance3D:
			# add to dict
			var m = child.get_mesh()
			var path = m
			if path not in mesh_dict:
				mesh_dict[path] = [child]
			else:
				mesh_dict[path].append(child)
		else:
			findMeshInstance3D(child)

func applyMultiMesh(node):
	print(mesh_dict)
	print("###")
	for m in mesh_dict:
		var meshcount = len(mesh_dict[m])
		print(meshcount)
		
		if meshcount > 1:
			var multimesh = MultiMesh.new()
			multimesh.mesh = m
			multimesh.transform_format = MultiMesh.TRANSFORM_3D
			multimesh.instance_count = meshcount
			multimesh.visible_instance_count = meshcount
			var i = 0
			for inst in mesh_dict[m]:
				inst.hide()
				multimesh.set_instance_transform(i, inst.global_transform)
				i += 1
			
			var mm_inst = MultiMeshInstance3D.new()
			mm_inst.multimesh = multimesh
			node.add_child(mm_inst)
			mm_inst.set_owner(get_tree().edited_scene_root)
			

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
	pass
