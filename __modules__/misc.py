import shared


def install(package, stdout=True, stderr=True):
    """
    Installs a package.

    :param package: name of package
    :param stdout: show stdout
    :param stderr: show stderr
    :returns: int
    """
    return shared.execute("pip install {}".format(package), stdout, stderr)


def uninstall(package, stdout=True, stderr=True):
    """
    Uninstalls a package.

    :param package: name of package
    :param stdout: show stdout
    :param stderr: show stderr
    :returns: int
    """
    return shared.execute("pip uninstall -y {}".format(package), stdout, stderr)
