import os

_changes = {}
_PUSH = 0
_PULL = 1


class Change:
    """
    Change class.
    """
    def __init__(self, pth, action):
        """
        Constructor.

        :param pth: path to process
        :param action: action to apply
        :return: Change
        """
        self.pth = pth
        self.action = action

    def __eq__(self, other):
        """
        Equals.

        :param other: other instance
        :return: bool
        """
        return self.pth == other.pth and self.action == other.action

    def opposite(self, other):
        """
        Checks if other one is the opposite action.

        :param other: other instance
        :return: bool
        """
        return self.pth == other.pth and self.action != other.action


def _insert(env, change):
    """
    Inserts a change into the changes dict.

    :param env: environment to insert into
    :param change: change to push
    :return: None
    """
    if not change.pth or not isinstance(change.pth, str):
        raise Exception("Invalid path <{}>".format(change.pth))
    if env not in _changes:
        _changes[env] = []

    change.pth = change.pth.replace("/", "\\").rstrip("\\")

    if change in _changes[env]:
        return
    for idx, chg in enumerate(_changes[env]):
        if change.opposite(chg):
            del _changes[env][idx]
            return
    _changes[env].append(change)


def push(env, pth):
    """
    Pushes an change.

    :param env: environment variable
    :param pth: path to add
    :return: None
    """
    _insert(env, Change(pth, _PUSH))


def pull(env, pth):
    """
    Pulls an change.

    :param env: environment variable
    :param pth: path to remove
    :return: None
    """
    _insert(env, Change(pth, _PULL))


def _unique_gen(lst, key=None):
    """
    Removes duplicates from a list.

    :param lst: list to process
    :param key: key to apply
    :return: generator
    """
    seen = set()
    if key is None:
        for x in lst:
            if x not in seen:
                seen.add(x)
                yield x
    else:
        for x in lst:
            value = key(x)
            if value not in seen:
                seen.add(value)
                yield x


def _unique(lst, key=None):
    """
    Removes duplicates from a list.

    :param lst: list to process
    :param key: key to apply
    :return: list
    """
    return list(_unique_gen(lst, key=key))


def _path_key(pth):
    """
    Key for unique method.

    :param pth: pth to process
    :return: str
    """
    return pth.lower().replace("/", "\\").rstrip("\\")


def current(env):
    """
    Read the current value of an environment variable.

    :param env: environment variable
    :return: str
    """
    if env in os.environ:
        pths = _unique(os.environ[env].rstrip(";").split(";"), key=_path_key)
    else:
        pths = []
    if env in _changes:
        for change in _changes[env]:
            if change.action == _PUSH:
                if change.pth not in pths:
                    pths.append(change.pth)
            else:
                if change.pth in pths:
                    pths.remove(change.pth)
    return ";".join(pths)


def call(cmd, stdout=True, stderr=True):
    """
    Executes command.

    :param cmd: command to execute
    :param stdout: show stdout
    :param stderr: show stderr
    :return: int
    """
    stdout = "" if stdout else " >nul"
    stderr = "" if stderr else " 2>nul"
    return os.system(cmd + stdout + stderr)


def set_to(env, pths, stdout=True, stderr=True):
    """
    Set env to paths.

    :param env: environment variable
    :param pths: paths to set
    :param stdout: show stdout
    :param stderr: show stderr
    :return: int
    """
    cmd = "powershell [Environment]::SetEnvironmentVariable('{}', '{}', 'User')"
    return call(cmd.format(env, pths), stdout, stderr)


def apply(env, stdout=True, stderr=True):
    """
    Applies an environment variable.

    :param env: environment to apply to
    :param stdout: show stdout
    :param stderr: show stderr
    :return: int
    """
    if env not in _changes:
        return
    return set_to(env, current(env), stdout, stderr)


def apply_all(stdout=True, stderr=True):
    """
    Applies all changes.

    :param stdout: show stdout
    :param stderr: show stderr
    :return: None
    """
    if not _changes:
        return
    for env in _changes.keys():
        apply(env, stdout, stderr)


def add(env, pth, stdout=True, stderr=True):
    """
    Adds path to environment variable.

    :param env: environment to add to
    :param pth: path to add
    :param stdout: show stdout
    :param stderr: show stderr
    :returns: int
    """
    push(env, pth)
    return apply(env, stdout, stderr)


def remove(env, pth, stdout=True, stderr=True):
    """
    Removes path from environment variable.

    :param env: environment to remove from
    :param pth: path to remove
    :param stdout: show stdout
    :param stderr: show stderr
    :returns: int
    """
    pull(env, pth)
    return apply(env, stdout, stderr)
