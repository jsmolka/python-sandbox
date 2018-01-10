import os
from ctypes import *

STD_OUTPUT_HANDLE = -11
HANDLE = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)	


class CursorInfo(Structure):
    _fields_ = [
        ("size", c_int),
        ("visible", c_byte)
    ]
    

class COORD(Structure): 
    _fields_ = [
        ("X", c_short), 
        ("Y", c_short)
    ]

    
def hide():
    ci = CursorInfo()
    windll.kernel32.GetConsoleCursorInfo(HANDLE, byref(ci))
    ci.visible = False
    windll.kernel32.SetConsoleCursorInfo(HANDLE, byref(ci))
    

def show():
    ci = CursorInfo()
    windll.kernel32.GetConsoleCursorInfo(HANDLE, byref(ci))
    ci.visible = True
    windll.kernel32.SetConsoleCursorInfo(HANDLE, byref(ci))


def reset():
    windll.kernel32.SetConsoleCursorPosition(HANDLE, COORD(0, 0))
