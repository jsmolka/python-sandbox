DEFAULT = "\033[m"
RED     = "\033[01;31m"
GREEN   = "\033[01;32m"
YELLOW  = "\033[01;33m"
BLUE    = "\033[01;34m"
MAGENTA = "\033[01;35m"
CYAN    = "\033[01;36m"
WHITE   = "\033[01;37m"


def cli_print(text):
    """
    This function prints text in different colors. Use <c:color>text</c> for a
    different text color.
    """
    print(
        text \
        .replace("<c:red>", RED) \
        .replace("<c:green>", GREEN) \
        .replace("<c:yellow>", YELLOW) \
        .replace("<c:blue>", BLUE) \
        .replace("<c:magenta>", MAGENTA) \
        .replace("<c:cyan>", CYAN) \
        .replace("<c:white>", WHITE) \
        .replace("</c>", DEFAULT)
    )
