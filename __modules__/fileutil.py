import ctypes
import datetime
import getpass
import glob
import os
import pathlib
import re
import sys


class FileException(Exception):
    def __init__(self, file):
        super(FileException, self).__init__("{0} not found".format(file))


class CmdException(Exception):
    def __init__(self, command):
        super(CmdException, self).__init__("{0} is unavailable".format(command))


class ArgException(Exception):
    def __init__(self, arg):
        super(ArgException, self).__init__("Invalid argument {0}".format(arg))


class ExtException(Exception):
    def __init__(self, ext):
        super(ExtException, self).__init__("Invalid extension {0}".format(ext))


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


def mainfile():
    """Returns main file"""
    return sys.modules["__main__"].__file__


def pydir():
    """Returns script directory"""
    return depty(os.path.dirname(mainfile()) + "\\")


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


def extension(file, dot=False):
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
    directory = os.path.dirname(file)
    if not directory:
        return ""
    return depty(directory + "\\")


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


def back(path):
    """Goes one folder back"""
    return depty(str(pathlib.Path(path).parent) + "\\")


def size(path, unit="kb"):
    """
    Returns file size of path
    Possible units: b, kb, mb, gb
    """
    if not exists(path):
        raise FileException(path)
    if unit not in ("b", "kb", "mb", "gb"):
        raise ArgException(unit)
    div = 1
    if unit == "kb":
        div = 1024
    elif unit == "mb":
        div = pow(1024, 2)
    elif unit == "gb":
        div = pow(1024, 3)
    return os.path.getsize(path) / div


def files(path, pattern=None, recursive=True):
    """Returns all files"""
    if pattern:
        fls = []
        for rule in pattern:
            fls.extend(list(glob.iglob("{0}/**/{1}".format(path, rule), recursive=recursive)))
        return fls
    return list(glob.iglob("{0}/**/*.*".format(path), recursive=recursive))


def fsort(fls, key=lambda x: x, reverse=False, name=False):
    """Sorts a file list based on file names"""
    return sorted(fls, key=lambda x: key(filename(x)) if name else key, reverse=reverse)


def admin(file_name):
    """Restart file as admin"""
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, file_name, None, 1)
        sys.exit()


def __execute(command, stdout, stderr):
    """Executes command"""
    if not stdout:
        command += " >nul"
    if not stderr:
        command += " 2>nul"
    return os.system(command)


def cmd(command, stdout=True, stderr=True):
    """Executes command"""
    return __execute(command, stdout=stdout, stderr=stderr)


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
        raise FileException(src)
    if isfile(src) and filelike(dst):
        return __copy_file_to_file(src, dst, stdout, stderr)
    if isfile(src) and pathlike(dst):
        return __copy_file_to_dir(src, dst, stdout, stderr)
    if isdir(src) and pathlike(dst):
        return __copy_dir_to_dir(src, dst, stdout, stderr)


def __copy_file_to_file(src, dst, stdout, stderr):
    """Copies file to file"""
    command = "echo D | xcopy \"{0}\" \"{1}\" /y".format(pty(src), pty(dst))
    return __execute(command, stdout, stderr)


def __copy_file_to_dir(src, dst, stdout, stderr):
    """Copies file to directory"""
    if not __endsslash(dst):
        dst += "\\"
    command = "echo V | xcopy \"{0}\" \"{1}\" /y".format(pty(src), pty(dst))
    return __execute(command, stdout, stderr)


def __copy_dir_to_dir(src, dst, stdout, stderr):
    """Copies directory to directory"""
    if __endsslash(src):
        src = src[:-1]
    if __endsslash(dst):
        dst = dst[:-1]
    command = "xcopy \"{0}\" \"{1}\" /y/i/s/h/e/k/f/c".format(pty(src), pty(dst))
    return __execute(command, stdout, stderr)


def move(src, dst, stdout=False, stderr=True):
    """
    Moves files or directories
    /y  overwrite files
    """
    if not exists(src):
        raise FileException(src)
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
    command = "move /y \"{0}\" \"{1}\"".format(pty(src), pty(dst))
    return __execute(command, stdout, stderr)


