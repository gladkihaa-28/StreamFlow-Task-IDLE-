import os
try:
    from CompiledFiles import cmain
except:
    from Task.CompiledFiles import cmain
import sys
import os


def run(file_name):
    cmain.main(file_name, file_name)


if __name__ == "__main__":
    path = sys.argv[1]
    run(path)
