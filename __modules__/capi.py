import ctypes as ct
import numpy as np


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
        data = [convert_list(row) for row in arg]
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


def func(pth, res=None):
    """
    Decorator for easy dll function calls

    @func(dll, res=type)
    def function(*args): pass
    """
    def decorator(pyfunc):
        
        def wrapper(*args, **kwargs):
        
            dll = load_dll(pth)
            cfunc = getattr(dll, pyfunc.__name__)

            args = [convert(arg) for arg in args]
            cfunc.argtypes = [argtype(arg) for arg in args]
            cfunc.restype = ctype(res)

            return cfunc(*args)
            
        return wrapper
        
    return decorator
