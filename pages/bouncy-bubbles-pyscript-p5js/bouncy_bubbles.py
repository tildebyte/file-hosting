# Bouncy Bubbles
# based on code from Keith Peters. Multiple-object collision.
# Adapted from https://p5js.org/examples/motion-bouncy-bubbles.html
# Port to pyscript by Ben Alkov, 2022-07

# We could also use p5.js' math functions, but might as well use Python's
import math

from typing import Any

from pyodide import ffi

from js import Window, window

# Convenience
p5js: Window = window


class Ball():
    def __init__(self, x: float, y: float, dia: float) -> None:
        self.x: float = x
        self.y: float = y
        self.diameter: float = dia
        self.vx = 0.0
        self.vy = 0.0

    def collide(self) -> None:
        for other_ball in BALLS:
            dx: float = other_ball.x - self.x
            dy: float = other_ball.y - self.y
            distance: float = math.sqrt(dx * dx + dy * dy)
            min_dist: float = other_ball.diameter / 2 + self.diameter / 2
            if (distance < min_dist):
                angle: float = math.atan2(dy, dx)
                targetX: float = self.x + math.cos(angle) * min_dist
                targetY: float = self.y + math.sin(angle) * min_dist
                ax: float = (targetX - other_ball.x) * SPRING
                ay: float = (targetY - other_ball.y) * SPRING
                self.vx -= ax
                self.vy -= ay
                other_ball.vx += ax
                other_ball.vy += ay

    def move(self) -> None:
        self.vy += GRAVITY
        self.x += self.vx
        self.y += self.vy
        if self.x + self.diameter / 2 > WIDTH:
            self.x = WIDTH - self.diameter / 2
            self.vx *= FRICTION
        elif self.x - self.diameter / 2 < 0:
            self.x = self.diameter / 2
            self.vx *= FRICTION

        if self.y + self.diameter / 2 > HEIGHT:
            self.y = HEIGHT - self.diameter / 2
            self.vy *= FRICTION
        elif (self.y - self.diameter / 2 < 0):
            self.y = self.diameter / 2
            self.vy *= FRICTION

    def display(self) -> None:
        p5js.ellipse(self.x, self.y, self.diameter, self.diameter)


NUM_BALLS = 13
SPRING = 0.05
GRAVITY = 0.03
FRICTION: float = -0.9
BALLS: list[Ball] = []
HEIGHT = 400
WIDTH = 720

# These functions are named per convention: p5.js doesn't know anything about them

def setup() -> None:
    global BALLS

    p5js.createCanvas(WIDTH, HEIGHT)
    BALLS = [Ball(p5js.random(WIDTH), p5js.random(HEIGHT), p5js.random(30, 70))
             for _ in range(NUM_BALLS)]
    p5js.noStroke()
    p5js.fill(255, 204)
    p5js.background(0)


def draw(*args: dict[str, Any]) -> None:
    p5js.background(0)
    for ball in BALLS:
        ball.collide()
        ball.move()
        ball.display()
    p5js.requestAnimationFrame(ffi.create_proxy(draw))


setup()
window.requestAnimationFrame(ffi.create_proxy(draw))
