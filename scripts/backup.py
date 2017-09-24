import dialog
import draw
import datetime
import os


def xcopy(source, target):
    """Copies directory or file"""
    if os.path.exists(source):

        if os.path.isfile(source):  # Copy file
            exit_code = os.system("xcopy \"{0}\" \"{1}\"".format(source, target))
        else:  # Copy directory
            exit_code = os.system("xcopy \"{0}\" \"{1}\" /s/h/e/k/f/c".format(source, target))

        if exit_code == 0:
            return True
        else:
            return False
    else:
        return False


today = datetime.date.today()
backup_name = "Backup {0}".format(today.strftime("%d-%m-%y"))
backup_path = "D:\\Backup\\" + backup_name

backup = [
    # (
    #   source,
    #   target
    # )
    (
        "C:\\Users\\Julian\\OneDrive\\Coding",
        backup_path + "\\Coding\\"
    ),
    (
        "C:\\Users\\Julian\\OneDrive\\Studium",
        backup_path + "\\Studium\\"
    ),
    (
        "C:\\Users\\Julian\\OneDrive\\Sonstiges",
        backup_path + "\\Sonstiges\\"
    ),
    (
        "C:\\Users\\Julian\\OneDrive\\Pictures",
        backup_path + "\\Pictures\\"
    ),
    (
        "C:\\Users\\Julian\\OneDrive\\Documents",
        backup_path + "\\Documents\\"
    ),
    (
        "C:\\Users\\Julian\\Documents\\Battlefield 1\\settings",
        backup_path + "\\Documents\\Config\\Battlefield 1\\"
    ),
    (
        "C:\\Users\\Julian\\Documents\\Battlefield 3\\settings",
        backup_path + "\\Documents\\Config\\Battlefield 3\\"
    ),
    (
        "C:\\Users\\Julian\\Documents\\Battlefield 4\\settings",
        backup_path + "\\Documents\\Config\\Battlefield 4\\"
    ),
    (
        "C:\\Program Files (x86)\\Origin Games\\Battlefield 1\\user.cfg",
        backup_path + "\\Documents\\Config\\Battlefield 1\\"
    ),
    (
        "D:\\Origin\\Battlefield 3\\user.cfg",
        backup_path + "\\Documents\\Config\\Battlefield 3\\"
    ),
    (
        "D:\\Origin\\Battlefield 4\\user.cfg",
        backup_path + "\\Documents\\Config\\Battlefield 4\\"
    ),
    (
        "D:\\Steam\\steamapps\\common\\Counter-Strike Global Offensive\\csgo\\cfg",
        backup_path + "\\Documents\\Config\\CSGO\\cfg\\"
    )
]

failed = list()

for element in backup:
    if not xcopy(element[0],  element[1]):
        failed.append(element[0])

draw.line()
print("##############################")
print("##### Copying completed ######")
print("##############################")
draw.line()

if failed:
    print("Following files or directories were not found or failed copying:")
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
