import admin
import os


def create_link(source, target=None):
    """Creates link"""
    if target is None:
        target = source
    os.system("mklink /d \"C:\\Users\\Julian\\{0}\" \"C:\\Users\\Julian\\OneDrive\\{1}\"".format(target, source))


create_link("Coding")
create_link("Studium")
create_link("Sonstiges")
create_link("Documents\\Dolphin Emulator")
create_link("Documents\\Outlook-Dateien")
create_link("Pictures")
