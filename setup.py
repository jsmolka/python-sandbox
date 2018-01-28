import ctypes
import os
import pip
import sys


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


def add_to_env(env, pth):
    """Adds path to system environment"""
    if env in os.environ:
        if pth not in os.environ[env].split(";"):
            os.system("setx {0} \"%{0}%;{1}\" >nul 2>nul".format(env, pth))
    else:
        os.system("setx {0} \"{1}\" >nul 2>nul".format(env, pth))


def install_package(package):
    """Installs or upgrades package"""
    pip.main(["install", "--upgrade", package])


admin_check(__file__)

module_path = os.path.dirname(__file__) + "\\__modules__"
add_to_env("PYTHONPATH", module_path)

packages = [
    "Pillow",
    "NumPy",
    "Pyglet",
    "OpenSimplex"
]
for pkg in packages:
    draw_heading(pkg)
    install_package(pkg)

draw_line()

dialog_enter("exit")
