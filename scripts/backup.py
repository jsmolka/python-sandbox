import dialog
import draw
import datetime
import os


def xcopy(source, target, is_file):
    """Copies directory or file"""
    if os.path.exists(source):
        if is_file:  # Copy files without arguments
            os.system("xcopy \"{0}\" \"{1}\"".format(source, target))
        else:  # Copy directories with arguments
            os.system("xcopy \"{0}\" \"{1}\" /s/h/e/k/f/c".format(source, target))

        return True
    else:
        return False


today = datetime.date.today()
backup_name = "Backup {0}".format(today.strftime("%d-%m-%y"))
backup_path = "D:\\Backup\\" + backup_name

backup = [
    # (
    #   source,
    #   target,
    #   is_file
    # )
    (
        "C:\\Users\\Julian\\OneDrive\\Coding",
        backup_path + "\\Coding\\",
        False
    ),
    (
        "C:\\Users\\Julian\\OneDrive\\Studium",
        backup_path + "\\Studium\\",
        False
    ),
    (
        "C:\\Users\\Julian\\OneDrive\\Sonstiges",
        backup_path + "\\Sonstiges\\",
        False
    ),
    (
        "C:\\Users\\Julian\\OneDrive\\Pictures",
        backup_path + "\\Pictures\\",
        False
    ),
    (
        "C:\\Users\\Julian\\OneDrive\\Documents",
        backup_path + "\\Documents\\",
        False
    ),
    (
        "C:\\Users\\Julian\\Documents\\Battlefield 1\\settings",
        backup_path + "\\Documents\\Config\\Battlefield 1\\",
        False
    ),
    (
        "C:\\Users\\Julian\\Documents\\Battlefield 3\\settings",
        backup_path + "\\Documents\\Config\\Battlefield 3\\",
        False
    ),
    (
        "C:\\Users\\Julian\\Documents\\Battlefield 4\\settings",
        backup_path + "\\Documents\\Config\\Battlefield 4\\",
        False
    ),
    (
        "C:\\Program Files (x86)\\Origin Games\\Battlefield 1\\user.cfg",
        backup_path + "\\Documents\\Config\\Battlefield 1\\",
        True
    ),
    (
        "D:\\Origin\\Battlefield 3\\user.cfg",
        backup_path + "\\Documents\\Config\\Battlefield 3\\",
        True
    ),
    (
        "D:\\Origin\\Battlefield 4\\user.cfg",
        backup_path + "\\Documents\\Config\\Battlefield 4\\",
        True
    ),
    (
        "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Counter-Strike Global Offensive\\csgo\\cfg",
        backup_path + "\\Documents\\Config\\CSGO\\cfg\\",
        False
    )
]

failed = list()

for element in backup:
    if not xcopy(element[0],  element[1], element[2]):
        failed.append(element[0])

draw.line()
print("##############################")
print("##### Copying completed ######")
print("##############################")
draw.line()

if failed:
    print("Following files or directories were not found:")
    for path in failed:
        print(path)
    draw.line()

if dialog.yes_no("Compress backup and delete copied files?"):
    draw.line()
    os.system("7z a -t7z -m0=lzma2 -mx=9 -aoa -mfb=64 -md=32m -ms=on -mhe \"{0}\" \"{0}\"".format(backup_path))

    draw.line()
    print("Removing copied files...")
    os.system("RD \"{0}\" /s/q".format(backup_path))

    draw.line()
    print("#############################")
    print("###### Backup completed #####")
    print("#############################")

draw.line()
dialog.enter("exit")
