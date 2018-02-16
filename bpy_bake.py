# author: Mateusz Grzeliński
# email: gmati2@wp.pl
# Problem: Blender cycles uses too much memory when baking multiple objects
# Solution (workaround):
# Bakes all object in selected group sequentially, one ater another
# to save memory script will restart blender after every bake
# bake source in: object_bake_api.c

import bpy
import sys
from time import sleep


def bake_sequentially(file_path, group_name=None):
    """
    group_name: name of group whose objects shall be baked. If None, uses current selection
    """

    D = bpy.data
    C = bpy.context
    oldsamples, C.scene.cycles.samples = C.scene.cycles.samples, 1
#    group_name = 'BakeUVMap'
#    image_name = 'Kafelki_kolorowe_diff'

    objects = []
    if group_name is None:
        objects = [i for i in C.selected_objects if i.type == 'MESH']
    else:
        objects = D.groups[group_name].objects

# Use temp file to store current index
# first line should be last executed index
    total_len = len(objects)
    current_index = 0
    with open(file_path, 'r') as f:
        try:
            current_index = int(f.readline())
            C.scene.render.bake.use_clear = False
        except ValueError as e:# first run
            C.scene.render.bake.use_clear = True

# select one object
    bpy.ops.object.select_all(action='DESELECT')
    objects[current_index].select = True

# find image to bake to
#    img = bpy.data.images[image_name]
    img = objects[current_index].active_material.node_tree.nodes.active.image

# bake save & cleanup
    bpy.ops.object.bake(type='DIFFUSE')
    img.save()
    C.scene.cycles.samples = oldsamples

    with open(file_path, 'w') as f:
        print("writing index and total to tmp file:", current_index, total_len)
        f.write(str(current_index + 1) + '\n')
        f.write(str(total_len))


if __name__ == "__main__":
    argv = sys.argv

    if "--" not in argv:
        argv = []  # as if no args are passed
    else:
        argv = argv[argv.index("--") + 1:]

    bake_sequentially(argv[0])
    # sleep(3)

    print("Baking single object done." + argv[0])


#    uv_image = "UV_image"
#    bpy.data.images.new(name=uv_image,width = 1024,height = 1024)

#    mat = bpy.data.materials[material.name]

#    nodes = mat.node_tree.nodes
#    node = nodes.new('ShaderNodeTexImage')
#    node.location = 300,0
#    node.label = 'uv_image'
#    node.name = 'uv_image'
#    node.image = bpy.data.images[uv_image]
#    uv_img = bpy.data.images[uv_image]
#    node.select = True
#    nodes.active = node
#    for area in bpy.context.screen.areas :
#        if area.type == 'IMAGE_EDITOR' :
#            area.spaces.active.image = uv_img

#    for ob in bpy.data.objects:
#        if 'pattern' in ob.name: #object of interest has the name pattern)
#            ob.select = True
#            bpy.context.scene.objects.active = ob
#        else:
#            ob.select = False
