from random import randint

ascii_min = 33
ascii_max = 126
length = int(input("Input password length: "))
count = int(input("Password count: "))

for i in range(0, count):
    pw = ""
    for j in range(0, length):
        pw += chr(randint(ascii_min, ascii_max))
    print(pw)

input()