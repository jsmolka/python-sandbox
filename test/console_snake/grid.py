from constants import *
from multiprocessing import Array


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
        
