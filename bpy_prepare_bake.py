"""
Author: Mateusz Grzeliński
Blender Cycles 2.79

Script will prepare selected objects to be baked into single image. It will:
    - create new image
    - create texture node with above image in every material used by selected objects
    - select newly created node
    - set bake setting (+ samples and compute method)
Now just click bake.

! Assume that uvs are arleady prepared
! Assume to use default (render) uv (use for exsample Texture Atlas addon)
! Assume you have arleady saved blend file somewhere
"""
import bpy



def set_image_in_materials(img_name, resolution):
    """ Adds texture node in every material and selects it """
    img = bpy.data.images.new(name=img_name, width=resolution, height=resolution)

    for obj in bpy.context.selected_objects:
        for slot in obj.material_slots:
            material = slot.material
            nodes = material.node_tree.nodes
            node = nodes.new('ShaderNodeTexImage')
            node.location = 0, 600
            node.image = img
            node.select = True
            nodes.active = node

    # pack image with blender file (or save externally) or it will be deleted
    # img.filepath = '/' + img_name
    # img.save()
    img.pack(as_png=True)
    bpy.ops.wm.save_mainfile()


def set_bake_settings():
    bpy.context.scene.cycles.samples = 1
    bpy.context.scene.cycles.bake_type = 'DIFFUSE'
    bake = bpy.context.scene.render.bake
    bake.use_pass_indirect = False
    bake.use_pass_direct = False
    bake.use_pass_color = True
    bake.use_selected_to_active = False
    bake.use_clear = False
    bake.use_cage = False
    bake.margin = 0

    # high memory consumtion - recommend to use cpu
    bpy.context.scene.cycles.device = 'CPU'

if __name__ == "__main__":
    # New image settings:
    img_name = "Kafelki"
    resolution = 1024 * 4
    set_image_in_materials(img_name, resolution)
    set_bake_settings()

# bpy.ops.object.bake_image()
