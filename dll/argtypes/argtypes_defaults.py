import capi

pth = "dll/argtypes.dll"


@capi.cfunc
def at_int(i, dll=pth):
    pass


@capi.cfunc
def at_dbl(d, dll=pth):
    pass


@capi.cfunc
def at_str(s, dll=pth):
    pass


at_int(100)
at_dbl(75.0123456789)
at_str("this works")
