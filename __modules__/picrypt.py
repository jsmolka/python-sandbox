import numpy as np
from random import randint
from math import sqrt, ceil
from PIL import Image

# Ideas
# Uses [r, g, b] as separate bytes
# [bin(r), bin(g), bin(b)] = 2^24 possible numbers -> Unicode maybe?

class Picrypt:
    def __init__(self):
        """Constructor"""
        self.image = None
        self.text = None

    @staticmethod
    def pi(n):
        """Calculates n digits of pi using the spigot algorithm"""
        l = list()
        k, a, b, a1, b1 = 2, 4, 1, 12, 4
        while n > 0:
            p, q, k = k * k, 2 * k + 1, k + 1
            a, b, a1, b1 = a1, b1, p * a + q * a1, p * b + q * b1
            d, d1 = a / b, a1 / b1
            while d == d1 and n > 0:
                l.append(int(d))
                n -= 1
                a, a1 = 10 * (a % b), 10 * (a1 % b1)
                d, d1 = a / b, a1 / b1
        return l

    def encrypt(self, s):
        """Encrypts a string"""
        n = len(s)
        rpi = list(reversed(Picrypt.pi(n)))
        pxl = list()
        print(n)
        pxl.append(n)
        for i in range(0, n):
            o = ord(s[i]) - rpi[-i - 1]
            if not 0 <= o < 128:
                raise Exception("Picrypt is only defined for ASCII characters")
            pxl.append(o)
            for j in range(0, rpi[i]):
                pxl.append(randint(0, 128))
        sqr = int(ceil(sqrt(len(pxl))))
        pic = np.zeros((sqr, sqr), dtype=np.uint8)
        r = c = 0
        for i in range(0, sqr ** 2):
            if c == sqr:
                c = 0
                r += 1
            if i < len(pxl):
                pic[r, c] = pxl[i]
            else:
                pic[r, c] = randint(0, 128)
            c += 1
        self.image = Image.fromarray(pic, "L")
        return self.image

    def decrypt(self, img):
        """Decrypts an image"""
        a = np.array(img, dtype=np.uint8)
        pxl = list()
        for i in range(0, len(a)):
            for j in range(0, len(a[0])):
                pxl.append(a[i, j])
        n = pxl.pop(0)
        rpi = list(reversed(Picrypt.pi(n)))
        self.text = ""
        j = 0
        for i in range(0, n):
            self.text += chr(pxl[j] + rpi[-i - 1])
            j += rpi[i] + 1
        return self.text

    def save_image(self, file_name):
        """Saves encrypted image"""
        if self.image is None:
            raise Exception("Image is not assigned")
        self.image.save(file_name, "png")

    def save_text(self, file_name):
        """Saves decrypted text"""
        if self.text is None:
            raise Exception("Text is not assigned")
        with open(file_name, "w") as f:
            f.write(self.text)

    @staticmethod
    def load_image(file_name):
        """Loads encrypted image"""
        return Image.open(file_name)

    @staticmethod
    def load_text(file_name):
        """Loads decrypted text"""
        with open(file_name, "r") as f:
            s = f.read()
        return s


pc = Picrypt()
pc.encrypt(Picrypt.load_text("in.txt"))
pc.save_image("test.png")
pc.decrypt(Picrypt.load_image("test.png"))
pc.save_text("out.txt")








