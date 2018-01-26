import capi
import numpy as np
from random import randint

pth = "dll/argtypes.dll"


@capi.cfunc
def at_npy_1d_int(l, i, dll=pth):
    pass


@capi.cfunc
def at_npy_1d_dbl(l, i, dll=pth):
    pass


@capi.cfunc
def at_npy_2d_int(l, r, c, dll=pth):
    pass


@capi.cfunc
def at_npy_2d_dbl(l, r, c, dll=pth):
    pass


@capi.cfunc
def at_npy_1d_uint32(l, i, dll=pth):
    pass


@capi.cfunc
def at_npy_2d_uint16(l, r, c, dll=pth):
    pass


@capi.cfunc
def at_npy_1d_out_int(in_, i, out, dll=pth):
    pass


@capi.cfunc
def at_npy_2d_out_dbl(in_, r, c, out, dll=pth):
    pass


n = 5
il = [[randint(100, 999) for i in range(n)] for j in range(n)]
fl = [[float(e) for e in r] for r in il]

at_npy_1d_int(np.array(il[0], dtype=np.int_), n)
at_npy_1d_dbl(np.array(fl[0], dtype=np.float_), n)

at_npy_2d_int(np.array(il, dtype=np.int_), n, n)
at_npy_2d_dbl(np.array(fl, dtype=np.float_), n, n)

at_npy_1d_uint32(np.array(il[0], dtype=np.uint32), n)
at_npy_2d_uint16(np.array(il, dtype=np.uint16), n, n)

n = 3
il = [[randint(10, 49) for i in range(n)] for j in range(n)]
fl = [[float(e) for e in r] for r in il]

arr_in = np.array(il[0], dtype=np.int_)
arr_out = np.zeros_like(arr_in)
print("at_npy_1d_out_int")
at_npy_1d_out_int(arr_in, n, arr_out)
print(arr_in)
print(arr_out)

arr_in = np.array(fl, dtype=np.float_)
arr_out = np.zeros_like(arr_in)
print("at_npy_2d_out_dbl")
at_npy_2d_out_dbl(arr_in, n, n, arr_out)
print(arr_in)
print(arr_out)
