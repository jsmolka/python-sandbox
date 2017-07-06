import dialog
import draw
import os
import shutil
import sys


def create_copies(name, extension, number):
    """Creates copies of files"""
    py_path = os.path.dirname(sys.argv[0])
    extension = "." + extension
    name = py_path + "\\" + name
    os.rename(name + extension, name + " 1" + extension)
    for number in range(1, number):
        file1 = name + " " + str(number) + extension
        file2 = name + " " + str(number + 1) + extension
        shutil.copyfile(file1, file2)


def create_one_gb_file(name):
    """Creates a one gigabyte file"""
    name += ".txt"
    string = "0"
    multiplied_string = ""
    for j in range(0, 1024):
        multiplied_string += string
    file = open(name, "a+")
    for k in range(0, (1024 * 1024)):
        file.write(multiplied_string)
    file.close()


# Create text file
print("Enter text file name!")
file_name = input()
print("Creating text file...")
create_one_gb_file(file_name)
print("Success!")

# Pack text file
draw.line()
rar_file = file_name + ".rar"
txt_file = file_name + ".txt"
cmd = "rar a -r {0} {1}".format(rar_file, txt_file)
print("Packing text file...")
os.system(cmd)
print("Success!")

os.remove(txt_file)

# Start
draw.line()
pack = dialog.yes_no("Start duplicating?")
gigabyte = 1

# Duplicate
while pack:
    # Create copies
    draw.line()
    print("Creating copies...")
    create_copies(file_name, "rar", 10)
    print("Success!")
    old_name = file_name + " "
    gigabyte *= 10

    # Pack copies
    draw.line()
    source_files = file_name + "*.rar"
    print("Enter rar directory name!")
    file_name = input()
    target_file = file_name + ".rar"
    cmd = "rar a -r {0} {1}".format(target_file, source_files)
    print("Packing rar directories...")
    os.system(cmd)
    print("Success!")

    # Delete copies
    i = 1
    while i <= 10:
        os.remove(old_name + str(i) + ".rar")
        i += 1

    # Stop
    draw.line()
    pack = not dialog.yes_no("Stop duplicating?")

# End screen
draw.line()
print("Stopped packing!")

byte_name = "gigabyte"

if gigabyte % pow(10, 9) == 0:
    byte_name = "exabyte"
    gigabyte //= pow(10, 9)
elif gigabyte % pow(10, 6) == 0:
    byte_name = "petabyte"
    gigabyte //= pow(10, 6)
elif gigabyte % pow(10, 3) == 0:
    byte_name = "terabyte"
    gigabyte //= pow(10, 3)

print("Compressed", byte_name, "in", file_name + ".rar:", gigabyte)

dialog.enter("exit")
