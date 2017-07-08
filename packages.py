import ctypes
import os
import pip
import platform
import sys


def admin___running():
    """Checks if program is running with admin privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def admin___restart(file_name):
    """Restarts program with admin privileges"""
    # File name should be __file__ of executed file
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, file_name, None, 1)
    sys.exit()


def admin_check(file_name):
    """Checks if program is running with admin privileges and restarts it if it is not"""
    if not admin___running():
        admin___restart(file_name)


def dialog_enter(action, message="Press enter to {0}..."):
    """Prints enter message"""
    message = message.format(action)
    input(message)


def draw___default():
    """Calculates default line for windows version"""
    system = platform.release()
    if system == "7":
        default_line = "-" * 79
    else:
        default_line = "-" * 119
    return default_line


def draw_line():
    """Prints line"""
    default_line = draw___default()
    print(default_line)


def draw_heading(text):
    """Prints heading"""
    default_line = draw___default()
    line_length = len(default_line)
    text = " {0} ".format(text)
    text_length = len(text)
    if (text_length + 2) > line_length:
        print("Heading is too long!")
    else:
        while text_length < line_length:
            text = "-{0}-".format(text)
            text_length = len(text)
        if text_length == line_length:
            print(text)
        else:
            text = text[0: text_length - 1]
            print(text)


def install(package):
    """Installs or upgrades package"""
    pip.main(["install", "--upgrade", package])


admin_check(__file__)

# List of packages
packages = [
    "Pillow",
    "NumPy",
    "OpenSimplex",
    "Panda3D",
    "Pyglet"
]

# Install or upgrade external packages
for package in packages:
    draw_heading(package)
    install(package)

# Install local packages
draw_heading("PyProcessing")
os.chdir("__packages__/pyprocessing")
os.system("pip install .")

draw_line()

dialog_enter("exit")
