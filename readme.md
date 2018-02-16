# Blender cycles bake high memory usage workaround

## Problem
Cycles baking process consumes too much memory, especially when it comes to
baking __multiple objects__, that can not be joined together into one.

## Workaround
Bake objects one by one.
After each bake blender must be restarted, because memory is not freed after
bake is completed (even after image is saved).
To achive this, script file [sequential_bake_main.py](./sequential_bake_main) runs
Blender with script [bpy_bake.py](./bpy_bake.py) in loop untill all objects are
baked. One by one. 
Those 2 files should be in the same directory.
