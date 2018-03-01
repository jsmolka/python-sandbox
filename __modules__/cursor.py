from ctypes import *

STD_HANDLE = windll.kernel32.GetStdHandle(-11)


class CursorInfo(Structure):
    """
    Cursor info structure.
    """
    _fields_ = [
        ("size", c_int),
        ("visible", c_byte)
    ]


class COORD(Structure):
    """
    Coordinate structure.
    """
    _fields_ = [
        ("X", c_short),
        ("Y", c_short)
    ]


def hide():
    """
    Hides cursor.

    :return: None
    """
    ci = CursorInfo()
    windll.kernel32.GetConsoleCursorInfo(STD_HANDLE, byref(ci))
    ci.visible = False
    windll.kernel32.SetConsoleCursorInfo(STD_HANDLE, byref(ci))


def show():
    """
    Shows cursor.

    :return: None
    """
    ci = CursorInfo()
    windll.kernel32.GetConsoleCursorInfo(STD_HANDLE, byref(ci))
    ci.visible = True
    windll.kernel32.SetConsoleCursorInfo(STD_HANDLE, byref(ci))

    
def position(x, y):
    """
    Sets cursor position.

    :param x: x position
    :param y: y position
    :return: None
    """
    windll.kernel32.SetConsoleCursorPosition(STD_HANDLE, COORD(x, y))


def reset():
    """
    Resets cursor.

    :return: None
    """
    position(0, 0)
