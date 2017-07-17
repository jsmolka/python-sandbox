import os


def line():
    """Prints line"""
    print("-" * (os.get_terminal_size()[0] - 1))


def heading(text):
    """Prints heading"""
    length = os.get_terminal_size()[0] - 1
    text = " {0} ".format(text)
    if len(text) + 2 > length:
        raise Exception("Heading is too long")
    else:
        while len(text) < length:
            text = "-{0}-".format(text)
        print(text) if len(text) == length else print(text[0: length])


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
    # Print new line on complete
    if iteration == total:
        print()
