# Ported to pyscript/p5.js by Ben Alkov, 2022-07-04
# Ported to Processing.py by Ben Alkov, 2014-07-10
# Based on "Web of stars" by Jerome Herr, May 8th, 2014
# Licensed by him as https://creativecommons.org/licenses/by-sa/3.0
# https://openprocessing.org/sketch/147466

# Not strictly necessary, but seeing naked e.g. `document`, `window`, etc. really bothers me
import js

from pyodide import create_proxy

NumBalls = 60
Balls = None
Width = 800
Height = 450

p5js = js.window
TAU = p5js.PI * 2


class Ball(object):
    EdgeBuffer = 50

    def __init__(self, index):
        self.index = index
        self.origin = p5js.createVector(p5js.random(Ball.EdgeBuffer,
                                                    Width - Ball.EdgeBuffer),
                                        p5js.random(Ball.EdgeBuffer,
                                                    Height - Ball.EdgeBuffer))
        self.radius = p5js.random(50.0, 150.0)
        self.location = p5js.createVector(self.origin.x + self.radius,
                                          self.origin.y)
        if p5js.random(1) > 0.5:
            self.direction = -1
        else:
            self.direction = 1
        self.offset = p5js.random(TAU)
        self.theta = 0.0
        self.size = 10.0
        self.distanceLimit = 60

    def run(self, balls):
        self.move()
        self.display()
        self.lineBetween(balls)

    def move(self):
        self.location.x = (self.origin.x
                           + p5js.sin(self.theta + self.offset)
                           * self.radius)
        self.location.y = (self.origin.y
                           + p5js.cos(self.theta + self.offset)
                           * self.radius)
        # 0.02615 is sine of 1.5 degrees
        self.theta += (0.02615 * self.direction)

    def display(self):
        p5js.noStroke()
        for idx in range(5):
            p5js.fill(255, idx * 50)
            p5js.ellipse(self.location.x, self.location.y,
                         self.size - 2 * idx, self.size - 2 * idx)

    def lineBetween(self, balls):
        for ball in balls:
            if self.index is not ball.index:
                distance = self.location.dist(ball.location)
                if 0 < distance < self.distanceLimit:
                    p5js.stroke(0x96ffffff)
                    p5js.line(self.location.x, self.location.y,
                              ball.location.x, ball.location.y)


# These are named per convention: p5.js doesn't know anything about them

def setup():
    global Balls

    renderer = p5js.createCanvas(Width, Height)
    renderer.style('display', 'block')
    p5js.background(10)
    Balls = [Ball(i)
             for i in range(NumBalls)]


def draw(*args):
    p5js.noStroke()
    # p5js.blendMode(p5js.BLEND)
    p5js.fill(0, 20)
    p5js.rect(0, 0, Width, Height)
    for ball in Balls:
        ball.run(Balls)
    p5js.requestAnimationFrame(create_proxy(draw))


setup()
js.window.requestAnimationFrame(create_proxy(draw))
