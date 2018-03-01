import ctypes
import datetime
import getpass
import glob
import itertools
import multiprocessing
import os
import pathlib
import re
import sys


class FileError(Exception):
    def __init__(self, fl):
        super(FileError, self).__init__("{0} not found".format(fl))


def pty(pth):
    """
    Creates a valid cmd path.

    :param pth: path to be validated
    :returns: str
    """
    return pth.replace("/", "\\")


def depty(pth):
    """
    Creates a non valid cmd path.

    :param pth: path to be devalidated
    :returns: str
    """
    return pth.replace("\\", "/")


def endsslash(pth):
    """
    Checks if path ends with a slash.

    :param pth: path to be checked
    :returns: str
    """
    return pth[-1] in ("/", "\\")


def deslash(pth):
    """
    Removes trailing slash from a path.

    :param pth: path to be deslashed
    :returns: str
    """
    return depty(pth.rstrip("/", "\\"))


def enslash(pth):
    """
    Adds trailing slash to a path.

    :param pth: path to be enslashed
    :returns: str
    """
    return depty(pth if endsslash(pth) else pth + "/")


def user():
    """
    Returns current user.

    :returns: str
    """
    return getpass.getuser()


def abspath(fl):
    """
    Returns absolute path for a file.

    :param fl: file to process
    :returns: str
    """
    return depty(os.path.abspath(fl))


def mainfile():
    """
    Returns main file if run as script or
    directory if run from console.

    :returns: str
    """
    if not hasattr(sys.modules["__main__"], "__file__"):
        return abspath(sys.argv[0])
    return depty(sys.modules["__main__"].__file__)


def remove_extension(fl):
    """
    Removes file extension.

    :param fl: file to be processed
    :returns: str
    """
    return os.path.splitext(fl)[0]


def filename(fl, ext=True):
    """
    Returns file name.

    :param fl: file to be processed
    :param ext: keep extension
    :returns: str
    """
    fl = os.path.basename(fl)
    return fl if ext else remove_extension(fl)


def dirname(fl):
    """
    Returns directory name of a file.

    :param fl: file to be processed
    :return: str
    """
    return enslash(os.path.dirname(fl))


def filelike(src):
    """
    Checks if src is filelike.

    :param src: src to be checked
    :returns: boolean
    """
    return bool(os.path.splitext(src)[1])


def pathlike(src):
    """
    Checks if src is pathlike.

    :param src: src to be checked
    :returns: boolean
    """
    return not filelike(src)


def pydir():
    """
    Returns script directory.

    :returns: str
    """
    main = mainfile()
    if pathlike(main):
        return main
    return dirname(main)


def cwd():
    """
    Returns current working directory.

    :returns: str
    """
    return enslash(os.getcwd())


def chdir(pth):
    """
    Changes current working directory.

    :param pth: directory to change to
    :returns: boolean
    """
    return os.chdir(pth)


def isdir(src):
    """
    Checks if src is a directory.

    :param src: src to be checked
    :returns: boolean
    """
    return os.path.isdir(src)


def isfile(src):
    """
    Checks if src is a file.

    :param src: src to be checked
    :returns: boolean
    """
    return os.path.isfile(src)


def exists(src):
    """
    Checks if src exists.

    :param src: src to be checked
    :returns: boolean
    """
    return os.path.exists(src)


def check(src):
    """
    Checks if src exists and raises error.

    :param src: src to be checked
    :returns: None
    """
    if not exists(src):
        raise FileError(src)


def extension(fl, dot=False):
    """
    Returns file extension.

    :param fl: file to be processed
    :param dot: keep dot
    :returns: str
    """
    ext = os.path.splitext(fl)[1]
    return ext if dot else ext[1:]


def join(*pths):
    """
    Combines multiple paths.

    :param pths: paths to be combined
    :returns: str
    """
    pth = os.path.join("", *pths)
    return depty(pth) if filelike(pth) else enslash(pth)


def split(fl):
    """
    Splits a file into path and name.

    :param fl: file to be processed
    :returns: tuple
    """
    return dirname(fl), filename(fl)


def listdir(pth, absolute=False):
    """
    Returns list of files and directories.

    :param pth: path to be processed
    :param absolute: get absolute path
    :returns: list
    """
    pths = os.listdir(pth)
    if absolute:
        return [join(pth, p) for p in pths]
    return pths


