import trimesh

def load_mesh(filename):
    try:
        print("Mesh Loaded Succesfully")
        mesh = trimesh.load_mesh(filename)
        return mesh
    except:
        print("Error Occured")

def view_mesh(mesh, combine_list):
    # Check if it's a Scene or a single mesh
    if isinstance(mesh, trimesh.Scene):
        # Iterate over the geometries in the scene (each part of the scene)
        counter = 0
        for idx, submesh in enumerate(mesh.geometry.values()):
            if counter in combine_list:
                print(f"Visualizing submesh {idx + 1}")
                submesh.show()  # This will open a separate window for each submesh
            counter += 1
            #print(counter)
    else:
        # If the mesh is not a scene, just show it
        mesh.show()


def generate_list(mesh):
    groups = []
    groups = list(range(len(mesh.geometry)))
    return groups


def combine_mesh(mesh, combine_list):
    if isinstance(mesh, trimesh.Scene):
        # Collect the submeshes you want to combine
        mesh_to_combine = []
        counter = 0
        for idx, submesh in enumerate(mesh.geometry.values()):
            if counter in combine_list:
                mesh_to_combine.append(submesh)
                #print(f"Adding submesh {idx + 1} to combine list")
            counter += 1

        # Combine the collected meshes
        if len(mesh_to_combine) >= 1:
            combined_mesh = trimesh.util.concatenate(mesh_to_combine)
            print("Meshes combined successfully!")
            return combined_mesh
        else:
            print("Not enough meshes to combine!")
            return mesh
    #else:
        #print("Single mesh detected!")
        #return mesh

    

def scale_mesh(mesh, scaling_factor):
    scaled_mesh = mesh.copy()
    scaled_mesh.apply_scale(scaling_factor)
    return scaled_mesh


"""
filename = 'objStuff/PigTracker Mounts and frames.obj'
#filename = '2Body.obj'

myMesh = load_mesh(filename)
generate_list(myMesh)



combine_list1=[0,20]
combine_list2=[19,17]


mesh = load_mesh(filename)
combined_mesh1 = combine_mesh(mesh, combine_list1)
combined_mesh2 = combine_mesh(mesh, combine_list2)
#generate_list(mesh)
view_mesh(mesh, combine_list1)
view_mesh(mesh, combine_list2)

exporting_scene = trimesh.Scene()

exporting_scene.add_geometry(combined_mesh1, node_name="Group1")
exporting_scene.add_geometry(combined_mesh2, node_name="Group2")

print('showing before export')
exporting_scene.show()
exporting_scene.export('2BodyCombined.obj')

print('showing exported')
newmesh = load_mesh('2BodyCombined.obj')
view_mesh(newmesh, [0])

view_mesh(newmesh, [1])

view_mesh(newmesh, [3])

"""