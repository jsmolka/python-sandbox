import platform


def __default():
    """Calculates default line for windows version"""
    system = platform.release()
    if system == "7":
        default_line = "-" * 79
    else:
        default_line = "-" * 119
    return default_line


def line():
    """Prints line"""
    default_line = __default()
    print(default_line)


def heading(text):
    """Prints heading"""
    default_line = __default()
    line_length = len(default_line)
    text = " {0} ".format(text)
    text_length = len(text)
    if (text_length + 2) > line_length:
        raise Exception("Heading is too long")
    else:
        while text_length < line_length:
            text = "-{0}-".format(text)
            text_length = len(text)
        if text_length == line_length:
            print(text)
        else:
            text = text[0: text_length - 1]
            print(text)


def menu(caption, *items):
    """Prints menu"""
    if not items:
        raise Exception("Items cannot be empty")

    if len(items) == 1 and type(items[0]) == list:  # Extract list
        items = items[0]

    print(caption)
    index = 1
    for item in items:
        print("{0}: {1}".format(index, item))
        index += 1


def progress_bar(iteration, total, prefix="Progress:", suffix="", decimals=1, length=25, fill='█'):
    """Prints progress bar"""
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + "-" * (length - filled_length - 1)
    print("\r%s |%s| %s%% %s" % (prefix, bar, percent, suffix), end="\r")
    # Print New Line on Complete
    if iteration == total:
        print()