def isempty(pth):
    """
    Checks if directory is empty.

    :param pth: path to be checked
    :returns: boolean
    """
    return not bool(listdir(pth))


def date(pattern="%d-%m-%y"):
    """
    Returns current date.

    :param pattern: pattern to be used
    :returns: str
    """
    today = datetime.date.today()
    return today if not pattern else today.strftime(pattern)


def mkdirs(pth):
    """
    Creates directories recursively.

    :param pth: path to create
    :returns: boolean
    """
    if filelike(pth):
        pth = dirname(pth)
    return os.makedirs(pth)


def up(pth):
    """
    Goes one folder up.

    :param pth: directory to go up from
    :returns: str
    """
    if filelike(pth):
        pth = dirname(pth)
    return enslash(str(pathlib.Path(pth).parent))


def size(src, unit="kb", digits=2):
    """
    Returns file size of path.

    :param src: src to measure
    :param unit: unit to convert to (b, kb, mb, gb)
    :param digits: digits to round to
    :returns: int
    """
    check(src)
    div = 1024 ** ("b", "kb", "mb", "gb").index(unit)
    return round(os.path.getsize(src) / div, digits)


def files(pth, pattern=None, recursive=True):
    """
    Returns all files.

    :param pth: path to get files for
    :param pattern: file pattern in string or list form
    :param recursive: search through sub directories
    :returns: list
    """
    if isinstance(pattern, list):
        fls = []
        for p in pattern:
            fls.extend(files(pth, pattern=p, recursive=recursive))
        return fls

    pth = join(pth, "**") if recursive else pth
    pattern = pattern if pattern else "*.*"
    return [depty(p) for p in glob.iglob(join(pth, pattern), recursive=recursive)]


def isadmin():
    """
    Checks for admin privileges

    :returns: boolean
    """
    return bool(ctypes.windll.shell32.IsUserAnAdmin())


def admin(fl=None):
    """
    Restarts file as admin.

    :param fl: file to run as admin
    :returns: None
    """
    if not isadmin():
        fl = fl if fl else mainfile()
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, fl, None, 1)
        sys.exit()


def _execute(cmd, stdout, stderr):
    """
    Executes a command.

    :param cmd: command to be executed
    :param stdout: show stdout
    :param stderr: show stderr
    :returns: int
    """
    stdout = "" if stdout else " >nul"
    stderr = "" if stderr else " 2>nul"
    return os.system(cmd + stdout + stderr)


def system(cmd, stdout=True, stderr=True):
    """
    Executes a command.

    :param cmd: command to be executed
    :param stdout: show stdout
    :param stderr: show stderr
    :returns: int
    """
    return _execute(cmd, stdout, stderr)


def _copy_file_to_file(src, dst, stdout, stderr):
    """
    Copies file to file.

    :param src: file to copy
    :param dst: file copy to
    :param stdout: show stdout
    :param stderr: show stderr
    :returns: int
    """
    cmd = "echo D | xcopy \"{0}\" \"{1}\" /y".format(pty(src), pty(dst))
    return _execute(cmd, stdout, stderr)


def _copy_file_to_dir(src, dst, stdout, stderr):
    """
    Copies file to directory.

    :param src: file to copy
    :param dst: directory to copy to
    :param stdout: show stdout
    :param stderr: show stderr
    :returns: int
    """
    dst = enslash(dst)
    cmd = "echo V | xcopy \"{0}\" \"{1}\" /y".format(pty(src), pty(dst))
    return _execute(cmd, stdout, stderr)


def _copy_dir_to_dir(src, dst, stdout, stderr):
    """
    Copies directory to directory.

    :param src: directory to copy
    :param dst: directory to copy to
    :param stdout: show stdout
    :param stderr: show stderr
    :returns: int
    """
    src = deslash(src)
    dst = deslash(dst)
    cmd = "xcopy \"{0}\" \"{1}\" /y/i/s/h/e/k/f/c".format(pty(src), pty(dst))
    return _execute(cmd, stdout, stderr)


def copy(src, dst, stdout=False, stderr=True):
    """
    Copies files or directories.
    /i  assume dst is a directory
    /s  copy folders and sub folders
    /h  copy hidden files and folders
    /e  copy empty folders
    /k  copy attributes
    /f  display full src and dst names
    /c  continue copying if an error occurs
    /y  overwrite files

    :param src: file or directory to copy
    :param dst: file or directory to copy to
    :param stdout: show stdout
    :param stderr: show stderr
    :returns: int
    """
    check(src)
    if isfile(src) and filelike(dst):
        return _copy_file_to_file(src, dst, stdout, stderr)
    if isfile(src) and pathlike(dst):
        return _copy_file_to_dir(src, dst, stdout, stderr)
    if isdir(src) and pathlike(dst):
        return _copy_dir_to_dir(src, dst, stdout, stderr)


