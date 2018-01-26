@echo off

gcc -shared -fPIC -m32 -o argtypes.dll argtypes_list.c argtypes_numpy.c argtypes_defaults.c
