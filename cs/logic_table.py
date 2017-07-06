import dialog
import draw
from logic import *

print("Input logic string!")
l = Logic(input())

draw.line()

print("Decrypted string:")
print(l.decrypted_string)

draw.line()

l.draw_table()

draw.line()

dialog.enter("exit")
