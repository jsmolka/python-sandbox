import capi

dll = "dll/restypes.dll"


@capi.func(dll, res=None)
def rt_none(l, i):
    pass


@capi.func(dll, res=int)
def rt_int(l, i):
    pass


@capi.func(dll, res=float)
def rt_dbl(l, i):
    pass


if __name__ == "__main__":
    il = [1, 2, 3, 4, 5]
    fl = [1.4, 2.5, 6.7, 3.4]

    print("rt_none:", rt_none(il, len(il)))
    print("rt_int:", rt_int(il, len(il)))
    print("rt_dbl:", rt_dbl(fl, len(fl)))
