import ctypes
import getpass
import inspect
import os


def join(*pths):
    """Combines multiple paths"""
    return os.path.join("", *pths)


def pydir(name=None):
    """Returns path of the current file"""
    pth = os.path.dirname(os.path.abspath(inspect.stack()[0][1]))
    return join(pth, name) if name else pth
    

def user():
    """Returns current user"""
    return getpass.getuser()

   
def convert_int(types, arg):
    """Converts int"""
    types.append(ctypes.c_int)
    return arg
    
    
def convert_str(types, arg):
    """Converts str"""
    types.append(ctypes.c_char_p)
    return ctypes.c_char_p(bytes(arg, encoding="utf-8"))
    
    
def convert_float(types, arg):
    """Converts float"""
    types.append(ctypes.c_float)
    return ctypes.c_float(arg)
    
    
def convert_list(types, arg):
    """Converts list"""
    convert(arg, arg[0])
    array = (arg.pop() * len(arg))
    types.append(array)
    return array(*arg)    
   
   
def convert(types, *args):   
    """Converts args"""
    for arg in args:
        if isinstance(arg, int): 
            arg = convert_int(types, arg)       
        elif isinstance(arg, str):
            arg = convert_str(types, arg)
        elif isinstance(arg, float):
            arg = convert_float(types, arg)
        elif isinstance(arg, list):
            arg = convert_list(types, arg)
        else:
            raise TypeError(arg)
    return args


def dll(func):
    """Decorator for dll functions"""  
    
    def dll_func(*args):
        """Creates valid dll function call"""
        pth = inspect.getargspec(func).defaults[0]
        
        types = []
        args = convert(types, *args)
        print(types)
        
        # cdll = ctypes.cdll.LoadLibrary(path)
        # print("calling", func.__name__, "in", cdll, "with", args)
        # return result
        
    return dll_func
    
    
@dll
def func(a, b, c, d, dll=pydir("test.dll")):
    pass  # Placeholder for dll function
    
    
func(1.4, "lul", 5, [1, 2, 3, 4])
