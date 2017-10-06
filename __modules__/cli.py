from ctypes import windll, Structure, c_short, c_ushort, byref
from math import ceil, floor
from shutil import get_terminal_size

__all__ = ["Color", "c_print", "LineStyle", "line", "heading", "big_heading",
           "menu", "progress_bar", "yes_no"]

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


def c_print(string, *colors, end=""):
    """Prints string in a different color"""
    if not colors:
        return print(string, end=end)

    color = 0x0000
    for c in colors:
        color |= c
    set_color(color)
    print(string, end=end)
    set_color(Color.DEFAULT)


class LineStyle:
    SCORE      = "-"
    UNDERSCORE = "_"
    HASH       = "#"


def terminal_size():
    """Returns terminal size"""
    return get_terminal_size()[0] - 1


def line(style=LineStyle.SCORE, color=()):
    """Draws line"""
    l = style * terminal_size()
    c_print(l, *color)


def heading(caption, style=LineStyle.HASH, color=()):
    """Draws heading"""
    size = terminal_size() - len(caption) - 2
    caption = "{0} {1} {2}".format(
        ceil(size / 2) * style,
        caption,
        floor(size / 2) * style
    )
    c_print(caption, *color)


def big_heading(caption, style=LineStyle.HASH, color=()):
    """Draws big heading"""
    line(style=style, color=color)
    heading(caption, style=style, color=color)
    line(style=style, color=color)


def menu(caption, *entries, caption_color=(), entry_color=()):
    """Draws menu"""
    if not isinstance(caption_color, tuple):
        caption_color = [caption_color]
    if not isinstance(entry_color, tuple):
        entry_color = [entry_color]

    c_print(caption, *caption_color)
    i = 0
    for entry in entries:
        i += 1
        c_print("[{0}] ".format(i) + entry, *entry_color)


def progress_bar(iteration, total, prefix="Progress:", suffix="", decimals=1, length=25, fill="█", color=()):
    """Draws progress bar"""
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = length * iteration // total
    bar = fill * filled_length + "-" * (length - filled_length - 1)
    c_print("\r%s |%s| %s%% %s" % (prefix, bar, percent, suffix), *color, end="\r")
    if iteration == total:
        print()


def yes_no(message, message_color=(), error_color=()):
    """Prints yes/no dialog"""
    c_print(message + " (y/n)", *message_color)
    while True:
        answer = input()
        if answer == "y":
            return True
        elif answer == "n":
            return False
        else:
            c_print("Invalid answer!", *error_color)


def enter(action):
    """Prints enter message"""
    input("Press enter to {0}...".format(action))


def user_input(*answers, range_=False):
    """Processes user input"""
    if not answers:
        raise Exception("Answers cannot be empty")

    if len(answers) == 1 and type(answers[0]) == list:  # Extract list
        answers = answers[0]

    if range_ and len(answers) != 2:
        raise Exception("Create range is only defines for two values in the answer list")

    answers = list(answers)
    if range_:
        if type(answers[0]) == int and type(answers[1]) == int:
            answers.sort()
            start = answers[0]
            end = answers[1] + 1
            answers = []
            for i in range(start, end):
                answers.append(i)

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
