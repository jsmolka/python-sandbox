import os
from ctypes import *
	
STD_OUTPUT_HANDLE = -11	

# Hide cursor
# https://github.com/GijsTimmers/cursor
class _CursorInfo(Structure):
	_fields_ = [
		("size", c_int),
		("visible", c_byte)
	]
 
ci = _CursorInfo()
handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
windll.kernel32.GetConsoleCursorInfo(handle, byref(ci))
ci.visible = False
windll.kernel32.SetConsoleCursorInfo(handle, byref(ci))

# Cursor position
# https://rosettacode.org/wiki/Terminal_control/Cursor_positioning#Python 
class COORD(Structure):
    pass
 
COORD._fields_ = [("X", c_short), ("Y", c_short)]

h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
row = 0
col = 0
windll.kernel32.SetConsoleCursorPosition(h, COORD(row, col))
	