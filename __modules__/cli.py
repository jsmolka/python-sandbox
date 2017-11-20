from ctypes import windll, Structure, c_short, c_ushort, byref
from math import ceil, floor
from shutil import get_terminal_size

__all__ = [
    "Color",
    "Style",
    "cprint",
    "line",
    "heading",
    "big_heading",
    "cinput",
    "tinput",
    "menu",
    "progress_bar",
    "question",
    "enter"
]

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


class Style:
    SCORE      = "-"
    UNDERSCORE = "_"
    HASH       = "#"


def cprint(*values, end="\n", color=None):
    """Prints string in a different color"""
    if color is None:
        return print(*values, end=end)
    clr = 0x0000
    for c in color:
        clr |= c
    set_color(clr)
    print(*values, end=end)
    set_color(Color.DEFAULT)


def terminal_size():
    """Returns terminal size"""
    return get_terminal_size()[0] - 1


def line(style=Style.SCORE, color=None):
    """Draws line"""
    cprint(style * terminal_size(), color=color)


def heading(caption, style=Style.HASH, color=None):
    """Draws heading"""
    half = (terminal_size() - len(caption) - 2) / 2
    cprint(ceil(half) * style, caption, floor(half) * style, color=color)


def big_heading(caption, style=Style.HASH, color=None):
    """Draws big heading"""
    line(style=style, color=color)
    heading(caption, style=style, color=color)
    line(style=style, color=color)


def cinput(*answers, message=None, span=False, color=None):
    """Processes a controlled input"""
    if message:
        cprint(message, color=color)
    if span:
        answers = range(answers[0], answers[1] + 1)
    while True:
        try:
            answer = type(answers[0])(input())
            if answer in answers:
                return answer
            else:
                cprint("Invalid answer! Try again!", color=color)
        except:
            cprint("Invalid answer! Try again!", color=color)


def tinput(input_type, message=None, color=None):
    """Processes a type input"""
    if message:
        cprint(message, color=color)
    while True:
        try:
            return input_type(input())
        except:
            cprint("Invalid answer! Try again!", color=color)


def menu(caption, *entries, result=False, color=None):
    """Draws menu"""
    cprint(caption, color=color)
    for index in range(0, len(entries)):
        cprint("[{0}] {1}".format(index + 1, entries[index]), color=color)
    if result:
        return cinput(1, len(entries), span=True, color=color) - 1



def progress_bar(iteration, total, prefix="Progress:", suffix="", decimals=1, length=25, fill="█", color=None):
    """Draws progress bar"""
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = length * iteration // total
    bar = fill * filled_length + "-" * (length - filled_length - 1)
    cprint("\r%s |%s| %s%% %s" % (prefix, bar, percent, suffix), color=color, end="\r")
    if iteration == total:
        print()


def question(message, color=None):
    """Prints yes/no dialog"""
    cprint(message + " (y/n)", color=color)
    while True:
        answer = input()
        if answer == "y":
            return True
        elif answer == "n":
            return False
        else:
            cprint("Invalid answer! Try again!", color=color)


def enter(action, color=None):
    """Prints enter message"""
    cprint("Press enter to {0}...".format(action), color=color, end="")
    input()
