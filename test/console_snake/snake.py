from constants import *
from grid import Grid
from multiprocessing import Value


class Snake:
    def __init__(self, rows, cols, default=VK_D):
        self.rows = rows
        self.cols = cols
        self.direction = Value("i", default)
        self.grid = Grid(rows, cols, FIELD)
        self.grid.create_border()