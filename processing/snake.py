from pyprocessing import *
from random import randint
from sys import maxsize

SCALE = 10
HEIGHT = 60
WIDTH = 100
FRAME_RATE = 200
AI = True


class Point:
    def __init__(self, x, y):
        """Constructor."""
        self.x = x
        self.y = y

    def __eq__(self, other):
        """Equal."""
        return self.x == other.x and self.y == other.y

    @staticmethod
    def make(point):
        """Create new point."""
        return Point(point.x, point.y)


def N(point):
    """Go north."""
    point.y -= SCALE
    return point


def S(point):
    """Go south."""
    point.y += SCALE
    return point


def E(point):
    """Go east."""
    point.x += SCALE
    return point


def W(point):
    """Go west."""
    point.x -= SCALE
    return point


class Snake:
    """Snake class."""
    def __init__(self):
        """Constructor."""
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
        """Moves snake."""
        if not self.direction:
            return
        self.nodes.insert(0, Point.make(self.directions[self.direction](self.nodes[0])))
        self.nodes.pop()

    def set_direction(self, direction):
        """Sets direction."""
        if direction in ["w", "s", "d", "a"]:
            self.direction = direction

    def generate_apple(self):
        """Generates apple."""
        self.apple.x = randint(0, WIDTH - 1) * SCALE
        self.apple.y = randint(0, HEIGHT - 1) * SCALE

    def apple_in_snake(self):
        """Checks if apple is in snake."""
        for p in snake.nodes:
            if p == self.apple:
                return True
        return False

    def deploy_apple(self):
        """Deploys new apple."""
        while self.apple_in_snake():
            self.generate_apple()

    def draw(self):
        """Draws snake."""
        background(0, 0, 255)
        fill(255, 0, 0)
        rect(self.apple.x, self.apple.y, SCALE, SCALE)
        fill(0, 255, 0)
        for p in self.nodes:
            rect(p.x, p.y, SCALE, SCALE)

    def check_apple(self):
        """Checks if apple in head."""
        if self.nodes[0] == self.apple:
            self.expand_snake()
            self.deploy_apple()

    def expand_snake(self):
        """Expands snake."""
        self.nodes.append(Point.make(self.nodes[-1]))

    def out_of_bounds(self):
        """Checks if snake is out of bounds."""
        return not 0 <= self.nodes[0].x < WIDTH * SCALE or not 0 <= self.nodes[0].y < HEIGHT * SCALE

    def get_score(self):
        """Gets score."""
        return len(self.nodes) - 2

    def inside_itself(self):
        """Checks if snake ate ifself."""
        for i in range(2, len(self.nodes)):
            if self.nodes[0] == self.nodes[i]:
                return True
        return False

    def distance(self, point):
        """Calculates distance to apple"""
        if point is None:
            return maxsize
        return abs((point.x - self.apple.x) ** 2 + (point.y - self.apple.y) ** 2)

    def look_ahead(self, point):
        """Looks ahead on step"""
        directions = [N(Point.make(point)), S(Point.make(point)), E(Point.make(point)), W(Point.make(point))]
        for point in directions:
            if not point in self.nodes:
                return True
        return False

    def ai(self):
        """AI function."""
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
    """Key pressed event."""
    global snake
    snake.set_direction(key.char)


def setup():
    """Setup."""
    global snake
    size(WIDTH * SCALE, HEIGHT * SCALE)
    frameRate(FRAME_RATE)
    noStroke()
    snake = Snake()


def draw():
    """Draw."""
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
