import ctypes as ct
import getpass
import inspect
import numpy as np
import os
import sys


def join(*pths):
    return os.path.join("", *pths)


def pydir(dll=None):
    pth = os.path.dirname(sys.modules["__main__"].__file__)
    return join(pth, dll) if dll else pth


def user():
    return getpass.getuser()


def get_defaults(func):
    defaults = inspect.getargspec(func).defaults
    if len(defaults) == 1:
        return None, defaults[0]
    if len(defaults) == 2:
        return defaults
    raise ValueError("Invalid defaults {0}".format(defaults))


def ctype(tp):
    if tp is None:
        return None
    if not isinstance(tp, type):
        tp = type(tp)
    if tp is int:
        return ct.c_int
    if tp is float:
        return ct.c_double
    if tp is str:
        return ct.c_char_p
    raise TypeError(tp)


def argtype(arg):
    if isinstance(arg, np.ndarray):
        if len(arg.shape) == 1:
            return np.ctypeslib.ndpointer(dtype=arg.dtype, flags="C")
        if len(arg.shape) == 2:
            return np.ctypeslib.ndpointer(dtype=np.uintp, ndim=1, flags="C")
        raise ValueError("Invalid shape {0}".format(arg.shape))
    return type(arg)


def convert_list(arg):
    if isinstance(arg[0], list):
        data = [convert_list(arg[row]) for row in range(len(arg))]
        return (ct.POINTER(ctype(arg[0][0])) * len(arg))(*data)
    return (ctype(arg[0]) * len(arg))(*arg)


def convert_ndarray(arg):
    if len(arg.shape) == 1:
        return arg
    if len(arg.shape) == 2:
        return (arg.__array_interface__['data'][0] +
            np.arange(arg.shape[0]) * arg.strides[0]).astype(np.uintp)
    raise ValueError("Invalid shape {0}".format(arg.shape))


def convert(arg):
    if isinstance(arg, int):
        return ct.c_int(arg)
    if isinstance(arg, float):
        return ct.c_double(arg)
    if isinstance(arg, str):
        return ct.c_char_p(arg.encode())
    if isinstance(arg, list):
        return convert_list(arg)
    if isinstance(arg, np.ndarray):
        return convert_ndarray(arg)
    raise TypeError(arg)


dlls = []


def load_dll(pth):
    global dlls
    for pth_, dll_ in dlls:
        if pth == pth_:
           return dll_
    dll = ct.cdll.LoadLibrary(pth)
    dlls.append((pth, dll))
    return dll


def cfunc(func):
    """
    Decorator for easy C function calls

    @cfunc
    def func(*args, [res=type], dll="name.dll"): pass
    """
    def wrapper(*args, func=func):
        res, pth = get_defaults(func)
        dll = load_dll(pth)
        func = getattr(dll, func.__name__)

        args = [convert(arg) for arg in args]
        func.argtypes = [argtype(arg) for arg in args]
        func.restype = ctype(res)

        return func(*args)

    return wrapper
