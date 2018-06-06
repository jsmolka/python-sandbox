import os
import cursor
import msvcrt
import multiprocessing as mp
import random
import time

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


class Grid:
    """Grid class."""
    def __init__(self, rows, cols, initial):
        """Constructor."""
        self.__array = mp.Array("i", rows * cols * [initial])
        self.rows = rows
        self.cols = cols

    def __getitem__(self, key):
        """Numpy-like getter."""
        r, c = key
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.__array[r * self.cols + c]
        else:
            raise IndexError("Index ({}, {}) out of range".format(r, c))

    def __setitem__(self, key, value):
        """Numpy-like setter."""
        r, c = key
        if 0 <= r < self.rows and 0 <= c < self.cols:
            self.__array[r * self.cols + c] = value
        else:
            raise IndexError("Index ({}, {}) out of range".format(r, c))
            
    def create_border(self):
        """Creates border."""
        print(self.rows, self.cols)
        for x in range(self.rows):
            self[x, 0] = self[x, self.cols - 1] = BORDER
        for y in range(self.cols):
            self[0, y] = self[self.rows - 1, y] = BORDER
            
            
class Snake:
    """Snake class."""
    def __init__(self, rows, cols, default=VK_D):
        """Constructor."""
        self.direction = mp.Value("i", default)
        self.grid = Grid(rows, cols, FIELD)
        self.grid.create_border()
        
        self.body = [(1, 1)]
        self.grid[1, 1] = HEAD
        self.deploy_apple()
        self.dead = False
        
    def new_apple(self):
        """Create new apple."""
        return random.randint(1, self.grid.rows - 1), random.randint(1, self.grid.cols - 1)
        
    def deploy_apple(self):
        """Deploys new apple."""
        apple = self.new_apple()
        while self.grid[apple] != FIELD:
            apple = self.new_apple()
        self.grid[apple] = APPLE
        
    def new_head(self):
        """Sets new head."""
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
        """Moves snake."""
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
    """Timer class."""
    def __init__(self, fps):
        """Constructor."""
        self._fps = 1 / fps
        self._clock = time.clock()

    def reset(self):
        """Resets timer."""
        self._clock = time.clock()
    
    @property
    def ready(self):
        """Ready property."""
        return self._fps <= time.clock() - self._clock

        
def get_key(key):
    """Read key input."""
    while True:
        vk = ord(msvcrt.getch())
        if vk in (VK_W, VK_A, VK_S, VK_D):
            key.value = vk
            
            
def render(grid):
    """Renders grid"""
    frame = 0
    timer = Timer(1)
    while True:
        cursor.reset()
        string = []
        for x in range(grid.rows):
            for y in range(grid.cols):
                string.append(TYPES[grid[x, y]])
            string.append("\n")
        print("".join(string), end="")
        frame += 1
        if timer.ready:
            print("fps:", frame)
            frame = 0
            timer.reset()


def main():
    """Main loop."""
    os.system("cls")
    cursor.hide()

    snake = Snake(25, 50)

    process_key = mp.Process(target=get_key, args=(snake.direction,))
    process_key.daemon = True
    process_key.start()
    process_render = mp.Process(target=render, args=(snake.grid,))
    process_render.daemon = True
    process_render.start()
    
    timer = Timer(10)
    while not snake.dead:
        if timer.ready:
            snake.move()
            timer.reset()
    
    process_key.terminate()
    process_render.terminate()
     
    os.system("cls")
    cursor.show()
    
    
if __name__ == "__main__":
    main()
