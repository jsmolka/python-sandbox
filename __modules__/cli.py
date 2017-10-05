class Color:
    red     = "\033[01;31m"
    green   = "\033[01;32m"
    yellow  = "\033[01;33m"
    blue    = "\033[01;34m"
    magenta = "\033[01;35m"
    cyan    = "\033[01;36m"
    white   = "\033[01;37m"
    default = "\033[m"


def c_print(text):
    """
    This function prints text in different colors.
    Use <color>text<default> for a different text color.
    """
    text = text \
        .replace("<red>", Color.red) \
        .replace("<green>", Color.green) \
        .replace("<yellow>", Color.yellow) \
        .replace("<blue>", Color.blue) \
        .replace("<magenta>", Color.magenta) \
        .replace("<cyan>", Color.cyan) \
        .replace("<white>", Color.white) \
        .replace("<default>", Color.default)

    print(text + Color.default)
