import os
import shared


def add(env, pth, stdout=True, stderr=True):
    """
    Adds path to system environment.

    :param env: environment to add to
    :param pth: path to add
    :param stdout: show stdout
    :param stderr: show stderr
    :returns: int
    """
    if env in os.environ:
        if pth not in os.environ[env].split(";"):
            return shared.execute("setx {0} \"%{0}%;{1}\"".format(env, pth), stdout, stderr)
    else:
        return shared.execute("setx {} \"{}\"".format(env, pth), stdout, stderr)
