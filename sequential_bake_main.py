6#!/usr/bin/python

import sys
import argparse
import os
import tempfile


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("file",
                        help="Path to blend file. File should be previously prepared for baking")

    return parser.parse_args()


def main():
    """ Calls instances of blender with script that will bake.  """

    args = parse()
    counter_file = tempfile.NamedTemporaryFile(mode='r')
    blender_script = "./bpy_bake.py"

    while True:
        try:
            os.system("blender " + args.file +
                      " --background --factory-startup --python " +
                      blender_script + " -- " +
                      counter_file.name + " ")
        except OSError as e:
            if e.errno == os.errno.ENOENT:
                print("Is blender installed?", file=sys.stderr)
            else:
                print("Something went terribly wrong...", file=sys.stderr)

        counter_file.seek(0)
        index = int(counter_file.readline())
        total = int(counter_file.readline())

        if index == total:
            break

    counter_file.close()

    print("SUCCES!! Check if bake is correct.")
    print("Baked from file: ", args.file)


if __name__ == '__main__':
    main()
