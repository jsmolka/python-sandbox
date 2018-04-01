import fileutil as fu
import numpy as np
from PIL import Image


def save_color(color):
    img = Image.new("RGB", (100, 100), color)
    img.save("dominant.png", "PNG")


if __name__ == "__main__":
    files = fu.files(fu.PYDIR, pattern=["*.jpg", "*.jpeg", "*.png"])
    if len(files) > 0:
        data = np.array(Image.open(files[0]))
        r = 0
        g = 0
        b = 0
        rows = len(data)
        cols = len(data[0])

        count = 0
        for i in range(0, rows):
            for j in range(0, cols):
                r += data[i][j][0]
                g += data[i][j][1]
                b += data[i][j][2]
                count += 1

        color = (r // count, g // count, b // count)
        save_color(color)
