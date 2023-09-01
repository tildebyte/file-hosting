# 1. One hundred squares
# 2. Of randomly-selected size
# 3. Each having semi-tranparent fill and stroke
# 4. Each colored according to an underlying algorithm
# 5. Each rotating around its own center with a randomly-selected speed and
#    direction
# 6. Randomly distributed around the circumference of
# 7. One of several concentric circles
# 8. All squares orbiting at a randomly-selected speed and direction around
#    a common center point
#
# Updated implemention, using pyscript and three.js by Ben Alkov May 2022
# Initial implementation by Ben Alkov 20-27 November 2016.

# from flatten import (
#     Point,
#     Polygon,
#     Segment,
# )

import math

# Not strictly necessary, but seeing naked e.g. `document`, `window`, etc. really bothers me
import js

from pyodide import create_proxy

import utils

bjs = js.window.BABYLON

ORIGIN = bjs.Vector3.Zero()
_BASIC_MAT = None
_ENGINE = None
_SCENE = None
_NUM_RECTS = 100
_RECTS = []
_WIDTH = js.window.innerWidth


class Rect():
    RECT_MIN_SIZE = 1.5
    RECT_MAX_SIZE = 5.0
    ROTATION_LIMIT = 0.07
    ROTATION_TOLERANCE = 0.009
    ORBIT_LIMIT = 0.009
    ORBIT_TOLERANCE = 0.0002
    BLUE = bjs.Color3.new(21, 21, 235)
    DK_BLUE = bjs.Color3.new(10, 10, 115)
    GREEN = bjs.Color3.new(149, 194, 81)
    DK_GREEN = bjs.Color3.new(57, 74, 31)
    HALF_PI = math.pi / 2

    def __init__(self):
        self._size = utils.rand_float(Rect.RECT_MIN_SIZE, Rect.RECT_MAX_SIZE)
        self._position = Rect._position_on_orbit()
        self._angle = self._get_angle()
        self._z_rotation = utils.rand_float(0, math.tau)
        # [-0.19, 0.19] within 0.03 rad of 0.
        self._orbit_angular_speed = utils.avoid_zero(Rect.ROTATION_LIMIT,
                                                     Rect.ROTATION_TOLERANCE)
        # [-1.5, 1.5] within 0.3 rad of 0.
        self._object_angular_speed = utils.avoid_zero(Rect.ORBIT_LIMIT,
                                                      Rect.ORBIT_TOLERANCE)
        self._plane = bjs.MeshBuilder.CreatePlane('plane', size=self._size)
        self._plane.material = bjs.StandardMaterial.new('material')
        self._plane.material.diffuseColor = bjs.Color3.Red()
        # self._plane.enableEdgesRendering()
        # self._plane.edgesWidth = 5
        # self._plane.material.alpha = 0.1
        # edges_opacity = 1
        # self._plane.edgesColor = bjs.Color3.new(149, 194, 81)
        self._plane.position = self._position
        self._plane.rotation = bjs.Vector3.new(0, 0, self._z_rotation)
        # self.recolor()

    def _get_angle(self):
        return js.Math.atan2(self._position.y, self._position.x)

    def orbit(self):
        x_pos = self._position.x
        y_pos = self._position.y
        theta = math.radians(self._orbit_angular_speed)
        self._plane.position.x = x_pos * js.Math.cos(theta) + y_pos * js.Math.sin(theta)
        self._plane.position.y = y_pos * js.Math.cos(theta) - x_pos * js.Math.sin(theta)
        self._angle = self._get_angle()

    def rotate(self):
        self._z_rotation += self._object_angular_speed
        self._plane.rotation.z = self._z_rotation

    def recolor(self):
        angle = abs(self._angle)
        # Left half
        if angle >= Rect.HALF_PI:
            shade = utils.map_linear(angle, math.pi, Rect.HALF_PI, 0, 0.5)
            color = Rect.GREEN.clone()
            other_color = Rect.BLUE.clone()
            stroke_color = Rect.DK_GREEN.clone()
            other_stroke_color = Rect.DK_BLUE.clone()
        # Right half.
        else:
            shade = utils.map_linear(angle, 0, Rect.HALF_PI, 0, 0.5)
            color = Rect.BLUE.clone()
            other_color = Rect.GREEN.clone()
            stroke_color = Rect.DK_BLUE.clone()
            other_stroke_color = Rect.DK_GREEN.clone()
        new_color = bjs.Color3.Lerp(color, other_color,
                                    shade + utils.rand_float(-0.02, 0.02))
        self._plane.material.diffuseColor = new_color
        self._plane.edgesColor = bjs.Color3.Lerp(stroke_color, other_stroke_color,
                                                 shade + utils.rand_float(-0.02, 0.02))

    def _choose_orbit():
        # Randomly choose an orbit, based on a set of weights.
        chance = utils.rand_float(0.0, 1.0)
        if chance < 0.18:
            return 3
        elif chance < 0.50:
            return 6
        elif chance < 0.78:
            return 9
        elif chance < 1.0:
            return 12

        return 0

    def _position_on_orbit():
        # Generate a random position on the circumference of the orbit chosen for
        # this item.
        angle = utils.rand_float(0, math.tau)
        # Slightly offsets the position so we don't end up with the
        # visible rects orbiting on *exact* circles.
        radius = Rect._choose_orbit() + utils.rand_float(0, int(_WIDTH / 23))
        creation_x = js.Math.cos(angle) * radius
        creation_y = js.Math.sin(angle) * radius
        # Add a teensy z-offset to mitigate z-fighting
        creation_z = utils.rand_float(-0.01, 0.01)
        return bjs.Vector3.new(creation_x, creation_y, creation_z)


