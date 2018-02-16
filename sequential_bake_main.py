#!/usr/bin/python

import sys
import argparse
import os
import tempfile
from time import sleep


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("file",
                        help="Path to blend file. File should be previously prepared for baking")
    parser.add_argument("--group", metavar="GROUP_NAME", default='',
                        help="Objects within this group will be baked. \
                        If None, current selection will used")

    return parser.parse_args()


def main():
    """
    Bakes sequentially .blend file

    Each time after single object is baked, saves baked image and restarts blender. It allows to clear memory.
    """
    # path = "/home/mat/storage/blender/pliki\ blend/Lustra/pliki_blend/Cycles_baking.blend"

    args = parse()
    counter_file = tempfile.NamedTemporaryFile(mode='r')
    current_dir = os.path.dirname(os.path.abspath(__file__))
    blender_script = current_dir + "/bpy_bake.py"

    while True:
        try:
            os.system("blender " + args.file +
                      " --background --python " +
                      blender_script + " -- " +
                      counter_file.name + " " +
                      args.group)
        except OSError as e:
            if e.errno == os.errno.ENOENT:
                print("Is blender installed?", file=sys.stderr)
            else:
                print("Bake might have failed", file=sys.stderr)

        counter_file.seek(0)
        index = int(counter_file.readline())
        total = int(counter_file.readline())
        # sleep(3)
        if index == total:
            break

    counter_file.close()


if __name__ == '__main__':
    main()
