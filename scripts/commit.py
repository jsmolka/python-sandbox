import os

os.chdir("C:\\Users\\Julian\\OneDrive\\Coding\\Python")

print("Input commit message!")
message = input()

os.system("git add --all & git commit -m \"{0}\" & git push origin master".format(message))
