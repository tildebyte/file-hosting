'''A sketch inspired by (a radical misinterpretation of) the math from the
JS1K segment of Steven Wittens' "Making Things With Maths" video. Really,
everything is mine except the math in `segment.py`. See also
http://acko.net/blog/js1k-demo-the-making-of

Updates for Processing.py 0405/Processing 3.0a by Ben Alkov 2015-02-12.
Implemented in Processing.py/Processing 2.1 by Ben Alkov 2014-09-11 - 16.

Copyright 2014, 2015, 2022 by Ben Alkov
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''
import math

# Not strictly necessary, but seeing naked e.g. `document`, `window`, etc. really bothers me
import js

from pyodide import create_proxy

from tentacle import Tentacle

p5js = js.window

TIME = 0
Tick = 1 / 500  # Guarantee floating point.
SphereRadius = 400
Colors = [
    [
        js.window.color(169, 202, 240),  # blues
        p5js.color(160, 191, 227),
        p5js.color(142, 170, 202),
        p5js.color(115, 137, 163),
        p5js.color(70, 84, 99)
    ],
    [
        p5js.color(206, 151, 96),  # reds
        p5js.color(207, 105, 43),
        p5js.color(193, 87, 37),
        p5js.color(124, 40, 12),
        p5js.color(120, 41, 13)
    ],
    [
        p5js.color(115, 146, 34),  # greens
        p5js.color(104, 135, 23),
        p5js.color(92, 109, 29),
        p5js.color(78, 93, 22),
        p5js.color(63, 76, 16)
    ]
]
Tentacles = [Tentacle(i * -100, Colors[i % 3]) for i in range(6)]


def rightHanded():
    # Fix flippin' coordinate system.
    # Not the *same* as right-handed, but good enough.
    # `-z` comes out of the screen.
    p5js.rotateX(math.tau / 2)  # `Y` up.
    # p5js.translate(256, -256, 0)  # Centered.


def fade():
    # Encapsulate alpha blend for trails.
    p5js.push()
    p5js.fill('rgba(0, 0, 0)')
    p5js.noStroke()
    p5js.translate(0, 0, -SphereRadius)
    p5js.rect(0, 0, p5js.windowWidth, p5js.windowHeight)
    p5js.pop()


def setup():
    p5js.frameRate(60)
    renderer = p5js.createCanvas(p5js.windowWidth, p5js.windowHeight, p5js.WEBGL)
    renderer.style('display', 'block')
    p5js.rectMode(p5js.RADIUS)
    p5js.ellipseMode(p5js.RADIUS)
    p5js.strokeWeight(2)


def draw(*args):
    global TIME

    rightHanded()
    p5js.clear()
    fade()
    TIME += Tick
    # We should be using the timestamp from *args here
    for t in Tentacles:
        t.update(TIME, Tick, SphereRadius)

    p5js.requestAnimationFrame(create_proxy(draw))


setup()
js.window.requestAnimationFrame(create_proxy(draw))
