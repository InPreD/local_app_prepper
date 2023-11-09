#!/usr/local/bin/python

from prepper.cli import main

def correct_path(path):
    return os.path.join(os.path.dirname(sys.arg[0]), path)

if __name__ == "__main__":
    main()