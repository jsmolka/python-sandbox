import ctypes
import datetime
import getpass
import glob
import os
import pathlib
import re
import sys


# pth : path
# fl  : file
# fls : files
# src : source
# dst : destination


class FileException(Exception):
    def __init__(self, e):
        super(FileException, self).__init__("{0} not found".format(e))


class CmdException(Exception):
    def __init__(self, e):
        super(CmdException, self).__init__("{0} is unavailable".format(e))


class ArgException(Exception):
    def __init__(self, e):
        super(ArgException, self).__init__("Invalid argument {0}".format(e))


class ExtException(Exception):
    def __init__(self, e):
        super(ExtException, self).__init__("Invalid extension {0}".format(e))


def pty(pth):
    """Creates valid cmd path"""
    return pth.replace("/", "\\")


def depty(pth):
    """Creates non valid cmd path"""
    return pth.replace("\\", "/")


def __endsslash(pth):
    """Checks if path ends with slash"""
    return True if pth[-1] in ("/", "\\") else False


def deslash(pth):
    """Removes trailing slash"""
    return depty(pth[:-1] if __endsslash(pth) else pth)


def enslash(pth):
    """Adds trailing slash"""
    return depty(pth if __endsslash(pth) else pth + "\\")


def user():
    """Returns current user"""
    return getpass.getuser()


def mainfile():
    """Returns main file"""
    return sys.modules["__main__"].__file__


def pydir():
    """Returns script directory"""
    return enslash(os.path.dirname(mainfile()))


USER = "C:/Users/{0}/".format(user())
DESKTOP = "{0}Desktop/".format(USER)
ONEDRIVE = "{0}OneDrive/".format(USER)
PYDIR = pydir()


def cwd():
    """Returns current working directory"""
    return enslash(os.getcwd())


def chdir(pth):
    """Changes current working directory"""
    return os.chdir(pth)


def isdir(src):
    """Checks if src is a directory"""
    return os.path.isdir(src)


def isfile(src):
    """Checks if src is a file"""
    return os.path.isfile(src)


def exists(src):
    """Checks if src exists"""
    return os.path.exists(src)


def filelike(src):
    """Checks if src is filelike"""
    if os.path.splitext(src)[1]:
        return True
    return False


def pathlike(src):
    """Checks if src is pathlike"""
    return not filelike(src)


def extension(fl, dot=False):
    """
    Returns file extension

    Keyword arguments:
    dot -- return extension with or without dot
    """
    ext = os.path.splitext(fl)[1]
    return ext if dot else ext[1:]


def rem_extension(fl):
    """Removes file extension"""
    return os.path.splitext(fl)[0]


def filename(fl, ext=True):
    """
    Returns file name

    Keyword arguments:
    ext -- return filename with or without extension
    """
    file = os.path.basename(fl)
    return file if ext else rem_extension(fl)


def dirname(fl):
    """Returns directory name of a file"""
    return enslash(os.path.dirname(fl))


def join(pth1, pth2):
    """Combines two paths"""
    pth = os.path.join(pth1, pth2)
    return depty(pth) if filelike(pth) else enslash(pth)


def abspath(fl):
    """Returns absolute path for a file"""
    return depty(os.path.abspath(fl))


def listdir(pth, absolute=False):
    """
    Returns list of files and directories

    Keyword arguments:
    absolute -- return absolute instead of dir names
    """
    fls = os.listdir(pth)
    if absolute:
        fls = [join(pth, d) for d in fls]
    return fls


def isempty(pth):
    """Checks if directory is empty"""
    if not listdir(pth):
        return True
    return False


def date(pattern="%d-%m-%y"):
    """
    Returns current date

    Keyword arguments:
    pattern -- format pattern of datetime
    """
    today = datetime.date.today()
    return today if pattern is None else today.strftime(pattern)


def mkdirs(pth):
    """Creates directories recursively"""
    if filelike(pth):
        pth = dirname(pth)
    return os.makedirs(pth)


def up(pth):
    """Goes one folder up"""
    if filelike(pth):
        pth = dirname(pth)
    return enslash(str(pathlib.Path(pth).parent))


def size(src, unit="kb"):
    """
    Returns file size of path

    Keyword arguments:
    unit -- return size in b, kb, mb, gb
    """
    if not exists(src):
        raise FileException(src)
    try:
        div = 1024 ** ("b", "kb", "mb", "gb").index(unit)
    except ValueError:
        raise ArgException(unit)
    return os.path.getsize(src) / div


def files(pth, pattern=None, recursive=True):
    """
    Returns all files

    Keyword arguments:
    pattern   -- file pattern in list form ["*.exe", "*.jpg"]
    recursive -- go through sub directories recursively
    """
    if pattern:
        fls = []
        for rule in pattern:
            fls.extend(list(glob.iglob("{0}/**/{1}".format(pth, rule), recursive=recursive)))
        return fls
    return list(glob.iglob("{0}/**/*.*".format(pth), recursive=recursive))


