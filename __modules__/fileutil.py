import getpass
import glob
import inspect
import os
import shutil


def cwd():
    "Returns current working directory"
    return os.getcwd()


def script_dir():
    """Returns script directory"""
    return os.path.dirname((inspect.getfile(inspect.currentframe())))


def user():
    """Returns current user name"""
    return getpass.getuser()


USER_DIR = "C:/Users/{0}".format(user())
ONEDRIVE_DIR = "{0}/OneDrive".format(USER_DIR)


def files(path=cwd(), filter=None, recursive=True):
    """Returns all files"""
    if filter:
        files = []
        for rule in filter:
            files.extend(glob.iglob("{0}/**/{1}".format(path, rule), recursive=recursive))
        return files  # Returns files ordered by filter
    return list(glob.iglob("{0}/**/*.*".format(path), recursive=recursive))


def file_ext(file, dot=False):
    """Returns file extension"""
    ext = os.path.splitext(file)[1]
    return ext if dot else ext[1:]


def remove_file_ext(file):
    """Returns file without extension"""
    return os.path.splitext(file)[0]


def file_name(file, ext=True):
    """Returns file name"""
    file = os.path.basename(file)
    return file if ext else remove_file_ext(file)


def abs_path(file):
    """Returns absolute path for a file"""
    return os.path.abspath(file)


def sort_by(files, key=lambda x: x, reverse=False):
    """Sorts a file list by criteria"""
    return sorted(files, key=lambda x: key(file_name(x)), reverse=reverse)
