import ctypes as ct
import numpy as np


def ctype(tp):
    """
    Converts type into ctype.

    :param tp: type
    :return: type
    """
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
    """
    Returns dll arguments type.

    :param arg: argument to get type for
    :return: type
    """
    if isinstance(arg, np.ndarray):
        if len(arg.shape) == 1:
            return np.ctypeslib.ndpointer(dtype=arg.dtype, flags="C")
        if len(arg.shape) == 2:
            return np.ctypeslib.ndpointer(dtype=np.uintp, ndim=1, flags="C")
        raise ValueError("Invalid shape {0}".format(arg.shape))
    return type(arg)


def convert_list(arg):
    """
    Converts list for dll call.

    :param arg: list to convert
    :return: list
    """
    if isinstance(arg[0], list):
        data = [convert_list(row) for row in arg]
        return (ct.POINTER(ctype(arg[0][0])) * len(arg))(*data)
    return (ctype(arg[0]) * len(arg))(*arg)


def convert_ndarray(arg):
    """
    Converts ndarray for dll call.

    :param arg: ndarray to convert
    :return: ndarray
    """
    if arg.ndim == 1:
        return arg
    if arg.ndim == 2:
        return (arg.__array_interface__['data'][0] +
                np.arange(arg.shape[0]) * arg.strides[0]).astype(np.uintp)
    raise ValueError("Invalid dimension {0}".format(arg.ndim))


def convert(arg):
    """
    Converts argument for dll call.

    :param arg: argument to convert
    :return: converted argument
    """
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


dlls = {}


def load_dll(pth):
    """
    Loads dll or returns dll if it has already been loaded.

    :param pth: dll path
    :return: loaded dll
    """
    global dlls
    if pth not in dlls:
        dlls[pth] = ct.cdll.LoadLibrary(pth)
    return dlls[pth]


def func(pth, res=None):
    """
    Decorator for easy dll function calls

    @func(dll, res=type)
    def function(*args):
        pass

    :param pth: dll path
    :param res: result type
    :return: dll function result
    """
    def decorate(pyfunc):
        """
        Decorator.

        :param pyfunc: function to wrap around
        :return: dll function result
        """
        def wrap(*args, **kwargs):
            """
            Wrapper.

            :param args: function arguments
            :param kwargs: keyword arguments
            :return: dll function result
            """
        
            dll = load_dll(pth)
            cfunc = getattr(dll, pyfunc.__name__)

            args = [convert(arg) for arg in args]
            cfunc.argtypes = [argtype(arg) for arg in args]
            cfunc.restype = ctype(res)

            return cfunc(*args)
            
        return wrap
        
    return decorate
