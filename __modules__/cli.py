import ctypes as ct
import math
import shutil

SHORT = ct.c_short
WORD = ct.c_ushort


class COORD(ct.Structure):
    """
    Coordinate structure.
    """
    _fields_ = [
        ("X", SHORT),
        ("Y", SHORT)]


class SMALL_RECT(ct.Structure):
    """
    Small rectangle structure.
    """
    _fields_ = [
        ("Left", SHORT),
        ("Top", SHORT),
        ("Right", SHORT),
        ("Bottom", SHORT)]


class CONSOLE_SCREEN_BUFFER_INFO(ct.Structure):
    """
    Console screen buffer info structure.
    """
    _fields_ = [
        ("dwSize", COORD),
        ("dwCursorPosition", COORD),
        ("wAttributes", WORD),
        ("srWindow", SMALL_RECT),
        ("dwMaximumWindowSize", COORD)]


STD_HANDLE = ct.windll.kernel32.GetStdHandle(-11)


def get_color():
    """
    Returns the current text color.

    :return: current text color
    """
    csbi = CONSOLE_SCREEN_BUFFER_INFO()
    ct.windll.kernel32.GetConsoleScreenBufferInfo(STD_HANDLE, ct.byref(csbi))
    return csbi.wAttributes


def set_color(color):
    """
    Sets the text color.

    :param color: color to set
    :return: None
    """
    ct.windll.kernel32.SetConsoleTextAttribute(STD_HANDLE, color)


class Color:
    """
    Color class.
    """
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
    """
    Style class.
    """
    SCORE      = "-"
    UNDERSCORE = "_"
    HASH       = "#"
    BLOCK      = "█"


def mix_colors(*colors):
    """
    Mixes colors.

    :param colors: colors to mix
    :return: hex
    """
    color = 0x0000
    for clr in colors:
        color |= clr
    return color


def cprint(*values, end="\n", color=()):
    """
    Prints string in a different color.

    :param values: values to print
    :param end: last character
    :param color: color to print in
    :return: None
    """
    if not color:
        return print(*values, end=end)
    set_color(mix_colors(*color))
    print(*values, end=end)
    set_color(Color.DEFAULT)


def terminal_size():
    """
    Returns terminal size

    :return: int
    """
    return shutil.get_terminal_size()[0] - 1


def line(style=Style.SCORE, color=()):
    """
    Draws line.

    :param style: style to use
    :param color: color to use
    :return: None
    """
    cprint(style * terminal_size(), color=color)


def heading(caption, style=Style.HASH, color=()):
    """
    Draws heading.

    :param caption: caption to print
    :param style: style to use
    :param color: color to use
    :return: None
    """
    half = (terminal_size() - len(caption) - 2) / 2
    cprint(math.ceil(half) * style, caption, math.floor(half) * style, color=color)


def big_heading(caption, style=Style.HASH, color=()):
    """
    Draws big heading.

    :param caption: caption to print
    :param style: style to use
    :param color: color to use
    :return: None
    """
    line(style=style, color=color)
    heading(caption, style=style, color=color)
    line(style=style, color=color)


def cinput(*answers, message=None, span=False, color=()):
    """
    Processes a controlled input.

    :param answers: possible answers
    :param message: message to print
    :param span: possible range
    :param color: color to use
    :return: answer
    """
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
                cprint("Invalid answer. Try again.", color=color)
        except Exception:
            cprint("Invalid answer. Try again.", color=color)


def tinput(input_type, message=None, color=()):
    """
    Processes a type input.

    :param input_type: type to cast to
    :param message: message to print
    :param color: color to use
    :return: answer of type
    """
    if message:
        cprint(message, color=color)
    while True:
        try:
            return input_type(input())
        except Exception:
            cprint("Invalid answer. Try again.", color=color)


def menu(caption, *entries, result=False, color=()):
    """
    Draws menu.

    :param caption: caption for menu
    :param entries: entries in menu
    :param result: return result
    :param color: color to use
    :return: result
    """
    cprint(caption, color=color)
    for idx, entry in enumerate(entries, start=1):
        cprint("[{0}] {1}".format(idx, entry), color=color)
    if result:
        return cinput(1, len(entries), span=True, color=color) - 1


def progress_bar(iteration, total, prefix="Progress:", suffix="", decimals=1, length=25, style=Style.BLOCK, color=()):
    """
    Draws progress bar.

    :param iteration: current iteration
    :param total: total iterations
    :param prefix: prefix
    :param suffix: suffix
    :param decimals: showed decimals
    :param length: progress bar length
    :param style: style to use
    :param color: color to use
    :return: None
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = length * iteration // total
    bar = style * filled_length + "-" * (length - filled_length - 1)
    cprint("\r%s |%s| %s%% %s" % (prefix, bar, percent, suffix), color=color, end="\r")
    if iteration == total:
        print()


def question(message, color=()):
    """
    Prints yes/no dialog.

    :param message: question
    :param color: color to use
    :return: boolean
    """
    cprint(message + " (y/n)", color=color)
    while True:
        answer = input()
        if answer == "y":
            return True
        elif answer == "n":
            return False
        else:
            cprint("Invalid answer. Try again.", color=color)


def enter(action, color=()):
    """
    Prints enter message.

    :param action: action for entering
    :param color: color to use
    :return: None
    """
    cprint("Press enter to {0}...".format(action), color=color, end="")
    input()
