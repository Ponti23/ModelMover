import trimesh
import time
import threading


def update_mesh(scene, mesh_file):
    """
    Replace the geometry in the current Trimesh Scene with a new mesh from a file.
    """
    new_mesh = trimesh.load(mesh_file)
    scene.clear()  # Remove the existing geometry
    scene.add_geometry(new_mesh)  # Add the new mesh
    scene.show()  # Update the viewer


def main():
    # Load the first mesh
    initial_mesh = trimesh.load("2Body.obj")
    
    # Create a scene and add the initial mesh
    scene = trimesh.Scene()
    scene.add_geometry(initial_mesh)
    
    # Show the initial mesh in the viewer
    print("Displaying 2Body.obj")
    scene.show()
     
    # Start a thread to update the viewer after 3 seconds
    def delayed_update():
        time.sleep(3)  # Wait for 3 seconds
        print("Updating to Box.obj")
        update_mesh(scene, "Box.obj")
    
    threading.Thread(target=delayed_update).start()


if __name__ == "__main__":
    main()
