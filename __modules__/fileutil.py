import datetime
import getpass
import glob
import inspect
import os
import re


def user():
    """Returns current user"""
    return getpass.getuser()


USER = "C:/Users/{0}/".format(user())
DESKTOP = "{0}Desktop/".format(USER)
ONEDRIVE = "{0}OneDrive/".format(USER)


def cwd():
    """Returns current working directory"""
    return os.getcwd()


def chdir(path):
    """Changes current working directory"""
    return os.chdir(path)


def pydir():
    """Returns script directory"""
    return os.path.dirname((inspect.getfile(inspect.currentframe())))


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
    return os.path.dirname(file)


def abspath(file):
    """Returns absolute path for a file"""
    return os.path.abspath(file)


def listdir(path):
    """Returns list of files and directories"""
    return os.listdir(path)


def isempty(path):
    """Checks if directory is empty"""
    if not listdir(path):
        return True
    return False


def pty(path):
    """Creates valid cmd path"""
    return path.replace("/", "\\")


def date(form="%d-%m-%y"):
    """Returns current date string"""
    today = datetime.date.today()
    return today if form is None else today.strftime(form)


def execute(cmd, suppress=False):
    """Executes a command"""
    return os.system(cmd + " >nul" if suppress else cmd)


def mkdirs(path):
    """Creates directories recursively"""
    if filelike(path):
        path = dirname(path)
    if not path[-1] in ("/", "\\"):
        path += "\\"
    os.makedirs(path)


def files(path, filter=None, recursive=True):
    """Returns all files"""
    if filter:
        files = []
        for rule in filter:
            files.extend(list(glob.iglob("{0}/**/{1}".format(path, rule), recursive=recursive)))
        return files
    return list(glob.iglob("{0}/**/*.*".format(path), recursive=recursive))


def fsort(files, key=lambda x: x, reverse=False):
    """Sorts a file list based on file names"""
    return sorted(files, key=lambda x: key(filename(x)), reverse=reverse)


def copy(src, dst, suppress=True):
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
        return __copy_file_to_file(src, dst, suppress)
    if isfile(src) and pathlike(dst):
        return __copy_file_to_dir(src, dst, suppress)
    if isdir(src) and pathlike(dst):
        return __copy_dir_to_dir(src, dst, suppress)


def __copy_file_to_file(src, dst, suppress):
    """Copies file to file"""
    cmd = "ECHO D | xcopy \"{0}\" \"{1}\" /y".format(pty(src), pty(dst))
    return execute(cmd, suppress=suppress)


def __copy_file_to_dir(src, dst, suppress):
    """Copies file to directory"""
    if not dst[-1] in ("/", "\\"):
        dst += "\\"
    cmd = "ECHO V | xcopy \"{0}\" \"{1}\" /y".format(pty(src), pty(dst))
    return execute(cmd, suppress=suppress)


def __copy_dir_to_dir(src, dst, suppress):
    """Copies directory to directory"""
    if src[-1] in ("/", "\\"):
        src = src[:-1]
    if dst[-1] in ("/", "\\"):
        dst = dst[:-1]
    cmd = "xcopy \"{0}\" \"{1}\" /y/i/s/h/e/k/f/c".format(pty(src), pty(dst))
    return execute(cmd, suppress=suppress)


def move(src, dst, suppress=True):
    """
    Moves files or directories
    /y  overwrite files
    """
    if not exists(src):
        return 1
    if not exists(dst):
        mkdirs(dst)
    if isfile(src) and filelike(dst):
        return __move_file_to_file(src, dst, suppress)
    if isfile(src) and pathlike(dst):
        return __move_file_to_dir(src, dst, suppress)
    if isdir(src) and pathlike(dst):
        return __move_dir_to_dir(src, dst, suppress)


def __move_file_to_file(src, dst, suppress):
    """Moves file to file"""
    cmd = "move /y \"{0}\" \"{1}\"".format(pty(src), pty(dst))
    return execute(cmd, suppress=suppress)


def __move_file_to_dir(src, dst, suppress):
    """Moves file to directory"""
    if not dst[-1] in ("/", "\\"):
        dst += "\\"
    cmd = "move /y \"{0}\" \"{1}\"".format(pty(src), pty(dst))
    return execute(cmd, suppress=suppress)


def __move_dir_to_dir(src, dst, suppress):
    """Moves directory to directory"""
    if src[-1] in ("/", "\\"):
        src = src[:-1]
    if dst[-1] in ("/", "\\"):
        dst = dst[:-1]
    cmd = "move /y \"{0}\" \"{1}\"".format(pty(src), pty(dst))
    return execute(cmd, suppress=suppress)


def remove(src, suppress=True):
    """Removes files or directories"""
    if not exists(src):
        return 1
    if isfile(src):
        return __remove_file(src, suppress)
    else:
        return __remove_dir(src, suppress)


def __remove_file(src, suppress):
    """Removes file"""
    cmd = "del \"{0}\"".format(pty(src))
    return execute(cmd, suppress=suppress)


def __remove_dir(src, suppress):
    """Removes directory"""
    if src[-1] in ("/", "\\"):
        src = src[:-1]
    cmd = "rd \"{0}\" /s/q".format(pty(src))
    return execute(cmd, suppress=suppress)


def remove_empty_dirs(path):
    """Removes empty folders recursively"""
    if not isdir(path):
        return
    folders = os.listdir(path)
    if folders:
        for folder in folders:
            full_path = os.path.join(path, folder)
            if isdir(full_path):
                remove_empty_dirs(full_path)
    if isempty(path):
        remove(path)


def filter(files, regex, ext=True):
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
        if re.match(r"{0}".format(regex), filename(file, ext=ext)):
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


def cd_back(path):
    """Goes one folder back"""
    parts = pty(path).split("\\")
    result = parts[0]
    for i in range(1, len(parts) - 1):
        result += "/{0}".format(parts[i])
    return result


def symlink(src, dst, suppress=True):
    """Creates symbolic link"""
    parent = cd_back(dst)
    if not exists(parent):
        mkdirs(parent)
    cmd = "mklink /d \"{0}\" \"{1}\"".format(pty(dst), pty(src))
    return execute(cmd, suppress=suppress)


def lzma(dst, *src, suppress=True):
    """Creates a lzma archive"""
    cmd = "7z a -t7z -m0=lzma2 -mx=9 -aoa -mfb=64 -md=32m -ms=on -mhe \"{0}\"{1}"
    files = ""
    for path in src:
        files += " \"{0}\"".format(pty(path))
    return execute(cmd.format(pty(dst), files), suppress=suppress)
