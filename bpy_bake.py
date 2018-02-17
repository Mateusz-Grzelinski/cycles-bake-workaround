"""
author: Mateusz Grzeliński
Blender Cycles 2.79
Problem:
    Blender cycles uses too much memory when baking multiple objects
Solution (workaround):
    Bakes all object in selected group sequentially, one ater another
    to save memory script will restart blender after every bake
    bake source in: object_bake_api.c
"""

import bpy
import sys


def bake_sequentially(file_path):

    D = bpy.data
    C = bpy.context
    objects = [i for i in C.selected_objects if i.type == 'MESH']

    # Use temp file to store current index
    # first line should be last executed index
    current_index = 0
    with open(file_path, 'r') as f:
        try:
            current_index = int(f.readline())
        except ValueError as e:
            pass  # first run <- not the best solution

    bpy.ops.object.select_all(action='DESELECT')
    objects[current_index].select = True

    # find image to bake to
    img = objects[current_index].active_material.node_tree.nodes.active.image

    # bake save & cleanup
    bpy.ops.object.bake(type='DIFFUSE')
    img.save()

    with open(file_path, 'w') as f:
        total_len = len(objects)
        f.write(str(current_index + 1) + '\n')
        f.write(str(total_len))

    return current_index


if __name__ == "__main__":
    argv = sys.argv
    # python script argument are given after '--'
    if "--" not in argv:
        argv = []  # as if no args are passed
    else:
        argv = argv[argv.index("--") + 1:]

    index = bake_sequentially(argv[0])

    print("Baking single object done. Tmp file: " + argv[0]
          + " Index: " + str(index)
          + '\n\n\n\n')
