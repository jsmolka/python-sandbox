import ctypes
import datetime
import getpass
import glob
import os
import pathlib
import re
import sys


# pth  : path
# pths : paths
# fl   : file
# fls  : files
# src  : source
# dst  : destination


class FileError(Exception):
    def __init__(self, fl):
        super(FileError, self).__init__("{0} not found".format(fl))


def pty(pth):
    """Creates valid cmd path"""
    return pth.replace("/", "\\")


def depty(pth):
    """Creates non valid cmd path"""
    return pth.replace("\\", "/")


def __endsslash(pth):
    """Checks if path ends with slash"""
    return pth[-1] in ("/", "\\")


def deslash(pth):
    """Removes trailing slash"""
    return depty(pth[:-1] if __endsslash(pth) else pth)


def enslash(pth):
    """Adds trailing slash"""
    return depty(pth if __endsslash(pth) else pth + "/")


def user():
    """Returns current user"""
    return getpass.getuser()


def mainfile():
    """Returns main file"""
    return depty(sys.modules["__main__"].__file__)


def remove_extension(fl):
    """Removes file extension"""
    return os.path.splitext(fl)[0]


def filename(fl, ext=True):
    """
    Returns file name

    Keyword arguments:
    ext -- return filename with or without extension
    """
    fl = os.path.basename(fl)
    return fl if ext else remove_extension(fl)


def dirname(fl):
    """Returns directory name of a file"""
    return enslash(os.path.dirname(fl))


def pydir():
    """Returns script directory"""
    return dirname(mainfile())


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


def check(src):
    """Checks if src exists and raises error"""
    if not exists(src):
        raise FileError(src)


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


def join(*pths):
    """Combines multiple paths"""
    pth = os.path.join("", *pths)
    return depty(pth) if filelike(pth) else enslash(pth)


def split(fl):
    """Splits file path"""
    return dirname(fl), filename(fl)


def abspath(fl):
    """Returns absolute path for a file"""
    return depty(os.path.abspath(fl))


def listdir(pth, absolute=False):
    """
    Returns list of files and directories

    Keyword arguments:
    absolute -- return absolute instead of dir names
    """
    pths = os.listdir(pth)
    if absolute:
        return [join(pth, p) for p in pths]
    return pths


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
    return today if not pattern else today.strftime(pattern)


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


def size(src, unit="kb", digits=2):
    """
    Returns file size of path

    Keyword arguments:
    unit   -- return size (b, kb, mb, gb)
    digits -- number of digits
    """
    check(src)
    div = 1024 ** ("b", "kb", "mb", "gb").index(unit)
    return round(os.path.getsize(src) / div, digits)


def files(pth, pattern=None, recursive=True):
    """
    Returns all files

    Keyword arguments:
    pattern   -- file pattern in list ["*.exe", "*.jpg"] or string "*.exe" form
    recursive -- search through sub directories recursively
    """
    if isinstance(pattern, list):
        fls = []
        for p in pattern:
            fls.extend(files(pth, pattern=p, recursive=recursive))
        return fls

    pth = join(pth, "**") if recursive else pth
    pattern = pattern if pattern else "*.*"
    return [depty(p) for p in glob.iglob(join(pth, pattern), recursive=recursive)]


def fsort(fls, key=lambda x: x, reverse=False, name=False):
    """
    Sorts a file list based on file names

    Keyword arguments:
    key     -- key for sorted
    reverse -- reverse for sorted
    name    -- use file name for sorting
    """
    return sorted(fls, key=lambda x: key(filename(x)) if name else key(x), reverse=reverse)


def isadmin():
    """Checks for admin privileges"""
    return bool(ctypes.windll.shell32.IsUserAnAdmin())


def admin():
    """Restarts as admin"""
    if not isadmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, mainfile(), None, 1)
        sys.exit()


def __execute(cmd, stdout, stderr):
    """Executes command"""
    stdout = "" if stdout else " >nul"
    stderr = "" if stderr else " 2>nul"
    return os.system(cmd + stdout + stderr)


def system(cmd, stdout=True, stderr=True):
    """
    Executes command

    Keyword arguments:
    stdout -- show standard output
    stderr -- show standard error
    """
    return __execute(cmd, stdout, stderr)


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
    check(src)
    if isfile(src) and filelike(dst):
        return __copy_file_to_file(src, dst, stdout, stderr)
    if isfile(src) and pathlike(dst):
        return __copy_file_to_dir(src, dst, stdout, stderr)
    if isdir(src) and pathlike(dst):
        return __copy_dir_to_dir(src, dst, stdout, stderr)


def __copy_file_to_file(src, dst, stdout, stderr):
    """Copies file to file"""
    cmd = "echo D | xcopy \"{0}\" \"{1}\" /y".format(pty(src), pty(dst))
    return __execute(cmd, stdout, stderr)


def __copy_file_to_dir(src, dst, stdout, stderr):
    """Copies file to directory"""
    dst = enslash(dst)
    cmd = "echo V | xcopy \"{0}\" \"{1}\" /y".format(pty(src), pty(dst))
    return __execute(cmd, stdout, stderr)


