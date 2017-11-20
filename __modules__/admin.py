import ctypes
import sys


def check(file_name):
    """Checks if program is running with admin privileges and restarts it if it is not"""
    if not ctypes.windll.shell32.IsUserAnAdmin():  # Check if user is admin
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, file_name, None, 1)  # Restart as admin
        sys.exit()  # Exit old instance
