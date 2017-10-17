import numpy as np
import ctypes

lib = ctypes.cdll.LoadLibrary("test.so")
func = lib.func
func.restype = None
func.argtypes = [np.ctypeslib.ndpointer(ctypes.c_int, flags="C_CONTIGUOUS"), ctypes.c_size_t]

cols = 100
indata = np.zeros(cols, dtype=np.int32)
for i in range(0, cols):
    indata[i] = i

func(indata, indata.size)

for i in range(0, cols):
    print(indata[i])
