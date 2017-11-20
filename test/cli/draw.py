from cli import *

cprint("a", "b", "c", color=[Color.CYAN, Color.INTENSE])
line(Style.HASH, color=[Color.CYAN, Color.INTENSE])
line(Style.SCORE, color=[Color.CYAN, Color.INTENSE])
line(Style.UNDERSCORE, color=[Color.CYAN, Color.INTENSE])
heading("test", style=Style.HASH ,color=[Color.CYAN, Color.INTENSE])
heading("test", style=Style.SCORE ,color=[Color.CYAN, Color.INTENSE])
heading("test", style=Style.UNDERSCORE ,color=[Color.CYAN, Color.INTENSE])
big_heading("test", style=Style.HASH ,color=[Color.CYAN, Color.INTENSE])
big_heading("test", style=Style.SCORE ,color=[Color.CYAN, Color.INTENSE])
big_heading("test", style=Style.UNDERSCORE ,color=[Color.CYAN, Color.INTENSE])
menu("caption", "entry", "entry", "entry", color=[Color.CYAN, Color.INTENSE])
n = 10000
for i in range(0, n):
    progress_bar(i, n - 1, color=[Color.CYAN, Color.INTENSE])
enter("exit")
