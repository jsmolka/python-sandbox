from constants import *
from msvcrt import getch

        
def get_key(k):
    while True:
        vk = ord(getch())
        if vk in (VK_W, VK_A, VK_S, VK_D):
            k.value = vk