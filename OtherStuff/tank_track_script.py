import bpy

def adjust_keyframes(obj, frame_adjustment):
    action = obj.animation_data.action
    for f in action.fcurves:
        #print(f.data_path + " - " + str(f.array_index))
        #print(len(f.keyframe_points))
        for p in f.keyframe_points:
            p.co[0] += frame_adjustment
        
        end_points = f.keyframe_points[-frame_adjustment:]
        
        i = 1.0
        for p in end_points:
            p.co[0] = i
            i += 1
        
        f.keyframe_points.sort()

#adjust_keyframes(bpy.context.active_object, 4)

# duplicate and adjust the keyframes
if False:
    items = 49
    #items = 5
    for i in range(items):
        bpy.ops.object.duplicate()
        obj = bpy.context.active_object
        adjust_keyframes(obj, 4)
        
# instance meshes
if True:
    mesh = bpy.data.objects["TrackPiece"].data

    objs = bpy.context.selected_objects
    for obj in objs:
        # set mesh instance
        obj.data = mesh
        
        # some testing...
        #action = obj.animation_data.action
        #bpy.data.actions.remove(action, do_unlink = True)
        
        
        # remove bevel modifier
        #modifier_to_remove = obj.modifiers.get("Bevel")
        #obj.modifiers.remove(modifier_to_remove)
