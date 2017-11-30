import datetime
import getpass
import glob
import os
import pathlib
import re
import sys


def pty(path):
    """Creates valid cmd path"""
    return path.replace("/", "\\")


def depty(path):
    """Creates non valid cmd path"""
    return path.replace("\\", "/")


def __endsslash(path):
    """Returns true if path ends with a slash"""
    return True if path[-1] in ("/", "\\") else False


def deslash(path):
    """Removes trailing slash"""
    return depty(path[:-1] if __endsslash(path) else path)


def user():
    """Returns current user"""
    return getpass.getuser()


def pydir():
    """Returns script directory"""
    return depty(os.path.dirname(sys.modules["__main__"].__file__) + "\\")


USER = "C:/Users/{0}/".format(user())
DESKTOP = "{0}Desktop/".format(USER)
ONEDRIVE = "{0}OneDrive/".format(USER)
PYDIR = pydir()


def cwd():
    """Returns current working directory"""
    return depty(os.getcwd() + "\\")


def chdir(path):
    """Changes current working directory"""
    return os.chdir(path)


def isdir(src):
    """Checks if src is a directory"""
    return os.path.isdir(src)


def isfile(src):
    """Checks if src is a file"""
    return os.path.isfile(src)


def exists(src):
    """Checks if src exists"""
    return os.path.exists(src)


def filelike(path):
    """Checks if path is filelike"""
    if os.path.splitext(path)[1]:
        return True
    return False


def pathlike(path):
    """Checks if path is pathlike"""
    return not filelike(path)


def ext(file, dot=False):
    """Returns file extension"""
    ext = os.path.splitext(file)[1]
    return ext if dot else ext[1:]


def remove_ext(file):
    """Removes file extension"""
    return os.path.splitext(file)[0]


def filename(file, ext=True):
    """Returns file name"""
    file = os.path.basename(file)
    return file if ext else remove_ext(file)


def dirname(file):
    """Returns directory name of a file"""
    return depty(os.path.dirname(file) + "\\")


def abspath(file):
    """Returns absolute path for a file"""
    return depty(os.path.abspath(file))


def listdir(path):
    """Returns list of files and directories"""
    return os.listdir(path)


def isempty(path):
    """Checks if directory is empty"""
    if not listdir(path):
        return True
    return False


def date(pattern="%d-%m-%y"):
    """Returns current date"""
    today = datetime.date.today()
    return today if pattern is None else today.strftime(pattern)


def mkdirs(path):
    """Creates directories recursively"""
    if filelike(path):
        path = dirname(path)
    return os.makedirs(path)


def files(path, pattern=None, recursive=True):
    """Returns all files"""
    if pattern:
        files = []
        for rule in pattern:
            files.extend(list(glob.iglob("{0}/**/{1}".format(path, rule), recursive=recursive)))
        return files
    return list(glob.iglob("{0}/**/*.*".format(path), recursive=recursive))


def fsort(files, key=lambda x: x, reverse=False):
    """Sorts a file list based on file names"""
    return sorted(files, key=lambda x: key(filename(x)), reverse=reverse)


def __execute(cmd, stdout, stderr):
    """Executes command"""
    if not stdout:
        cmd += " >nul"
    if not stderr:
        cmd += " 2>nul"
    return os.system(cmd)


def copy(src, dst, stdout=False, stderr=True):
    """
    Copies files or directories
    /i  assume dst is a directory
    /s  copy folders and sub folders
    /h  copy hidden files and folders
    /e  copy empty folders
    /k  copy attributes
    /f  display full src and dst names
    /c  continue copying if an error occurs
    /y  overwrite files
    """
    if not exists(src):
        return 1
    if isfile(src) and filelike(dst):
        return __copy_file_to_file(src, dst, stdout, stderr)
    if isfile(src) and pathlike(dst):
        return __copy_file_to_dir(src, dst, stdout, stderr)
    if isdir(src) and pathlike(dst):
        return __copy_dir_to_dir(src, dst, stdout, stderr)


def __copy_file_to_file(src, dst, stdout, stderr):
    """Copies file to file"""
    cmd = "ECHO D | xcopy \"{0}\" \"{1}\" /y".format(pty(src), pty(dst))
    return __execute(cmd, stdout, stderr)


def __copy_file_to_dir(src, dst, stdout, stderr):
    """Copies file to directory"""
    if not __endsslash(dst):
        dst += "\\"
    cmd = "ECHO V | xcopy \"{0}\" \"{1}\" /y".format(pty(src), pty(dst))
    return __execute(cmd, stdout, stderr)


