# This module adds the target_dir to PYTHONPATH
# It adds the sub_dir if it is assigned
# It adds the python_dir if the sub_dir is not assigned
import os
import platform


def dialog_enter(action, message="Press enter to {0}..."):
    """Prints enter message"""
    message = message.format(action)
    input(message)


def draw___default():
    """Calculates default line for windows version"""
    system = platform.release()
    if system == "7":
        default_line = "-" * 79
    else:
        default_line = "-" * 119
    return default_line


def draw_line():
    """Prints line"""
    default_line = draw___default()
    print(default_line)


# Define directories
sub_dir = "__modules__"
python_dir = os.path.dirname(os.path.abspath(__file__))
if sub_dir != "":
    target_dir = python_dir + "\\" + sub_dir
else:
    target_dir = python_dir

print("Adding directory: {0}".format(target_dir))

# Append target_dir to PYTHONPATH
if "PYTHONPATH" in os.environ:
    path_string = os.environ["PYTHONPATH"]
    path_list = path_string.split(";")
    if target_dir in path_list:
        draw_line()
        print("Directory already exists in PYTHONPATH")
    else:
        cmd = "setx PYTHONPATH \"%PYTHONPATH%;{0}\"".format(target_dir)
        draw_line()
        os.system(cmd)
        draw_line()
        print("Added directory to PYTHONPATH")

else:  # Create PYTHONPATH and appending target_dir
    cmd = "setx PYTHONPATH \"{0}\"".format(target_dir)
    draw_line()
    os.system(cmd)
    draw_line()
    print("Created PYTHONPATH")
    draw_line()
    print("Added directory to PYTHONPATH")

draw_line()

dialog_enter("exit")
