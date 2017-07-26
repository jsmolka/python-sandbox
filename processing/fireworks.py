import random
from pyprocessing import *

# Configuration
WIDTH = 1000
HEIGHT = 500

vertical_gravity = 1

fireworks = []
fireworks_count = 5
fireworks_diameter = 8
fireworks_color_min = 128
fireworks_color_max = 256
fireworks_velocity_min = 18
fireworks_velocity_max = 29

particle_count = 35
particle_diameter = 10
particle_fading_steps = 15
particle_velocity_min = -10
particle_velocity_max = 10


class Particle:
    def __init__(self, x, y, c):
        """Constructor"""
        self.x = x
        self.y = y
        self.c = c
        self.d = particle_diameter  # Diameter
        self.vv = random.randint(particle_velocity_min, particle_velocity_max)
        self.hv = random.randint(particle_velocity_min, particle_velocity_max)
        self.vg = vertical_gravity  # Vertical gravity

        self.faded = False
        self.fading_steps = particle_fading_steps

    def move(self):
        """Moves particle"""
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
        """Draws particle"""
        if not self.faded:
            if 0 <= self.x <= WIDTH:
                if 0 <= self.y <= HEIGHT:
                    ellipse(self.x, self.y, self.d, self.d)

            if self.fading_steps <= 0:
                self.faded = True


class Fireworks:
    def __init__(self):
        """Constructor"""
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(HEIGHT, HEIGHT * 4)
        self.c = random.randint(fireworks_color_min, fireworks_color_max)
        self.v = random.randint(fireworks_velocity_min, fireworks_velocity_max)
        self.d = fireworks_diameter  # Diameter
        self.g = vertical_gravity  # Vertical gravity

        self.exploded = False
        self.particles = []

    def move(self):
        """Moves rocket"""
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
        """Draw rocket"""
        if not self.exploded:
            if 0 <= self.x <= WIDTH:
                if 0 <= self.y <= HEIGHT:
                    ellipse(self.x, self.y, self.d, self.d)

    def explode(self):
        """Explodes rocket"""
        self.exploded = True
        for i in range(0, particle_count):
            p = Particle(self.x, self.y, self.d)
            self.particles.append(p)


def setup():
    global fireworks, fireworks_count
    size(WIDTH, HEIGHT)
    frameRate(45)
    for i in range(0, fireworks_count):
        fw = Fireworks()
        fireworks.append(fw)


def draw():
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
