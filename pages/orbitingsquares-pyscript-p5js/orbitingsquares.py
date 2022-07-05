# 1. One hundred squares
# 2. Of randomly-selected size
# 3. Each having semi-tranparent fill and stroke
# 4. Each colored according to an underlying algorithm
# 5. Each rotating around its own center with a randomly-selected speed and
#    direction
# 6. Randomly distributed around the circumference of
# 7. One of several concentric circles
# 8. All squares rotating at a randomly-selected speed and direction around
#    a common center point
#
# Port to pyscript/p5.js by Ben Alkov 2022-07
# Initial Processing.py implementation 2014-08-07 - 12:
# https://github.com/tildebyte/processing.py-demos/blob/master/OrbitingSquares_HYPE/OrbitingSquares_HYPE.pyde

# Copyright 2022 Ben Alkov
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#   http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Note that we have a weird bug here, where the squares' fills don't render
# after the initial frame

import math

# Not strictly necessary, but seeing naked e.g. `document`, `window`, etc. really bothers me
import js
from pyodide import create_proxy

NUM_SQUARES = 100
BLUE = None
DK_BLUE = None
GREEN = None
DK_GREEN = None
SQUARES = None
HEIGHT = 720
WIDTH = 1280

p5js = js.window


class Square():
    # p5.js DEFAULT IS RADIANS!!
    ROTATION_LIMIT = 0.03
    ROTATION_TOLERANCE = 0.009
    ORBIT_LIMIT = 0.003
    ORBIT_TOLERANCE = 0.0001

    def __init__(self):
        self._orbit = self._chooseOrbit() + p5js.random(0, int(WIDTH / 23))
        self._orbit_angle = p5js.random(math.tau)
        self._position = p5js.createVector(math.cos(self._orbit_angle) * self._orbit,
                                           math.sin(self._orbit_angle) * self._orbit)
        self._size = p5js.random(int(WIDTH / 30), int(WIDTH / 20))
        self._rot_angle = p5js.random(math.tau)
        self._s_color = p5js.color(0)
        self._s_opac = p5js.map(self._size, WIDTH / 30, WIDTH / 20, 150, 200)
        self._f_color = None
        self._f_opac = p5js.map(self._size, WIDTH / 30, WIDTH / 20, 150, 200)
        self._recolor()
        self._rot_speed = Square.avoidZero(Square.ROTATION_LIMIT, Square.ROTATION_TOLERANCE)
        self._orbit_speed = Square.avoidZero(Square.ORBIT_LIMIT, Square.ORBIT_TOLERANCE)

    @staticmethod
    def avoidZero(limit, tolerance):
        '''
        This is specifically used to avoid zero or synchronous rotation. We want all
        visible rects to *appear* to rotate "in place".
        Return a random value in the range from `-limit` to strictly less than
        `limit`, excluding the inner range +/-`tolerance` (and, logically, zero as
        well).
        '''
        value = p5js.random(-limit, limit)
        while -tolerance < value < tolerance:
            value = p5js.random(-limit, limit)
            continue
        return value

    def _chooseOrbit(self):
        '''
        Randomly choose an orbit, based on a set of weights.
        The returns can be adjusted to account for a larger / smaller sketch size.
        '''
        chance = p5js.random(0, 1)
        if chance < 0.18:
            return (WIDTH / 8) * 2
        elif chance < 0.50:
            return (WIDTH / 4) * 2
        elif chance < 0.78:
            return (WIDTH / 2.46) * 2
        elif chance < 1.0:
            return (WIDTH / 1.7777) * 2

    def _move(self):
        '''
        Generate a random position on the circumference of the orbit chosen for
        this item.
        '''
        x = self._position.x
        y = self._position.y
        self._position.x = x * math.cos(self._orbit_speed) + y * math.sin(self._orbit_speed)
        self._position.y = y * math.cos(self._orbit_speed) - x * math.sin(self._orbit_speed)
        self._orbit_angle = math.atan2(self._position.y, self._position.x)

    def _recolor(self):
        angle = abs(self._orbit_angle)
        half_pi = math.pi / 2
        # Left half
        if angle >= half_pi:
            shade = p5js.map(angle, math.pi, half_pi, 0, 0.5)
            this_fill_color = GREEN
            other_fill_color = BLUE
            this_stroke_color = DK_GREEN
            other_stroke_color = DK_BLUE
        # Right half
        else:
            shade = p5js.map(angle, 0, half_pi, 0, 0.5)
            this_fill_color = BLUE
            other_fill_color = GREEN
            this_stroke_color = DK_BLUE
            other_stroke_color = DK_GREEN
        self._f_color = p5js.lerpColor(this_fill_color, other_fill_color,
                                       shade + p5js.random(-0.02, 0.02))
        self._s_color = p5js.lerpColor(this_stroke_color, other_stroke_color,
                                       shade + p5js.random(-0.02, 0.02))

    def draw(self):
        self._move()
        self._recolor()
        self._s_color.setAlpha(self._s_opac)
        p5js.stroke(self._s_color)
        self._f_color.setAlpha(self._f_opac)
        p5js.fill(self._f_color)
        p5js.push()
        p5js.translate(self._position.x, self._position.y)
        self._rot_angle += self._rot_speed
        p5js.rotate(self._rot_angle)
        p5js.rect(0, 0, self._size, self._size)
        p5js.pop()

    def __str__(self) -> str:
        return(f'Square:\n'
               f'orbit: {self._orbit}\n'
               f'orbit_angle: {self._orbit_angle}\n'
               f'position: {self._position}\n'
               f'size: {self._size}\n'
               f'rot_angle: {self._rot_angle}\n'
               f's_color: {self._s_color}\n'
               f'f_color: {self._f_color}\n'
               f'rot_speed: {self._rot_speed}\n'
               f'orbit_speed: {self._orbit_speed}\n'
               )


# These are named per convention: p5.js doesn't know anything about them

def setup():
    global SQUARES
    global BLUE
    global DK_BLUE
    global GREEN
    global DK_GREEN

    p5js.frameRate(60)
    p5js.createCanvas(WIDTH, HEIGHT, p5js.WEBGL)
    # 2D renderer
    # p5js.createCanvas(WIDTH, HEIGHT)
    p5js.setAttributes('antialias', True)
    # p5js.strokeCap(p5js.SQUARE)  # Not available for WEBGL
    p5js.strokeWeight(2)
    p5js.rectMode(p5js.CENTER)
    p5js.background(p5js.color(70, 71, 76))
    BLUE = p5js.color(21, 21, 235)
    DK_BLUE = p5js.color(10, 10, 115)
    GREEN = p5js.color(149, 194, 81)
    DK_GREEN = p5js.color(57, 74, 31)
    SQUARES = [Square() for _ in range(NUM_SQUARES)]


def draw(*args):
    p5js.background(p5js.color(70, 71, 76))
    # Remove if using 2D renderer!
    # p5js.translate(640, 360, 0)
    for square in SQUARES:
        # js.console.log(square.__str__())
        square.draw()
    p5js.requestAnimationFrame(create_proxy(draw))


setup()
js.window.requestAnimationFrame(create_proxy(draw))
