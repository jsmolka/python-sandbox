import winreg

PATH = "Software\Microsoft\Command Processor"


def get_key(path, name):
    try:
        root_key=winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(root_key, name)
        winreg.CloseKey(root_key)
        return value
    except WindowsError:
        return None


def set_reg(path, name, value):
    try:
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, path)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(registry_key)
        return True
    except WindowsError:
        return False


# print(set_reg(PATH, "test", "lol nice"))
# print(get_key(PATH, "test"))
