import cursor
import os
from constants import *
from key import get_key
from multiprocessing import Process
from render import render
from snake import Snake


if __name__ == "__main__":

    os.system("cls")
    cursor.hide()

    snake = Snake(20, 40)

    process_key = Process(target=get_key, args=(snake.direction,))
    process_key.start()
    process_render = Process(target=render, args=(snake.grid,))
    process_render.start()
    
    while snake.direction.value != VK_W:
        pass
        
    process_key.terminate()
    process_render.terminate()
