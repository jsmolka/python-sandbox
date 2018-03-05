import os


def call(cmd, stdout=True, stderr=True):
    """
    Executes command.

    :param cmd: command to execute
    :param stdout: show stdout
    :param stderr: show stderr
    :returns: int
    """
    stdout = "" if stdout else " >nul"
    stderr = "" if stderr else " 2>nul"
    return os.system(cmd + stdout + stderr)


def install(package, stdout=True, stderr=True):
    """
    Installs a package.

    :param package: name of package
    :param stdout: show stdout
    :param stderr: show stderr
    :returns: int
    """
    return call("pip install {}".format(package), stdout, stderr)


def uninstall(package, stdout=True, stderr=True):
    """
    Uninstalls a package.

    :param package: name of package
    :param stdout: show stdout
    :param stderr: show stderr
    :returns: int
    """
    return call("pip uninstall -y {}".format(package), stdout, stderr)