def _handle_render():
    #     def update():
    #         for this_rect in _RECTS:
    #             for other_rect in _RECTS:
    #                 if other_rect != this_rect:
    #                     connect(this_rect, other_rect)
    for rect in _RECTS:
        rect.rotate()
        rect.orbit()
        rect.recolor()
        # js.console.log(f'rect {rect._size} has material {rect._plane.material}')
    _SCENE.render()


def _handle_resize(*args):
    _ENGINE.resize()


def _setup():
    global _BASIC_MAT
    global _ENGINE
    global _RECTS
    global _SCENE

    canvas = js.document.getElementById('renderCanvas')
    _ENGINE = bjs.Engine.new(canvas, True, preserveDrawingBuffer=True, stencil=True)
    _SCENE = bjs.Scene.new(_ENGINE)
    _SCENE.ambientColor = bjs.Color3.White()
    _SCENE.diffuseColor = bjs.Color3.White()
    _SCENE.specularColor = bjs.Color3.White()
    camera = bjs.ArcRotateCamera.new('Camera', -js.Math.PI / 2, js.Math.PI / 2, 80, ORIGIN)
    camera.attachControl(canvas, True)
    light = bjs.HemisphericLight.new('light', bjs.Vector3.new(0.5, 0.5, -1))  # noqa
    _BASIC_MAT = bjs.StandardMaterial.new('_BASIC_MAT')

    plane = bjs.MeshBuilder.CreatePlane('plane', size=5)
    plane.position.x = 5
    plane.position.z = -10
    plane.material = bjs.StandardMaterial.new('material')
    plane.material.diffuseColor = bjs.Color3.Green()
    plane.enableEdgesRendering()
    plane.edgesWidth = 15
    # plane.material.alpha = 0.6
    # plane.edgesColor = bjs.Color3.Red()

    _RECTS = [Rect() for _ in range(_NUM_RECTS)]


pyscript_loader.close()

_setup()
js.window.addEventListener('resize', create_proxy(_handle_resize))
_ENGINE.runRenderLoop(create_proxy(_handle_render))
