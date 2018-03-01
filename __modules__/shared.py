import os


def execute(cmd, stdout, stderr):
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


def system(cmd, stdout=True, stderr=True):
    """
    Executes command.

    :param cmd: command to execute
    :param stdout: show stdout
    :param stderr: show stderr
    :returns: int
    """
    return execute(cmd, stdout, stderr)