def _move_file_to_file(src, dst, stdout, stderr):
    """
    Moves file to file.

    :param src: file to move
    :param dst: file to move to
    :param stdout: show stdout
    :param stderr: show stderr
    :returns: int
    """
    cmd = "move /y \"{0}\" \"{1}\"".format(pty(src), pty(dst))
    return _execute(cmd, stdout, stderr)


def _move_file_to_dir(src, dst, stdout, stderr):
    """
    Move file to directory.

    :param src: file to move
    :param dst: directory to move to
    :param stdout: show stdout
    :param stderr: show stderr
    :returns: int
    """
    dst = enslash(dst)
    cmd = "move /y \"{0}\" \"{1}\"".format(pty(src), pty(dst))
    return _execute(cmd, stdout, stderr)


def _move_dir_to_dir(src, dst, stdout, stderr):
    """
    Move directory to directory.

    :param src: directory to move
    :param dst: directory to move to
    :param stdout: show stdout
    :param stderr: show stderr
    :returns: int
    """
    src = deslash(src)
    dst = deslash(dst)
    cmd = "move /y \"{0}\" \"{1}\"".format(pty(src), pty(dst))
    return _execute(cmd, stdout, stderr)


def move(src, dst, stdout=False, stderr=True):
    """
    Moves files or directories.
    /y  overwrite files

    :param src: file or directory to move
    :param dst: file or directory to move to
    :param stdout: show stdout
    :param stderr: show stderr
    :returns: int
    """
    check(src)
    if not exists(dst):
        mkdirs(dst)
    if isfile(src) and filelike(dst):
        return _move_file_to_file(src, dst, stdout, stderr)
    if isfile(src) and pathlike(dst):
        return _move_file_to_dir(src, dst, stdout, stderr)
    if isdir(src) and pathlike(dst):
        return _move_dir_to_dir(src, dst, stdout, stderr)


def _remove_file(src, stdout, stderr):
    """
    Removes file.

    :param src: file to delete
    :param stdout: show stdout
    :param stderr: show stderr
    :returns: int
    """
    cmd = "del \"{0}\"".format(pty(src))
    return _execute(cmd, stdout, stderr)


def _remove_dir(src, stdout, stderr):
    """
    Removes directory.

    :param src: directory to delete
    :param stdout: show stdout
    :param stderr: show stderr
    :returns: int
    """
    src = deslash(src)
    cmd = "rd \"{0}\" /s/q".format(pty(src))
    return _execute(cmd, stdout, stderr)


def remove(src, stdout=False, stderr=True):
    """
    Removes file or directory.

    :param src: file or directory to delete
    :param stdout: show stdout
    :param stderr: show stderr
    :returns: int
    """
    check(src)
    if isfile(src):
        return _remove_file(src, stdout, stderr)
    if isdir(src):
        return _remove_dir(src, stdout, stderr)


def rename(src, dst, stdout=False, stderr=True):
    """
    Renames files or directories.

    :param src: file or directory to rename
    :param dst: name to rename to
    :param stdout: show stdout
    :param stderr: show stderr
    :returns: int
    """
    check(src)
    cmd = "ren \"{0}\" \"{1}\"".format(pty(src), pty(filename(dst)))
    return _execute(cmd, stdout, stderr)


def remove_empty_dirs(pth):
    """
    Removes empty folders recursively.

    :param pth: path to remove folders from
    :returns: None
    """
    if not isdir(pth):
        return
    for d in listdir(pth, absolute=True):
        if isdir(d):
            remove_empty_dirs(d)
    if isempty(pth):
        remove(pth)


def _unique(fls, key):
    """
    Removes duplicates based on a key.

    :param fls: list to remove duplicates from
    :param key: remove duplicates based on key
    :returns: list without duplicates
    """
    seen = set()
    for pth in fls:
        val = key(pth)
        if val in seen:
            continue
        seen.add(val)
        yield pth


def unique(fls, key=lambda x: x):
    """
    Removes duplicates based on a key.

    :param fls: list to remove duplicates from
    :param key: remove duplicates based on key
    :returns: list without duplicates
    """
    return list(_unique(fls, key))


