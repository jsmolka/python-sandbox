from ctypes import windll, Structure, c_short, c_ushort, byref

__all__ = ["Color", "c_print"]

SHORT = c_short
WORD = c_ushort


class COORD(Structure):
    _fields_ = [
        ("X", SHORT),
        ("Y", SHORT)]


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


stdout_handle = windll.kernel32.GetStdHandle(-11)
SetConsoleTextAttribute = windll.kernel32.SetConsoleTextAttribute
GetConsoleScreenBufferInfo = windll.kernel32.GetConsoleScreenBufferInfo


def get_color():
    """Returns the current text color"""
    csbi = CONSOLE_SCREEN_BUFFER_INFO()
    GetConsoleScreenBufferInfo(stdout_handle, byref(csbi))
    return csbi.wAttributes


def set_color(color):
    """Sets the text color"""
    SetConsoleTextAttribute(stdout_handle, color)


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


def c_print(string, *colors):
    """Prints string in a different color"""
    if not colors:
        return print(string)

    color = 0x0000
    for c in colors:
        color |= c
    set_color(color)
    print(string)
    set_color(Color.DEFAULT)


class LineType:
    SCORE      = "-"
    UNDERSCORE = "_"
    HASH       = "#"
