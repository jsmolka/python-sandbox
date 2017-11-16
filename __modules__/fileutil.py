import getpass
import glob
import inspect
import os
import shutil


def cwd():
    """Returns current working directory"""
    return os.getcwd()


def chdir(path):
    """Changes current working directory"""
    os.chdir(path)


def cdir():
    """Returns script directory"""
    return os.path.dirname((inspect.getfile(inspect.currentframe())))


def user():
    """Returns current user name"""
    return getpass.getuser()


USER_DIR = "C:/Users/{0}/".format(user())
DESKTOP_DIR = "{0}/Desktop/".format(USER_DIR)
ONEDRIVE_DIR = "{0}/OneDrive/".format(USER_DIR)


def isdir(src):
    """Checks if src is a directory"""
    return os.path.isdir(src)


def isfile(src):
    """Checks if src is a file"""
    return os.path.isfile(src)


def exists(src):
    """Checks if src exists"""
    return os.path.exists(src)


def mkdirs(path):
    """Creates directories recursively"""
    os.makedirs(path)


def files(path=cwd(), filter=None, recursive=True):
    """Returns all files"""
    if filter:
        files = []
        for rule in filter:
            files.extend(glob.iglob("{0}/**/{1}".format(path, rule), recursive=recursive))
        return files  # Returns files ordered by filter
    return list(glob.iglob("{0}/**/*.*".format(path), recursive=recursive))


def ext(file, dot=False):
    """Returns file extension"""
    ext = os.path.splitext(file)[1]
    return ext if dot else ext[1:]


def remove_ext(file):
    """Returns file without extension"""
    return os.path.splitext(file)[0]


def file_name(file, ext=True):
    """Returns file name"""
    file = os.path.basename(file)
    return file if ext else remove_ext(file)


def dir_name(file):
    """Returns the directory name of a file"""
    return os.path.dirname(file)


def abs_path(file):
    """Returns absolute path for a file"""
    return os.path.abspath(file)


def sort_by(files, key=lambda x: x, reverse=False):
    """Sorts a file list by criteria"""
    return sorted(files, key=lambda x: key(file_name(x)), reverse=reverse)


def copy(src, dst):
    """Copies files from one place to another"""
    if not exists(src):
        raise Exception("{0} does no exist".format(src))
    if isfile(src):
        if not exists(dst):
            mkdirs(dst)
        shutil.copy(src, dst)
    else:
        shutil.copytree(src, dst)


def move(src, dst):
    """Moves files form one place to another"""
    if not exists(src):
        raise Exception("{0} does not exist".format(src))
    if not exists(dst):
        mkdirs(dst)
    shutil.move(src, dst)


def remove(src):
    """Removes file or files from a directory"""
    if not exists(src):
        raise Exception("{0} does not exist".format(src))
    if isfile(src):
        os.remove(src)
    else:
        shutil.rmtree(src)
