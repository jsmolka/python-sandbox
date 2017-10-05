class Color:
    RED     = "\033[01;31m"
    GREEN   = "\033[01;32m"
    YELLOW  = "\033[01;33m"
    BLUE    = "\033[01;34m"
    MAGENTA = "\033[01;35m"
    CYAN    = "\033[01;36m"
    WHITE   = "\033[01;37m"
    DEFAULT = "\033[m"


def c_print(text):
    """
    This function prints text in different colors.
    Use <color>text<default> for a different text color.
    """
    text = text \
        .replace("<red>", Color.RED) \
        .replace("<green>", Color.GREEN) \
        .replace("<yellow>", Color.YELLOW) \
        .replace("<blue>", Color.BLUE) \
        .replace("<magenta>", Color.MAGENTA) \
        .replace("<cyan>", Color.CYAN) \
        .replace("<white>", Color.WHITE) \
        .replace("<default>", Color.DEFAULT)

    print(text + Color.DEFAULT)
