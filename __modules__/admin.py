import __main__
import ctypes
import sys


def __running():
    """Checks if program is running with admin privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def __restart(file_name):
    """Restarts program with admin privileges"""
    # File name should be __file__ of executed file
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, file_name, None, 1)
    sys.exit()


def check(file_name):
    """Checks if program is running with admin privileges and restarts it if it is not"""
    if not __running():
        __restart(file_name)


if __name__ != "__main__":  # Run if admin module is not main module
    check(__main__.__file__)  # Automatically check main module at import
