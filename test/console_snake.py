import os
from ctypes import *
from msvcrt import getch
from multiprocessing import Process, Value, Array
from random import randint
from time import clock, sleep


################################################################################
################################## Constants ###################################
################################################################################


BORDER = 0
FIELD = 1
BODY = 2
HEAD = 3
APPLE = 4

TYPES = [
    "█",  # Border
    " ",  # Field
    "B",  # Body
    "H",  # Head
    "A"  # Apple
]

VK_W = 119
VK_A = 97
VK_S = 115
VK_D = 100

STD_OUTPUT_HANDLE = -11
HANDLE = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)	


################################################################################
################################### Classes ####################################
################################################################################


class CursorInfo(Structure):
    _fields_ = [
        ("size", c_int),
        ("visible", c_byte)
    ]
    

class COORD(Structure): 
    _fields_ = [
        ("X", c_short), 
        ("Y", c_short)
    ]


class Grid:
    def __init__(self, rows, cols, initial):
        self.__array = Array("i", rows * cols * [initial])
        self.rows = rows
        self.cols = cols

    def __getitem__(self, key):
        r, c = key
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.__array[r * self.cols + c]
        else:
            raise IndexError("Index out of range")

    def __setitem__(self, key, value):
        r, c = key
        if 0 <= r < self.rows and 0 <= c < self.cols:
            self.__array[r * self.cols + c] = value
        else:
            raise IndexError("Index out of range")
            
    def create_border(self):
        for x in range(0, self.rows):
            self[x, 0] = self[x, self.cols - 1] = BORDER
        for y in range(0, self.cols):
            self[0, y] = self[self.rows - 1, y] = BORDER
            
            
class Snake:
    def __init__(self, rows, cols, default=VK_D):
        self.direction = Value("i", default)
        self.grid = Grid(rows, cols, FIELD)
        self.grid.create_border()
        
        self.body = [(1, 1)]
        self.grid[1, 1] = HEAD
        self.deploy_apple()
        self.dead = False
        
    def new_apple(self):
        return randint(1, self.grid.rows - 1), randint(1, self.grid.cols - 1)
        
    def deploy_apple(self):
        apple = self.new_apple()
        while self.grid[apple] != FIELD:
            apple = self.new_apple()
        self.grid[apple] = APPLE
        
    def new_head(self):
        x, y = self.body[0]
        if self.direction.value == VK_W:
            return x - 1, y
        if self.direction.value == VK_S:
            return x + 1, y
        if self.direction.value == VK_A:
            return x, y - 1
        if self.direction.value == VK_D:
            return x, y + 1
        
    def move(self):
        old_head = self.body[0]
        new_head = self.new_head()
        tail = self.body.pop()
        
        on_apple = self.grid[new_head] == APPLE
        self.dead = self.grid[new_head] in (BODY, BORDER)
        
        self.grid[old_head] = BODY
        self.grid[tail] = FIELD        
        self.grid[new_head] = HEAD
        
        self.body.insert(0, new_head)
        
        if on_apple:
            self.body.append(self.body[-1])
            self.deploy_apple()
            
            
class Timer:
    def __init__(self, fps):
        self.__fps = 1 / fps
        self.__clock = clock()

    def reset(self):
        self.__clock = clock()
    
    @property
    def ready(self):
        return self.__fps <= clock() - self.__clock


################################################################################
################################## Functions ###################################
################################################################################
    
    
def cursor_hide():
    ci = CursorInfo()
    windll.kernel32.GetConsoleCursorInfo(HANDLE, byref(ci))
    ci.visible = False
    windll.kernel32.SetConsoleCursorInfo(HANDLE, byref(ci))
    

def cursor_show():
    ci = CursorInfo()
    windll.kernel32.GetConsoleCursorInfo(HANDLE, byref(ci))
    ci.visible = True
    windll.kernel32.SetConsoleCursorInfo(HANDLE, byref(ci))


def cursor_reset():
    windll.kernel32.SetConsoleCursorPosition(HANDLE, COORD(0, 0))

        
def get_key(key):
    while True:
        vk = ord(getch())
        if vk in (VK_W, VK_A, VK_S, VK_D):
            key.value = vk
            
            
def render(grid):
    frame = 0
    timer = Timer(1)
    while True:
        cursor_reset()
        string = []
        for x in range(0, grid.rows):
            for y in range(0, grid.cols):
                string.append(TYPES[grid[x, y]])
            string.append("\n")
        print("".join(string), end="")
        frame += 1
        if timer.ready:
            print("fps:", frame)
            frame = 0
            timer.reset()
    
    
################################################################################
##################################### Main #####################################
################################################################################


def main():
    os.system("cls")
    cursor_hide()

    snake = Snake(25, 50)

    process_key = Process(target=get_key, args=(snake.direction,))
    process_key.start()
    process_render = Process(target=render, args=(snake.grid,))
    process_render.start()
    
    timer = Timer(10)
    while not snake.dead:
        if timer.ready:
            snake.move()
            timer.reset()
    
    process_key.terminate()
    process_render.terminate()
     
    os.system("cls")
    cursor_show()
    
    
if __name__ == "__main__":
    main()