def __copy_dir_to_dir(src, dst, stdout, stderr):
    """Copies directory to directory"""
    src = deslash(src)
    dst = deslash(dst)
    cmd = "xcopy \"{0}\" \"{1}\" /y/i/s/h/e/k/f/c".format(pty(src), pty(dst))
    return __execute(cmd, stdout, stderr)


def move(src, dst, stdout=False, stderr=True):
    """
    Moves files or directories
    /y  overwrite files

    Keyword arguments:
    stdout -- show standard output
    stderr -- show standard error
    """
    check(src)
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
    dst = enslash(dst)
    cmd = "move /y \"{0}\" \"{1}\"".format(pty(src), pty(dst))
    return __execute(cmd, stdout, stderr)


def __move_dir_to_dir(src, dst, stdout, stderr):
    """Moves directory to directory"""
    src = deslash(src)
    dst = deslash(dst)
    cmd = "move /y \"{0}\" \"{1}\"".format(pty(src), pty(dst))
    return __execute(cmd, stdout, stderr)


def remove(src, stdout=False, stderr=True):
    """
    Removes files or directories

    Keyword arguments:
    stdout -- show standard output
    stderr -- show standard error
    """
    check(src)
    if isfile(src):
        return __remove_file(src, stdout, stderr)
    if isdir(src):
        return __remove_dir(src, stdout, stderr)


def __remove_file(src, stdout, stderr):
    """Removes file"""
    cmd = "del \"{0}\"".format(pty(src))
    return __execute(cmd, stdout, stderr)


def __remove_dir(src, stdout, stderr):
    """Removes directory"""
    src = deslash(src)
    cmd = "rd \"{0}\" /s/q".format(pty(src))
    return __execute(cmd, stdout, stderr)


def rename(src, dst, stdout=False, stderr=True):
    """
    Renames files or directories

    Keyword arguments:
    stdout -- show standard output
    stderr -- show standard error
    """
    check(src)
    cmd = "ren \"{0}\" \"{1}\"".format(pty(src), pty(filename(dst)))
    return __execute(cmd, stdout, stderr)


def remove_empty_dirs(pth):
    """Removes empty folders recursively"""
    if not isdir(pth):
        return
    for d in listdir(pth, absolute=True):
        if isdir(d):
            remove_empty_dirs(d)
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


def regex(fls, pattern, name=True, ext=True, other=False):
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
    for fl in fls:
        if re.match(r"".join(pattern), filename(fl, ext=ext) if name else fl):
            matching.append(fl)
        elif other:
            not_matching.append(fl)
    return matching if not other else matching, not_matching


def symlink(src, dst, stdout=False, stderr=True):
    """
    Creates symbolic link

    Keyword arguments:
    stdout -- show standard output
    stderr -- show standard error
    """
    check(src)
    if not exists(up(dst)):
        mkdirs(up(dst))
    cmd = "mklink /d \"{0}\" \"{1}\"".format(pty(dst), pty(src))
    return __execute(cmd, stdout, stderr)


def lzma(dst, *src, stdout=False, stderr=True):
    """
    Creates a lzma archive with 7zip

    Keyword arguments:
    stdout -- show standard output
    stderr -- show standard error
    """
    src = list(src)
    for idx, fl in enumerate(src):
        check(fl)
        src[idx] = pty(fl)
    cmd = "7z a -t7z -m0=lzma2 -mx=9 -aoa -mfb=64 -md=32m -ms=on -mhe \"{0}\" \"{1}\"".format(pty(dst), "\" \"".join(src))
    return __execute(cmd, stdout, stderr)


def compress_pdf(src, setting="ebook", stdout=False, stderr=True):
    """
    Compresses a pdf file

    Keyword arguments:
    setting -- choose which setting to use (screen, ebook, printer, prepress, default)
    stdout  -- show standard output
    stderr  -- show standard error
    """
    check(src)
    src_ = src + "_"
    rename(src, src_)
    cmd = "gswin32c -sDEVICE=pdfwrite -dCompatibilityLevel=1.5 -dPDFSETTINGS=/{0} -dNOPAUSE " \
          "-dQUIET -dBATCH -sOutputFile=\"{1}\" \"{2}\"".format(setting, pty(src), pty(src_))
    exit_code = __execute(cmd, stdout, stderr)
    remove(src_)
    return exit_code


def grep(key, src, pattern=None, recursive=True):
    """
    Searches for a key in a path or file

    Keyword arguments:
    pattern   -- file pattern in list ["*.exe", "*.jpg"] or string "*.exe" form
    recursive -- search through sub directories recursively
    """
    key = key.lower()
    fls = [src] if filelike(src) else files(src, pattern=pattern, recursive=recursive)
    result = []
    for fl in fls:
        try:
            with open(fl, "r", encoding="utf-8") as opened_fl:
                for idx, line in enumerate(opened_fl, start=1):
                    if key in line.lower():
                        result.append((idx, fl))
        except:
            continue
    return result


USER = join("C:/Users", user())
DESKTOP = join(USER, "Desktop")
ONEDRIVE = join(USER, "OneDrive")
PYDIR = pydir()
