import capi
from random import randint

dll = "dll/argtypes.dll"


@capi.func(dll)
def at_lst_1d_int(l, i):
    pass


@capi.func(dll)
def at_lst_1d_dbl(l, i):
    pass


@capi.func(dll)
def at_lst_2d_int(l, r, c):
    pass


@capi.func(dll)
def at_lst_2d_dbl(l, r, c):
    pass


n = 10
il = [[randint(100, 999) for i in range(n)] for j in range(n)]
fl = [[float(e) for e in r] for r in il]

at_lst_1d_int(il[0], n)
at_lst_1d_dbl(fl[0], n)

at_lst_2d_int(il, n, n)
at_lst_2d_dbl(fl, n, n)
