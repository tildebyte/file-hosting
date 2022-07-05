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
# Port to transcrypt/pyp5js Ben Alkov 2022
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

NUM_SQUARES = 100
BLUE = None
DK_BLUE = None
GREEN = None
DK_GREEN = None
squares = None


class Square():
    # p5.js DEFAULT IS RADIANS!!
    ROTATION_LIMIT = 0.03
    ROTATION_TOLERANCE = 0.009
    ORBIT_LIMIT = 0.003
    ORBIT_TOLERANCE = 0.0001

    def __init__(self):
        self._orbit = self._chooseOrbit() + random(0, int(width / 23))
        self._orbit_angle = random(TAU)
        self._position = createVector(cos(self._orbit_angle) * self._orbit,
                                      sin(self._orbit_angle) * self._orbit)
        self._size = random(int(width / 30), int(width / 20))
        self._rot_angle = random(TAU)
        self._s_color = color(0)
        self._s_opac = map(self._size, width / 30, width / 20, 150, 200)
        self._f_color = None
        self._f_opac = map(self._size, width / 30, width / 20, 150, 200)
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
        value = random(-limit, limit)
        while -tolerance < value < tolerance:
            value = random(-limit, limit)
            continue
        return value

    def _chooseOrbit(self):
        '''
        Randomly choose an orbit, based on a set of weights.
        The returns can be adjusted to account for a larger / smaller sketch size.
        '''
        chance = random(0, 1)
        if chance < 0.18:
            return width / 8
        elif chance < 0.50:
            return width / 4
        elif chance < 0.78:
            return width / 2.46
        elif chance < 1.0:
            return width / 1.7777

    def _move(self):
        '''
        Generate a random position on the circumference of the orbit chosen for
        this item.
        '''
        x = self._position.x
        y = self._position.y
        self._position.x = x * cos(self._orbit_speed) + y * sin(self._orbit_speed)
        self._position.y = y * cos(self._orbit_speed) - x * sin(self._orbit_speed)
        self._orbit_angle = atan2(self._position.y, self._position.x)

    def _recolor(self):
        angle = abs(self._orbit_angle)
        half_pi = PI / 2
        # Left half
        if angle >= half_pi:
            shade = map(angle, PI, half_pi, 0, 0.5)
            this_fill_color = GREEN
            other_fill_color = BLUE
            this_stroke_color = DK_GREEN
            other_stroke_color = DK_BLUE
        # Right half
        else:
            shade = map(angle, 0, half_pi, 0, 0.5)
            this_fill_color = BLUE
            other_fill_color = GREEN
            this_stroke_color = DK_BLUE
            other_stroke_color = DK_GREEN
        self._f_color = lerpColor(this_fill_color, other_fill_color,
                                  shade + random(-0.02, 0.02))
        self._s_color = lerpColor(this_stroke_color, other_stroke_color,
                                  shade + random(-0.02, 0.02))

    def draw(self):
        self._move()
        self._recolor()
        self._s_color.setAlpha(self._s_opac)
        stroke(self._s_color)
        self._f_color.setAlpha(self._f_opac)
        fill(self._f_color)
        push()
        translate(self._position.x, self._position.y)
        self._rot_angle += self._rot_speed
        rotate(self._rot_angle)
        rect(0, 0, self._size, self._size)
        pop()

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


def setup():
    global squares
    global BLUE
    global DK_BLUE
    global GREEN
    global DK_GREEN
    frameRate(60)
    createCanvas(1280, 720, WEBGL)
    setAttributes('antialias', True)
    # strokeCap(SQUARE)  # Not available for WEBGL
    strokeWeight(2)
    rectMode(CENTER)
    background(color(70, 71, 76))
    BLUE = color(21, 21, 235)
    DK_BLUE = color(10, 10, 115)
    GREEN = color(149, 194, 81)
    DK_GREEN = color(57, 74, 31)
    squares = [Square() for _ in range(NUM_SQUARES)]


def draw():
    background(color(70, 71, 76))
    # Remove if using 2D renderer!
    # translate(-width / 2, -height / 2, 0)
    for square in squares:
        # print(square.__str__())
        square.draw()
