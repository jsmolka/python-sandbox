import __main__
import ctypes
import sys


def check(file_name):
    """Checks if program is running with admin privileges and restarts it if it is not"""
    if not ctypes.windll.shell32.IsUserAnAdmin():  # Check if user is admin
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, file_name, None, 1)  # Restart as admin
        sys.exit()  # Exit old instance


if __name__ != "__main__":  # Run if admin module is not main module
    check(__main__.__file__)  # Automatically check main module at import