def fsort(fls, key=lambda x: x, reverse=False, name=False):
    """
    Sorts a file list based on file names

    Keyword arguments:
    key     -- key for sorted
    reverse -- reverse for sorted
    name    -- use file name for sorting
    """
    return sorted(fls, key=lambda x: key(filename(x)) if name else key, reverse=reverse)


def admin():
    """Restarts as admin"""
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, mainfile(), None, 1)
        sys.exit()


def __execute(command, stdout, stderr):
    """Executes command"""
    if not stdout:
        command += " >nul"
    if not stderr:
        command += " 2>nul"
    return os.system(command)


def cmd(command, stdout=True, stderr=True):
    """
    Executes command

    Keyword arguments:
    stdout -- show standard output
    stderr -- show standard error
    """
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

    Keyword arguments:
    stdout -- show standard output
    stderr -- show standard error
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
    dst = enslash(dst)
    command = "echo V | xcopy \"{0}\" \"{1}\" /y".format(pty(src), pty(dst))
    return __execute(command, stdout, stderr)


def __copy_dir_to_dir(src, dst, stdout, stderr):
    """Copies directory to directory"""
    src = deslash(src)
    dst = deslash(dst)
    command = "xcopy \"{0}\" \"{1}\" /y/i/s/h/e/k/f/c".format(pty(src), pty(dst))
    return __execute(command, stdout, stderr)


def move(src, dst, stdout=False, stderr=True):
    """
    Moves files or directories
    /y  overwrite files

    Keyword arguments:
    stdout -- show standard output
    stderr -- show standard error
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
    dst = enslash(dst)
    command = "move /y \"{0}\" \"{1}\"".format(pty(src), pty(dst))
    return __execute(command, stdout, stderr)


def __move_dir_to_dir(src, dst, stdout, stderr):
    """Moves directory to directory"""
    src = deslash(src)
    dst = deslash(dst)
    command = "move /y \"{0}\" \"{1}\"".format(pty(src), pty(dst))
    return __execute(command, stdout, stderr)


def remove(src, stdout=False, stderr=True):
    """
    Removes files or directories

    Keyword arguments:
    stdout -- show standard output
    stderr -- show standard error
    """
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
    src = deslash(src)
    command = "rd \"{0}\" /s/q".format(pty(src))
    return __execute(command, stdout, stderr)


def rename(src, dst, stdout=False, stderr=True):
    """
    Renames files or directories

    Keyword arguments:
    stdout -- show standard output
    stderr -- show standard error
    """
    if not exists(src):
        raise FileException(src)
    command = "ren \"{0}\" \"{1}\"".format(pty(src), pty(filename(dst)))
    return __execute(command, stdout, stderr)


def remove_empty_dirs(pth):
    """Removes empty folders recursively"""
    if not isdir(pth):
        return
    dirs = listdir(pth)
    for d in dirs:
        full = os.path.join(pth, d)
        if isdir(full):
            remove_empty_dirs(full)
    if isempty(pth):
        remove(pth)


def remove_duplicates(fls):
    """Removes duplicate files"""
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

    Keyword arguments:
    name  -- apply regular expression to filename
    ext   -- choose whether to ignore extension or not
    other -- return list of not matching files
    """
    matching = []
    not_matching = []
    for f in fls:
        if re.match(r"{0}".format(pattern), filename(f, ext=ext) if name is True else f):
            matching.append(f)
        else:
            not_matching.append(f)
    return matching, not_matching if other else matching


def symlink(src, dst, stdout=False, stderr=True):
    """
    Creates symbolic link

    Keyword arguments:
    stdout -- show standard output
    stderr -- show standard error
    """
    if not exists(src):
        raise FileException(src)
    parent = up(dst)
    if not exists(parent):
        mkdirs(parent)
    command = "mklink /d \"{0}\" \"{1}\"".format(pty(dst), pty(src))
    return __execute(command, stdout, stderr)


HAS_7Z = True if __execute("7z", False, False) == 0 else False
HAS_GS = True if __execute("echo quit | gswin32c", False, False) == 0 else False


def lzma(dst, *src, stdout=False, stderr=True):
    """
    Creates a lzma archive with 7zip

    Keyword arguments:
    stdout -- show standard output
    stderr -- show standard error
    """
    if not HAS_7Z:
        raise CmdException("7z")
    fls = ""
    for f in src:
        if not exists(f):
            raise FileException(f)
        fls += " \"{0}\"".format(pty(f))
    command = "7z a -t7z -m0=lzma2 -mx=9 -aoa -mfb=64 -md=32m -ms=on -mhe \"{0}\"{1}"
    return __execute(command.format(pty(dst), fls), stdout, stderr)


def compress_pdf(src, setting="ebook", stdout=False, stderr=True):
    """
    Compresses a pdf file
    Settings: screen, ebook, printer, prepress, default

    Keyword arguments:
    setting -- choose which setting to use ("screen", "ebook", "printer", "prepress", "default")
    stdout  -- show standard output
    stderr  -- show standard error
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