def __move_file_to_dir(src, dst, stdout, stderr):
    """Moves file to directory"""
    if not __endsslash(dst):
        dst += "\\"
    command = "move /y \"{0}\" \"{1}\"".format(pty(src), pty(dst))
    return __execute(command, stdout, stderr)


def __move_dir_to_dir(src, dst, stdout, stderr):
    """Moves directory to directory"""
    if __endsslash(src):
        src = src[:-1]
    if __endsslash(dst):
        dst = dst[:-1]
    command = "move /y \"{0}\" \"{1}\"".format(pty(src), pty(dst))
    return __execute(command, stdout, stderr)


def remove(src, stdout=False, stderr=True):
    """Removes files or directories"""
    if not exists(src):
        raise FileException(src)
    if isfile(src):
        return __remove_file(src, stdout, stderr)
    else:
        return __remove_dir(src, stdout, stderr)


def __remove_file(src, stdout, stderr):
    """Removes file"""
    command = "del \"{0}\"".format(pty(src))
    return __execute(command, stdout, stderr)


def __remove_dir(src, stdout, stderr):
    """Removes directory"""
    if __endsslash(src):
        src = src[:-1]
    command = "rd \"{0}\" /s/q".format(pty(src))
    return __execute(command, stdout, stderr)


def rename(src, dst, stdout=False, stderr=True):
    """Renames files or directories"""
    if not exists(src):
        raise FileException(src)
    command = "ren \"{0}\" \"{1}\"".format(pty(src), pty(filename(dst)))
    return __execute(command, stdout, stderr)


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


def remove_duplicates(fls):
    """Removes duplicate files"""
    test = set([filename(file) for file in fls])
    if len(test) == len(fls):
        return fls

    result = []
    for i in range(0, len(fls)):
        duplicate = False
        for j in range(i + 1, len(fls)):
            if filename(fls[i]) == filename(fls[j]):
                duplicate = True
                break
        if not duplicate:
            result.append(fls[i])
    return result


def regex(fls, pattern, name=True, ext=True, other=True):
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
    not_matching = []
    for f in fls:
        if re.match(r"{0}".format(pattern), filename(f, ext=ext) if name is True else f):
            matching.append(f)
        else:
            not_matching.append(f)
    if other:
        return matching, not_matching
    else:
        return matching


def symlink(src, dst, stdout=False, stderr=True):
    """Creates symbolic link"""
    if not exists(src):
        raise FileException(src)
    parent = back(dst)
    if not exists(parent):
        mkdirs(parent)
    command = "mklink /d \"{0}\" \"{1}\"".format(pty(dst), pty(src))
    return __execute(command, stdout, stderr)


HAS_7Z = True if __execute("7z", False, False) == 0 else False
HAS_GS = True if __execute("echo quit | gswin32c", False, False) == 0 else False


def lzma(dst, *src, stdout=False, stderr=True):
    """Creates a lzma archive"""
    if not HAS_7Z:
        raise CmdException("7z")
    for file in src:
        if not exists(file):
            raise FileException(file)
    command = "7z a -t7z -m0=lzma2 -mx=9 -aoa -mfb=64 -md=32m -ms=on -mhe \"{0}\"{1}"
    fls = ""
    for path in src:
        fls += " \"{0}\"".format(pty(path))
    return __execute(command.format(pty(dst), fls), stdout, stderr)


def compress_pdf(src, setting="ebook", stdout=False, stderr=True):
    """
    Compresses a pdf file
    Settings: screen, ebook, printer, prepress, default
    """
    if not HAS_GS:
        raise CmdException("Ghostscript")
    if not exists(src):
        raise FileException(src)
    if not extension(src) == "pdf":
        raise ExtException("pdf")
    if setting not in ("screen", "ebook", "printer", "prepress", "default"):
        raise ArgException(setting)
    src_ = src + "_"
    rename(src, src_)
    command = "gswin32c -sDEVICE=pdfwrite -dCompatibilityLevel=1.5 -dPDFSETTINGS=/{0} " \
              "-dNOPAUSE -dQUIET -dBATCH -sOutputFile=\"{1}\" \"{2}\"".format(setting, pty(src), pty(src_))
    code = __execute(command, stdout, stderr)
    remove(src_)
    return code
