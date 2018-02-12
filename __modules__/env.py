import os


def system(cmd, stdout, stderr):
    """Executes command"""
    stdout = "" if stdout else " >nul"
    stderr = "" if stderr else " 2>nul"
    return os.system(cmd + stdout + stderr)


def add_to_env(env, pth, stdout=False, stderr=True):
    """Adds path to system environment"""
    if env in os.environ:
        if pth not in os.environ[env].split(";"):
            system("setx {0} \"%{0}%;{1}\"".format(env, pth), stdout, stderr)
    else:
        system("setx {0} \"{1}\"".format(env, pth), stdout, stderr)
