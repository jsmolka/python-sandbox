from pyprocessing import *
from random import randint
from sys import maxsize

SCALE = 20
HEIGHT = 30
WIDTH = 50
FRAME_RATE = 15
AI = False


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

    def distance(self, p):
        if p is None:
            return maxsize
        return abs((p.x - self.apple.x) ** 2 + (p.y - self.apple.y) ** 2)

    def look_ahead(self, p):
        directions = [N(Point.make(p)), S(Point.make(p)), E(Point.make(p)), W(Point.make(p))]
        for p in directions:
            if not p in self.nodes:
                return True
        return False

    def ai(self):
        head = self.nodes[0]
        directions = [N(Point.make(head)), S(Point.make(head)), E(Point.make(head)), W(Point.make(head))]
        for i in range(0, len(directions)):
            directions[i] = None if directions[i] in self.nodes else directions[i]
        adjacent = [
            ["w", self.distance(directions[0])],
            ["s", self.distance(directions[1])],
            ["d", self.distance(directions[2])],
            ["a", self.distance(directions[3])]
        ]
        adjacent.sort(key=lambda x: x[1])
        for i in range(0, len(adjacent)):
            if self.look_ahead(self.directions[adjacent[i][0]](Point.make(head))):
                self.set_direction(adjacent[i][0])
                break


def keyPressed():
    global snake
    snake.set_direction(key.char)


def setup():
    global snake
    size(WIDTH * SCALE, HEIGHT * SCALE)
    frameRate(FRAME_RATE)
    noStroke()
    snake = Snake()


def draw():
    global snake
    if AI:
        snake.ai()
    snake.move()
    snake.draw()
    if snake.out_of_bounds() or snake.inside_itself():
        fill(255)
        print("Score:", snake.get_score())
        text("Game Over", WIDTH * SCALE / 2 - 25, HEIGHT * SCALE / 2)
        noLoop()
    snake.check_apple()

run()
