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


def add_path(path, variable):
    """Adds path to system variable"""
    if variable in os.environ:
        if path not in os.environ[variable].split(";"):
            Popen(["setx", variable, os.environ.get(variable) + ";" + path], stdout=DEVNULL, stderr=STDOUT)
    else:
        Popen(["setx", variable, path], stdout=DEVNULL, stderr=STDOUT)


def install_package(package):
    """Installs or upgrades package"""
    pip.main(["install", "--upgrade", package])


admin_check(__file__)

module_path = os.path.dirname(__file__) + "\\__modules__"
add_path(module_path, "PYTHONPATH")

packages = [
    "Pillow",
    "NumPy",
    "Pyglet",
    "OpenSimplex"
]
for pkg in packages:
    draw_heading(pkg)
    install_package(pkg)

draw_heading("PyProcessing")
os.chdir("__packages__/pyprocessing")
os.system("pip install .")

draw_heading("Maze")
os.chdir("../maze")
os.system("pip install .")

draw_line()

dialog_enter("exit")
