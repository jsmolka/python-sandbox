import os
import utils

files = utils.get_files()

dll = []
for file in files:
    extension = os.path.splitext(file)[1]
    if extension == ".dll":
        dll.append(os.path.dirname(file))

dll = list(set(dll))
for path in dll:
    print(path)
    utils.add_path(path, "path")
