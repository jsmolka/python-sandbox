import numpy as np
from ctypes import cdll, c_void_p, c_int

rows = 10
cols = 10
input = np.zeros((rows, cols), dtype=np.uint32)
for i in range(0, rows):
    for j in range(0, cols):
        input[i, j] = (i + 1) * (j + 1)
lib = cdll.LoadLibrary("test.so")
func = lib.func
func.restype = None
func.argtypes = [np.ndpointer(c_int, flags="C_CONTIGUOUS"), c_int, c_int]
func(c_void_p(input.ctypes.data), c_int(rows), c_int(cols))
