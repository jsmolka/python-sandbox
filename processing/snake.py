from pyprocessing import *
from random import randint

SCALE = 20
HEIGHT = 20
WIDTH = 30


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False

    @staticmethod
    def make(p):
        return Point(p.x, p.y)


def N(p):
    p.y -= SCALE
    return p


def S(p):
    p.y += SCALE
    return p


def E(p):
    p.x += SCALE
    return p


def W(p):
    p.x -= SCALE
    return p


class Snake:
    def __init__(self):
        self.nodes = [Point(0, 0), Point(0, 0)]
        self.apple = Point(randint(0, WIDTH - 1) * SCALE, randint(0, HEIGHT - 1) * SCALE)
        self.direction = None
        self.directions = {
            "w": N,
            "s": S,
            "d": E,
            "a": W
        }

    def move(self):
        if not self.direction:
            return
        self.nodes.insert(0, Point.make(self.directions[self.direction](self.nodes[0])))
        self.nodes.pop()

    def set_direction(self, direction):
        if direction in ["w", "s", "d", "a"]:
            self.direction = direction

    def generate_apple(self):
        self.apple.x = randint(0, WIDTH - 1) * SCALE
        self.apple.y = randint(0, HEIGHT - 1) * SCALE

    def apple_in_snake(self):
        for p in snake.nodes:
            if p == self.apple:
                return True
        return False

    def deploy_apple(self):
        while self.apple_in_snake():
            self.generate_apple()

    def draw(self):
        background(0, 0, 255)
        fill(255, 0, 0)
        rect(self.apple.x, self.apple.y, SCALE, SCALE)
        fill(0, 255, 0)
        for p in self.nodes:
            rect(p.x, p.y, SCALE, SCALE)

    def check_apple(self):
        if self.nodes[0] == self.apple:
            self.expand_snake()
            self.deploy_apple()

    def expand_snake(self):
        self.nodes.append(Point.make(self.nodes[-1]))

    def out_of_bounds(self):
        if not 0 <= self.nodes[0].x < WIDTH * SCALE or not 0 <= self.nodes[0].y < HEIGHT * SCALE:
            return True
        return False

    def get_score(self):
        return len(self.nodes) - 2

    def inside_itself(self):
        for i in range(2, len(self.nodes)):
            if self.nodes[0] == self.nodes[i]:
                return True
        return False


def keyPressed():
    global snake
    snake.set_direction(key.char)


def setup():
    global snake
    size(WIDTH * SCALE, HEIGHT * SCALE)
    frameRate(10)
    noStroke()
    snake = Snake()


def draw():
    global snake
    snake.move()
    snake.draw()
    if snake.out_of_bounds() or snake.inside_itself():
        fill(255)
        print("Score:", snake.get_score())
        text("Game Over", WIDTH * SCALE / 2 - 25, HEIGHT * SCALE / 2)
        noLoop()
    snake.check_apple()

run()