def __copy_dir_to_dir(src, dst, stdout, stderr):
    """Copies directory to directory"""
    if __endsslash(src):
        src = src[:-1]
    if __endsslash(dst):
        dst = dst[:-1]
    cmd = "xcopy \"{0}\" \"{1}\" /y/i/s/h/e/k/f/c".format(pty(src), pty(dst))
    return __execute(cmd, stdout, stderr)


def move(src, dst, stdout=False, stderr=True):
    """
    Moves files or directories
    /y  overwrite files
    """
    if not exists(src):
        return 1
    if not exists(dst):
        mkdirs(dst)
    if isfile(src) and filelike(dst):
        return __move_file_to_file(src, dst, stdout, stderr)
    if isfile(src) and pathlike(dst):
        return __move_file_to_dir(src, dst, stdout, stderr)
    if isdir(src) and pathlike(dst):
        return __move_dir_to_dir(src, dst, stdout, stderr)


def __move_file_to_file(src, dst, stdout, stderr):
    """Moves file to file"""
    cmd = "move /y \"{0}\" \"{1}\"".format(pty(src), pty(dst))
    return __execute(cmd, stdout, stderr)


def __move_file_to_dir(src, dst, stdout, stderr):
    """Moves file to directory"""
    if not __endsslash(dst):
        dst += "\\"
    cmd = "move /y \"{0}\" \"{1}\"".format(pty(src), pty(dst))
    return __execute(cmd, stdout, stderr)


def __move_dir_to_dir(src, dst, stdout, stderr):
    """Moves directory to directory"""
    if __endsslash(src):
        src = src[:-1]
    if __endsslash(dst):
        dst = dst[:-1]
    cmd = "move /y \"{0}\" \"{1}\"".format(pty(src), pty(dst))
    return __execute(cmd, stdout, stderr)


def remove(src, stdout=False, stderr=True):
    """Removes files or directories"""
    if not exists(src):
        return 1
    if isfile(src):
        return __remove_file(src, stdout, stderr)
    else:
        return __remove_dir(src, stdout, stderr)


def __remove_file(src, stdout, stderr):
    """Removes file"""
    cmd = "del \"{0}\"".format(pty(src))
    return __execute(cmd, stdout, stderr)


def __remove_dir(src, stdout, stderr):
    """Removes directory"""
    if __endsslash(src):
        src = src[:-1]
    cmd = "rd \"{0}\" /s/q".format(pty(src))
    return __execute(cmd, stdout, stderr)


def remove_empty_dirs(path):
    """Removes empty folders recursively"""
    if not isdir(path):
        return
    folders = listdir(path)
    if folders:
        for folder in folders:
            full_path = os.path.join(path, folder)
            if isdir(full_path):
                remove_empty_dirs(full_path)
    if isempty(path):
        remove(path)


def regex(files, pattern, ext=True):
    """
    Filters files with regular expressions
    .       match any character
    *       match any repetition of characters (.* any sequence)
    \       escape following character
    ^       start of string
    $       end of string
    ()      enclose expression
    [A-Z]   sequence of characters
    {m, n}  characters must appear m to n times
    (?:1|2) must be one of the options
    """
    matching = []
    other = []
    for file in files:
        if re.match(r"{0}".format(pattern), filename(file, ext=ext)):
            matching.append(file)
        else:
            other.append(file)
    return matching, other


def remove_duplicates(files):
    """Removes duplicate files"""
    test = set([filename(file) for file in files])
    if len(test) == len(files):
        return files

    result = []
    for i in range(0, len(files)):
        duplicate = False
        for j in range(i + 1, len(files)):
            if filename(files[i]) == filename(files[j]):
                duplicate = True
        if not duplicate:
            result.append(files[i])
    return result


def back(path):
    """Goes one folder back"""
    return depty(str(pathlib.Path(path).parent) + "\\")


def symlink(src, dst, stdout=False, stderr=True):
    """Creates symbolic link"""
    parent = back(dst)
    if not exists(parent):
        mkdirs(parent)
    cmd = "mklink /d \"{0}\" \"{1}\"".format(pty(dst), pty(src))
    return __execute(cmd, stdout, stderr)


def lzma(dst, *src, stdout=False, stderr=True):
    """Creates a lzma archive"""
    cmd = "7z a -t7z -m0=lzma2 -mx=9 -aoa -mfb=64 -md=32m -ms=on -mhe \"{0}\"{1}"
    files = ""
    for path in src:
        files += " \"{0}\"".format(pty(path))
    return __execute(cmd.format(pty(dst), files), stdout, stderr)
