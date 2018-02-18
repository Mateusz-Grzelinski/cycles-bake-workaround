# Blender cycles bake high memory usage workaround

## Problem
Cycles baking process consumes too much memory, especially when it comes to
baking __multiple objects__, that can not be joined together into one.

## Workaround
Bake objects one by one.
After each bake blender must be restarted, because memory is not freed after
bake is completed (even after image is saved).
To achive this, script file [sequential_bake_main.py](./sequential_bake_main) runs
Blender with script [bpy_bake.py](./bpy_bake.py) in loop untill all selected objects are
baked. One by one.

# Usage & examples
Files [sequential_bake_main.py](./sequential_bake_main) and [bpy_bake.py](./bpy_bake.py) sould be in the same folder.

bpy_* file are meant to be used inside blender.

[Bpy_prepare_bake.py](./bpy_prepare_bake.py) is used to automate preparation for baking. Look inside for details.

[Sequential_bake_main.py](./sequential_bake_main.py) calls
[bpy_bake.py](./bpy_bake.py) with command 
```
blener /path/to/my_file.blend --background --factory-startup --python ./bpy_bake.py -- /path/to/tempfile
```
Tempfile is used to communicate to [sequential_bake_main.py](./sequential_bake_main.py) when to stop calling instances of blender (created automatically)

Examples:
1. Bake selected object in file: `"/path/to/file.blend"` (remember to properly escape path)
   ```bash
   python sequential_bake_main.py "/path/to/file.blend"
   ```
