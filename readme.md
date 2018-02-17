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
Those 2 files should be in the same directory.

# Usage & examples
bpy_* file are meant to be used inside blender.
[Sequential_bake_main.py](./sequential_bake_main.py) calls
[bpy_bake.py](./bpy_bake.py) with command 
```
blener /path/to/my_file.blend --background --python ./bpy_bake.py -- /path/to/tempfile
```
Tempfile is used to communicate to sequential_bake_main.py when to stop calling
instances of blender

Examples:
1. Bake selected object in file: `"/path/to/file.blend"`
   ```bash
   python sequential_bake_main.py "/path/to/file.blend"
   ```
