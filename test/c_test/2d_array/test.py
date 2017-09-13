import numpy as np
import ctypes

rows = 10
cols = 10
infile = np.zeros((rows, cols), dtype=np.intp)
for i in range(0, rows):
    for j in range(0, cols):
        infile[i, j] = (i + 1) * (j + 1)
ctypes_arrays = [np.ctypeslib.as_ctypes(array) for array in infile]
pointer_ar = (ctypes.POINTER(ctypes.c_int) * rows)(*ctypes_arrays)

lib = ctypes.cdll.LoadLibrary("test.so")
func = lib.func
# func.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_int))
func(pointer_ar)
