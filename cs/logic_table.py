from cli import *
from logic import *

print("Input logic string!")
l = Logic(input())

line()

print("Decrypted string:")
print(l.decrypted_string)

line()

l.draw_table()

line()

enter("exit")
