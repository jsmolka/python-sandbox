import capi

pth = "dll/restypes.dll"


@capi.cfunc
def rt_none(l, i, res=None, dll=pth):
    pass


@capi.cfunc
def rt_int(l, i, res=int, dll=pth):
    pass


@capi.cfunc
def rt_dbl(l, i, res=float, dll=pth):
    pass


il = [1, 2, 3, 4, 5]
fl = [1.4, 2.5, 6.7, 3.4]

print("rt_none:", rt_none(il, len(il)))
print("rt_int:", rt_int(il, len(il)))
print("rt_dbl:", rt_dbl(fl, len(fl)))
