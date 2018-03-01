import random
from pyprocessing import *

# Configuration
WIDTH = 1000
HEIGHT = 500

GRAVITY = 1

fireworks = []
F_COUNT = 5
F_D = 8
F_COLOR_MIN = 128
F_COLOR_MAX = 256
F_VEL_MIN = 18
F_VEL_MAX = 29

P_COUNT = 35
P_D = 10
P_STEPS = 15
P_VEL_MIN = -10
P_VEL_MAX = 10


class Particle:
    def __init__(self, x, y, c):
        """Constructor."""
        self.x = x
        self.y = y
        self.c = c
        self.d = P_D  # Diameter
        self.vv = random.randint(P_VEL_MIN, P_VEL_MAX)
        self.hv = random.randint(P_VEL_MIN, P_VEL_MAX)
        self.vg = GRAVITY  # Vertical gravity

        self.faded = False
        self.fading_steps = P_STEPS

    def move(self):
        """Moves particle."""
        if not self.faded:
            if self.vv != 0:
                self.y -= self.vv
            if self.hv != 0:
                self.x -= self.hv

            if self.fading_steps <= 10:
                if 0 <= self.y <= HEIGHT:
                    self.vv -= self.vg

            self.fading_steps -= 1

    def draw(self):
        """Draws particle."""
        if not self.faded:
            if 0 <= self.x <= WIDTH:
                if 0 <= self.y <= HEIGHT:
                    ellipse(self.x, self.y, self.d, self.d)

            if self.fading_steps <= 0:
                self.faded = True


class Fireworks:
    def __init__(self):
        """Constructor."""
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(HEIGHT, HEIGHT * 4)
        self.c = random.randint(F_COLOR_MIN, F_COLOR_MAX)
        self.v = random.randint(F_VEL_MIN, F_VEL_MAX)
        self.d = F_D  # Diameter
        self.g = GRAVITY  # Vertical gravity

        self.exploded = False
        self.particles = []

    def move(self):
        """Moves rocket."""
        if not self.exploded:
            self.y -= self.v
            if 0 <= self.y <= HEIGHT:
                self.v -= self.g
            if self.v <= 0:
                self.explode()
        else:
            should_reset = True
            for p in self.particles:
                p.move()
                p.draw()
                if not p.faded:
                    should_reset = False
            if should_reset:
                self.__init__()

    def draw(self):
        """Draw rocket."""
        if not self.exploded:
            if 0 <= self.x <= WIDTH:
                if 0 <= self.y <= HEIGHT:
                    ellipse(self.x, self.y, self.d, self.d)

    def explode(self):
        """Explodes rocket."""
        self.exploded = True
        for i in range(P_COUNT):
            p = Particle(self.x, self.y, self.d)
            self.particles.append(p)


def setup():
    """Setup."""
    global fireworks, F_COUNT
    size(WIDTH, HEIGHT)
    frameRate(45)
    for i in range(F_COUNT):
        fw = Fireworks()
        fireworks.append(fw)


def draw():
    """Draw."""
    global fireworks
    fill(0, 60)
    noStroke()
    rect(0, 0, WIDTH, HEIGHT)
    colorMode(HSB)  # Colorful color mode
    for fw in fireworks:
        fill(fw.c)
        fw.move()
        fw.draw()
    colorMode(RGB)


run()
