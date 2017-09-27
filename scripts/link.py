import ctypes
import os
import sys
from pathlib import Path


def admin_check(file_name):
    """Checks if program is running with admin privileges and restarts it if it is not"""
    if not ctypes.windll.shell32.IsUserAnAdmin():  # Check if user is admin
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, file_name, None, 1)  # Restart as admin
        sys.exit()  # Exit old instance


def create_link(source, target=None):
    """Creates link"""
    if target is None:
        target = source
    os.system("mklink /d \"{0}\\{1}\" \"{0}\\OneDrive\\{2}\"".format(str(Path.home()), target, source))


admin_check(__file__)

create_link("Coding")
create_link("Studium")
create_link("Sonstiges")
create_link("Documents\\Dolphin Emulator")
create_link("Documents\\Outlook-Dateien")
create_link("Pictures")
create_link("Documents\\Settings\\Atom\\.atom", ".atom")