def regex(fls, pattern, name=True, ext=True, other=False):
    """
    Filters files with regular expressions.
    .       match any character
    *       match any repetition of characters (.* any sequence)
    \       escape following character
    ^       start of string
    $       end of string
    ()      enclose expression
    [A-Z]   sequence of characters
    {m, n}  characters must appear m to n times
    (?:1|2) must be one of the options

    :param fls: list to process
    :param pattern: regex pattern to apply
    :param name: use filename for regex
    :param ext: keep extension
    :param other: return not matching list aswell
    :returns: tuple
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
    Creates a symbolic link.

    :param src: src to link to
    :param dst: path for link
    :param stdout: show stdout
    :param stderr: show stderr
    :returns: int
    """
    check(src)
    if not exists(up(dst)):
        mkdirs(up(dst))
    cmd = "mklink /d \"{0}\" \"{1}\"".format(pty(dst), pty(src))
    return _execute(cmd, stdout, stderr)


def lzma(dst, *src, stdout=False, stderr=True):
    """
    Creates a lzma archive with 7zip.

    :param dst: path for created archive
    :param src: files to compress
    :param stdout: show stdout
    :param stderr: show stderr
    :returns: int
    """
    src = list(src)
    for idx, fl in enumerate(src):
        check(fl)
        src[idx] = pty(fl)
    cmd = "7z a -t7z -m0=lzma2 -mx=9 -aoa -mfb=64 -md=32m -ms=on -mhe \"{0}\" \"{1}\"".format(pty(dst), "\" \"".join(src))
    return _execute(cmd, stdout, stderr)


def compress_pdf(src, setting="ebook", stdout=False, stderr=True):
    """
    Compresses a pdf file.

    :param src: pdf file to compress
    :param setting: setting to apply (screen, ebook, printer, prepress, default)
    :param stdout: show stdout
    :param stderr: show stderr
    :returns: int
    """
    check(src)
    src_ = src + "_"
    rename(src, src_)
    cmd = "gswin32c -sDEVICE=pdfwrite -dCompatibilityLevel=1.5 -dPDFSETTINGS=/{0} -dNOPAUSE " \
          "-dQUIET -dBATCH -sOutputFile=\"{1}\" \"{2}\"".format(setting, pty(src), pty(src_))
    exit_code = _execute(cmd, stdout, stderr)
    remove(src_)
    return exit_code


def _grep_file(key, fl, case):
    """
    Searches for a key in a file.

    :param key: key to search for
    :param fl: file to search through
    :param case: search case sensitive
    :returns: list
    """
    result = []
    try:
        with open(fl, "r", encoding="utf-8") as opened_fl:
            for idx, line in enumerate(opened_fl, start=1):
                line = line if case else line.lower()
                if key in line:
                    result.append((idx, fl))
    except Exception:
        pass
    return result


def _grep_files(key, fls, case):
    """
    Searches for a key in multiple files.

    :param key: key to search for
    :param fls: files to search through
    :param case: search case sensitive
    :returns: list
    """
    result = []
    for fl in fls:
        result.extend(_grep_file(key, fl, case))
    return result


def _grep_process(key, fls, case, count):
    """
    Searches for a key in multiple files with multiple processes.

    :param key: key to search for
    :param fls: files to search through
    :param case: search case sensitive
    :param count: process count
    :returns: list
    """
    pool = multiprocessing.Pool(processes=count)
    starmap = pool.starmap(_grep_file, zip(itertools.repeat(key), fls, itertools.repeat(case)))
    pool.close()
    pool.join()
    return list(itertools.chain.from_iterable(starmap))


def grep(key, src, pattern=None, recursive=True, case=False, count=1):
    """
    Searches for a key in a path or file.

    :param key: key to search for
    :param src: file or directory to search through
    :param pattern: pattern for files
    :param recursive: search through sub directories
    :param case: search case sensitive
    :param count: process count (if __name__ == "__main__" necessary if greater than one)
    :returns: list
    """
    key = key if case else key.lower()
    fls = [src] if filelike(src) else files(src, pattern=pattern, recursive=recursive)

    if count == 1:
        return _grep_files(key, fls, case)
    else:
        return _grep_process(key, fls, case, count)


USER = join("C:/Users", user())
DESKTOP = join(USER, "Desktop")
ONEDRIVE = join(USER, "OneDrive")
PYDIR = pydir()
