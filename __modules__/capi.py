import ctypes as ct
import getpass
import inspect
import os
import sys


def join(*pths):
    return os.path.join("", *pths)


def pydir(fl=None):
    pth = os.path.dirname(sys.modules["__main__"].__file__)
    return join(pth, fl) if fl else pth
    

def user():
    return getpass.getuser()
    
    
def get_defaults(func):
    defaults = inspect.getargspec(func).defaults
    if len(defaults) == 2:
        return defaults
    else:
        return None, defaults[0]
    
    
def ctype(ptype):
    if ptype is None:
        return None
    if not isinstance(ptype, type):
        ptype = type(ptype)
    if ptype is int:
        return ct.c_int
    if ptype is float:
        return ct.c_double
    if ptype is str:
        return ct.c_char_p
    else:
        raise TypeError(ptype)
                
        
def convert(arg):
    if isinstance(arg, int):
        return ct.c_int(arg)
    if isinstance(arg, float):
        return ct.c_double(arg)
    if isinstance(arg, str):
        return ct.c_char_p(arg.encode())
    if isinstance(arg, list):
        if isinstance(arg[0], list):
            data = [convert(arg[row]) for row in range(len(arg))]
            return (ct.POINTER(ctype(arg[0][0])) * len(arg))(*data)
        return (ctype(arg[0]) * len(arg))(*arg)
    else:
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
        func.argtypes = [type(arg) for arg in args]
        func.restype = ctype(res)

        return func(*args)
        
    return wrapper
