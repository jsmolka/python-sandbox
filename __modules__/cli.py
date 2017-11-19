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


def c_print(*values, end="\n", color=None):
    """Prints string in a different color"""
    if color is None:
        return print(*values, end=end)
    clr = 0x0000
    for c in color:
        clr |= c
    set_color(clr)
    print(*values, end=end)
    set_color(Color.DEFAULT)


class LineStyle:
    SCORE      = "-"
    UNDERSCORE = "_"
    HASH       = "#"


def terminal_size():
    """Returns terminal size"""
    return get_terminal_size()[0] - 1


def line(style=LineStyle.SCORE, color=None):
    """Draws line"""
    l = style * terminal_size()
    c_print(l, color=color)


def heading(caption, style=LineStyle.HASH, color=None):
    """Draws heading"""
    size = terminal_size() - len(caption) - 2
    caption = "{0} {1} {2}".format(
        ceil(size / 2) * style,
        caption,
        floor(size / 2) * style
    )
    c_print(caption, color=color)


def big_heading(caption, style=LineStyle.HASH, color=None):
    """Draws big heading"""
    line(style=style, color=color)
    heading(caption, style=style, color=color)
    line(style=style, color=color)


def user_input(*answers, span=False, color=None):
    """Processes user input"""
    if span:
        answers = range(answers[0], answers[1] + 1)
    answer_type = type(answers[0])
    while True:
        answer = input()
        try:
            answer = answer_type(answer)
            if answer in answers:
                return answer
            else:
                c_print("Invalid answer! Try again!", color=color)
        except:
            c_print("Invalid answer! Try again!", color=color)


def menu(caption, *entries, result=False, color=None):
    """Draws menu"""
    c_print(caption, color=color)
    for i in range(0, len(entries)):
        c_print("[{0}] {1}".format(i + 1, entries[i]), color=color)
    if result:
        return user_input(1, len(entries), span=True, color=color) - 1



def progress_bar(iteration, total, prefix="Progress:", suffix="", decimals=1, length=25, fill="█", color=None):
    """Draws progress bar"""
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = length * iteration // total
    bar = fill * filled_length + "-" * (length - filled_length - 1)
    c_print("\r%s |%s| %s%% %s" % (prefix, bar, percent, suffix), color=color, end="\r")
    if iteration == total:
        print()


def yes_no(message, color=None):
    """Prints yes/no dialog"""
    c_print(message + " (y/n)", color=color)
    while True:
        answer = input()
        if answer == "y":
            return True
        elif answer == "n":
            return False
        else:
            c_print("Invalid answer!", color=color)


def enter(action, color=None):
    """Prints enter message"""
    c_print("Press enter to {0}...".format(action), color=color, end="")
    input()



