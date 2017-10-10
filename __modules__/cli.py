from ctypes import windll, Structure, c_short, c_ushort, byref
from math import ceil, floor
from shutil import get_terminal_size

__all__ = ["Color", "c_print", "LineStyle", "line", "heading", "big_heading",
           "menu", "progress_bar", "yes_no", "enter", "user_input"]

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


def c_print(string, *color, end="\n"):
    """Prints string in a different color"""
    if not color:
        return print(string, end=end)

    clr = 0x0000
    for c in color:
        clr |= c
    set_color(clr)
    print(string, end=end)
    set_color(Color.DEFAULT)


def iterable(color):
    """Creates iterable color"""
    if color == Color.DEFAULT:
        color = []
    elif not isinstance(color, list):
        color = [color]
    return color


class LineStyle:
    SCORE      = "-"
    UNDERSCORE = "_"
    HASH       = "#"


def terminal_size():
    """Returns terminal size"""
    return get_terminal_size()[0] - 1


def line(style=LineStyle.SCORE, color=Color.DEFAULT):
    """Draws line"""
    l = style * terminal_size()
    color = iterable(color)
    c_print(l, *color)


def heading(caption, style=LineStyle.HASH, color=Color.DEFAULT):
    """Draws heading"""
    size = terminal_size() - len(caption) - 2
    caption = "{0} {1} {2}".format(
        ceil(size / 2) * style,
        caption,
        floor(size / 2) * style
    )
    color = iterable(color)
    c_print(caption, *color)


def big_heading(caption, style=LineStyle.HASH, color=Color.DEFAULT):
    """Draws big heading"""
    color = iterable(color)
    line(style=style, color=color)
    heading(caption, style=style, color=color)
    line(style=style, color=color)


def menu(caption, *entries, caption_color=Color.DEFAULT, entry_color=Color.DEFAULT):
    """Draws menu"""
    caption_color = iterable(caption_color)
    entry_color = iterable(entry_color)
    c_print(caption, *caption_color)
    for i in range(0, len(entries)):
        c_print("[{0}] ".format(i + 1) + entries[i], *entry_color)


def progress_bar(iteration, total, prefix="Progress:", suffix="", decimals=1, length=25, fill="█", color=Color.DEFAULT):
    """Draws progress bar"""
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = length * iteration // total
    bar = fill * filled_length + "-" * (length - filled_length - 1)
    color = iterable(color)
    c_print("\r%s |%s| %s%% %s" % (prefix, bar, percent, suffix), *color, end="\r")
    if iteration == total:
        print()


def yes_no(message, message_color=Color.DEFAULT, error_color=Color.DEFAULT):
    """Prints yes/no dialog"""
    message_color = iterable(message_color)
    error_color = iterable(error_color)
    c_print(message + " (y/n)", *message_color)
    while True:
        answer = input()
        if answer == "y":
            return True
        elif answer == "n":
            return False
        else:
            c_print("Invalid answer!", *error_color)


def enter(action, color=Color.DEFAULT):
    """Prints enter message"""
    color = iterable(color)
    c_print(action, *color, end="")
    input()


def user_input(*answers, span=False):
    """Processes user input"""
    if span:
        answers = range(answers[0], answers[1])
    answer_type = type(answers[0])
    while True:
        answer = input()
        try:
            answer = answer_type(answer)
            if answer in answers:
                return answer
            else:
                print("Invalid answer! Try again!")
        except:
            print("Invalid answer! Try again!")
