import os
import shared


_changes = {}


def current(env):
    """
    Read the current value of an environment variable.

    :param env: environment variable
    :return: str
    """
    pths = ""
    if env in os.environ:
        pths = os.environ[env].rstrip(";")
    if env in _changes:
        if pths:
            pths += ";"
        pths += ";".join(_changes[env])
    return pths


def _push_change(env, pth):
    """
    Pushes an change.

    :param env: environment variable
    :param pth: path to add
    :return: None
    """
    if env not in _changes:
        _changes[env] = []
    if not pth:
        raise Exception("Path to add is invalid: <{}>".format(pth))
    if pth not in _changes[env]:
        _changes[env].append(pth)


def add(env, pth, stdout=True, stderr=True):
    """
    Adds path to system environment.

    :param env: environment to add to
    :param pth: path to add
    :param stdout: show stdout
    :param stderr: show stderr
    :returns: int
    """
    cmd = "powershell [Environment]::SetEnvironmentVariable('{}', '{}', 'User')"
    _push_change(env, pth)
    return shared.execute(cmd.format(env, current(env)), stdout, stderr)
