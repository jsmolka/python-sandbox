import admin
import os
import utils

common = os.getcwd()

include = [
    common,
    common + "\\sfml"
]

lib = [
    common + "\\sfml\\lib"
]

dll = [
    common + "\\sfml\\dll"
]

for include_path in include:
    print(include_path)
    utils.add_path(include_path, "CPATH")

for lib_path in lib:
    print(lib_path)
    utils.add_path(lib_path, "LIBRARY_PATH")

for dll_path in dll:
    print(dll_path)
    utils.add_path(dll_path, "PATH")
