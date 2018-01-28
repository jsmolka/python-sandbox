import os
import winreg
from ctypes import *


def add_to_env(env, pth):
    """Adds path to system environment"""
    if env in os.environ:
        if pth not in os.environ[env].split(";"):
            os.system("setx {0} \"%{0}%;{1}\" >nul 2>nul".format(env, pth))
    else:
        os.system("setx {0} \"{1}\" >nul 2>nul".format(env, pth))


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


def cursor_hide():
    """Hides cursor"""
    ci = CursorInfo()
    windll.kernel32.GetConsoleCursorInfo(HANDLE, byref(ci))
    ci.visible = False
    windll.kernel32.SetConsoleCursorInfo(HANDLE, byref(ci))


def cursor_show():
    """Shows cursor"""
    ci = CursorInfo()
    windll.kernel32.GetConsoleCursorInfo(HANDLE, byref(ci))
    ci.visible = True
    windll.kernel32.SetConsoleCursorInfo(HANDLE, byref(ci))


def cursor_set(x, y):
    """Sets cursor"""
    windll.kernel32.SetConsoleCursorPosition(HANDLE, COORD(x, y))


def cursor_reset():
    """Resets cursor"""
    cursor_set(0, 0)


def get_registry(path, name, hkey=winreg.HKEY_CURRENT_USER):
    """Gets registry key"""
    try:
        root_key=winreg.OpenKey(hkey, path, 0, winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(root_key, name)
        winreg.CloseKey(root_key)
        return value
    except WindowsError:
        return None


def set_registry(path, name, value, hkey=winreg.HKEY_CURRENT_USER):
    """Sets registry key"""
    try:
        winreg.CreateKey(hkey, path)
        registry_key = winreg.OpenKey(hkey, path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(registry_key)
        return True
    except WindowsError:
        return False


SHORT = c_short
WORD = c_ushort


class SMALL_RECT(Structure):
    _fields_ = [
        ("Left", SHORT),
        ("Top", SHORT),
        ("Right", SHORT),
        ("Bottom", SHORT)]


class CONSOLE_SCREEN_BUFFER_INFO(Structure):
    _fields_ = [
        ("dwSize", COORD),
        ("dwCursorPosition", COORD),
        ("wAttributes", WORD),
        ("srWindow", SMALL_RECT),
        ("dwMaximumWindowSize", COORD)]


def get_color():
    """Returns the current text color"""
    csbi = CONSOLE_SCREEN_BUFFER_INFO()
    windll.kernel32.GetConsoleScreenBufferInfo(HANDLE, byref(csbi))
    return csbi.wAttributes


def set_color(color):
    """Sets the text color"""
    windll.kernel32.SetConsoleTextAttribute(HANDLE, color)


class Color:
    BLACK      = 0x0000
    BLUE       = 0x0001
    GREEN      = 0x0002
    CYAN       = 0x0003
    RED        = 0x0004
    MAGENTA    = 0x0005
    YELLOW     = 0x0006
    GREY       = 0x0007
    INTENSE    = 0x0008

    BG_BLACK   = 0x0000
    BG_BLUE    = 0x0010
    BG_GREEN   = 0x0020
    BG_CYAN    = 0x0030
    BG_RED     = 0x0040
    BG_MAGENTA = 0x0050
    BG_YELLOW  = 0x0060
    BG_GREY    = 0x0070
    BG_INTENSE = 0x0080

    DEFAULT    = get_color()
