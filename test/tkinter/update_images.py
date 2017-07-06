import tkinter as tk
from PIL import Image, ImageTk
from maze import *

root = tk.Tk()

m = Maze()
m.create(100, 100, Algorithm.Create.BACKTRACKING)
img = Image.fromarray(Maze.upscale(m.maze, 3))
photo = ImageTk.PhotoImage(img)

label = tk.Label(image=photo)
label.image = photo  # keep a reference!
label.pack(side="bottom", fill="both", expand="yes")

# root.mainloop()
while True:  # Replace mainloop
    root.update_idletasks()  # Needed

    m.create(100, 100, Algorithm.Create.BACKTRACKING)
    img = Image.fromarray(Maze.upscale(m.maze, 3))
    photo = ImageTk.PhotoImage(img)
    label.image = photo  # keep a reference!
    label.configure(image=photo)

    root.update()  # Needed
