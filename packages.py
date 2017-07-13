import ctypes
import os
import pip
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


def draw_line():
    """Prints line"""
    print("-" * (os.get_terminal_size()[0] - 1))


def draw_heading(text):
    """Prints heading"""
    cmd_length = os.get_terminal_size()[0] - 1
    text = " {0} ".format(text)
    if len(text) + 2 > cmd_length:
        raise Exception("Heading is too long")
    else:
        while len(text) < cmd_length:
            text = "-{0}-".format(text)
        if len(text) == cmd_length:
            print(text)
        else:
            text = text[0: cmd_length]
            print(text)


def dialog_enter(action, message="Press enter to {0}..."):
    """Prints enter message"""
    message = message.format(action)
    input(message)


def install(package):
    """Installs or upgrades package"""
    pip.main(["install", "--upgrade", package])


admin_check(__file__)

# List of packages
packages = [
    "Pillow",
    "NumPy",
    "OpenSimplex",
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
