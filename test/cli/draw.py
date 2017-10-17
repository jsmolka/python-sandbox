from cli import *

c_print("a", "b", "c", color=[Color.CYAN, Color.INTENSE])
line(LineStyle.HASH, color=[Color.CYAN, Color.INTENSE])
line(LineStyle.SCORE, color=[Color.CYAN, Color.INTENSE])
line(LineStyle.UNDERSCORE, color=[Color.CYAN, Color.INTENSE])
heading("test", style=LineStyle.HASH ,color=[Color.CYAN, Color.INTENSE])
heading("test", style=LineStyle.SCORE ,color=[Color.CYAN, Color.INTENSE])
heading("test", style=LineStyle.UNDERSCORE ,color=[Color.CYAN, Color.INTENSE])
big_heading("test", style=LineStyle.HASH ,color=[Color.CYAN, Color.INTENSE])
big_heading("test", style=LineStyle.SCORE ,color=[Color.CYAN, Color.INTENSE])
big_heading("test", style=LineStyle.UNDERSCORE ,color=[Color.CYAN, Color.INTENSE])
menu("caption", "entry", "entry", "entry", caption_color=[Color.CYAN, Color.INTENSE], entry_color=[Color.MAGENTA, Color.INTENSE])
n = 10000
for i in range(0, n):
    progress_bar(i, n - 1, color=[Color.CYAN, Color.INTENSE])
enter("exit")
