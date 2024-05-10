import bpy
import math
import bpy_extras

def make_new_maps(new_uv):
    for obj in bpy.context.selected_objects:
        if obj.type == "MESH" and new_uv not in obj.data.uv_layers:
            obj.data.uv_layers.new(name=new_uv)

def set_active(name):
    for obj in bpy.context.selected_objects:
        if name in obj.data.uv_layers:
            obj.data.uv_layers[name].active = True

def remove(name):
    for obj in bpy.context.selected_objects:
        if name in obj.data.uv_layers:
            uv_layer = obj.data.uv_layers[name]
            obj.data.uv_layers.remove(uv_layer)

def uv_separate():
    for obj in bpy.context.selected_objects:
        islands = bpy_extras.mesh_utils.mesh_linked_uv_islands(obj.data)
        print(islands)

def test(uv_name):
    print("###")
    unique_mats = []
    sel = bpy.context.selected_objects
    for obj in sel:
        for m_slot in obj.material_slots:
            m = m_slot.material
            if m not in unique_mats:
                unique_mats.append(m)
    
    i = 0 
    # go through each of the unique materials
    for unique_mat in unique_mats:
        print(unique_mat)
        
        for obj in sel:
            for m_slot in obj.material_slots:
                m = m_slot.material
                
                # find if selected object has a material that matches the unique material
                if m == unique_mat:
                    
                    print(obj)
                    polygons = obj.data.polygons
                    print("Poly count " + str(len(polygons)))
                    
                    uv_map = obj.data.uv_layers[uv_name].uv
                    
                    a = 0
                    
                    # a polygon is a FACE
                    for p in polygons:
                        
                        # check if face uses this material
                        if p.material_index == m_slot.slot_index:
                            
                            for loop_index in p.loop_indices:
                                
                                a += 1
                                uv_map[loop_index].vector.x += -3 +  5 * i
                                uv_map[loop_index].vector.y += -3
                                pass
                    
                    #print("vertices with matching slot: " + str(a))
                    
                    # break because we found the matching mat, don't care about the others
                    break
            
        # iterate once for each unique mat
        i += 1
        

new_map = "UVMap2"


reset = 1
if reset == 1:
    remove(new_map)
    make_new_maps(new_map)
    set_active(new_map)
    test(new_map)
else:
    pass

#uv_separate()