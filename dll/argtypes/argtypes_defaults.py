import capi

dll = "dll/argtypes.dll"


@capi.func(dll)
def at_int(i):
    pass


@capi.func(dll)
def at_dbl(d):
    pass


@capi.func(dll)
def at_str(s):
    pass


if __name__ == "__main__":
    at_int(100)
    at_dbl(75.0123456789)
    at_str("this works")
