import ctypes
import os
import pip
import sys
from subprocess import Popen, DEVNULL, STDOUT


def admin_check(file_name):
    """Checks if program is running with admin privileges and restarts it if it is not"""
    if not ctypes.windll.shell32.IsUserAnAdmin():  # Check if user is admin
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, file_name, None, 1)  # Restart as admin
        sys.exit()  # Exit old instance


def draw_line():
    """Prints line"""
    print("-" * (os.get_terminal_size()[0] - 1))


def draw_heading(text):
    """Prints heading"""
    length = os.get_terminal_size()[0] - 1
    text = " {0} ".format(text)
    if len(text) + 2 > length:
        raise Exception("Heading is too long")
    else:
        while len(text) < length:
            text = "-{0}-".format(text)
        print(text) if len(text) == length else print(text[0: length])


def dialog_enter(action, message="Press enter to {0}..."):
    """Prints enter message"""
    message = message.format(action)
    input(message)


def add_path(pth):
    """Adds path to PYTHONPATH"""
    if "PYTHONPATH" in os.environ:
        if pth not in os.environ["PYTHONPATH"].split(";"):
            Popen(["setx", "PYTHONPATH", os.environ.get("PYTHONPATH") + ";" + path], stdout=DEVNULL, stderr=STDOUT)
    else:
        Popen(["setx", "PYTHONPATH", path], stdout=DEVNULL, stderr=STDOUT)


def install_package(pkg):
    """Installs or upgrades package"""
    pip.main(["install", "--upgrade", pkg])


admin_check(__file__)

# List of paths
paths = [
    os.path.dirname(__file__) + "\\__modules__"
]

# List of packages
packages = [
    "Pillow",
    "NumPy",
    "Pyglet",
    "OpenSimplex"
]

# Add paths to PYTHONPATH
for path in paths:
    add_path(path)

# Install or upgrade external packages
for package in packages:
    draw_heading(package)
    install_package(package)

# Install local packages
draw_heading("PyProcessing")
os.chdir("__packages__/pyprocessing")
os.system("pip install .")

draw_line()

dialog_enter("exit")
