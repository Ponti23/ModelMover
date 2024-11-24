import trimesh



data = {'a': ['0', '1', '2'], 'b': ['3', '4', '5']}

def combine_mesh(group, list):
    print(group)
    print(list)
    return list


def export_file(data):
    scene = []
    for group, list in data.items():
        combined_mesh = combine_mesh(group, list)
        scene.append(combined_mesh)
    return scene

scene = export_file(data)
print(scene)