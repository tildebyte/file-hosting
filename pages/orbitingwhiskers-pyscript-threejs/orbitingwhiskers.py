# 1. One hundred lines
# 2. Of randomly-selected size
# 3. Each having semi-tranparent fill and stroke
# 4. Each colored according to an underlying algorithm
# 5. Each rotating around its own center with a randomly-selected speed and
#    direction
# 6. Randomly distributed around the circumference of
# 7. One of several concentric circles
# 8. All lines rotating at a randomly-selected speed and direction around
#    a common center point
#
# Implementation by Ben Alkov May 2022, base on my OrbitingCubes.py

import math

# Not strictly necessary, but seeing naked e.g. `document`, `window`, etc. really bothers me
import js
from pyodide import create_proxy
from three import (
    BufferAttribute,
    BufferGeometry,
    Color,
    DirectionalLight,
    Euler,
    Group,
    LineBasicMaterial,
    LineSegments,
    Object3D,
    PerspectiveCamera,
    Scene,
    Vector3,
    WebGLRenderer,
)

import utils

_CAMERA = None
_CLICKED = 0
_HEIGHT = js.window.innerHeight
_RENDERER = None
_SCENE = None
_WIDTH = js.window.innerWidth

_WHISKERS = None


class Whisker():
    # three.js length units are in meters
    CUBE_MIN_SIZE = 1.25
    CUBE_MAX_SIZE = 2.0

    # ORBIT_SPEED and SELF_ROT are degrees/frame
    # [-0.13, 0.13] within 0.01 degree of 0
    ORBIT_SPEED_LIMIT = 0.13
    ORBIT_SPEED_TOLERANCE = 0.01

    # [-1.3, 1.3] within 0.5 degree of 0
    SELF_ROT_SPEED_LIMIT = 1.3
    SELF_ROT_TOLERANCE = 0.5

    # Pythagoras in 3D
    CUBE_MAX_EXTENT = math.sqrt(3) * CUBE_MAX_SIZE

    # First orbit is a little larger than the diagonal extent of the largest cube
    FIRST_ORBIT = CUBE_MAX_EXTENT + (CUBE_MAX_SIZE * 0.5)
    ORBITS = (FIRST_ORBIT, FIRST_ORBIT * 2,
              FIRST_ORBIT * 3, FIRST_ORBIT * 4)

    def __init__(self):
        self._size = utils.rand_float(self.CUBE_MIN_SIZE, self.CUBE_MAX_SIZE)
        self._position, self._radius = Whisker._position_on_orbit()
        self._angle = self._update_angle()
        self._rotation = Euler.new(0.0, 0.0, utils.rand_float(0.0, math.tau))
        self._orbit_angular_speed = utils.avoid_zero(self.ORBIT_SPEED_LIMIT,
                                                     self.ORBIT_SPEED_TOLERANCE)
        self._object_angular_speed = utils.avoid_zero(self.SELF_ROT_SPEED_LIMIT,
                                                      self.SELF_ROT_TOLERANCE)
        self._group = Group.new()
        self._whisker = BufferGeometry.new()
        verts = js.Float32Array.new([
            0, 0, 0,
            self._size, 0, 0
            ])
        self._whisker.setAttribute('position', BufferAttribute.new(verts, 3))
        self._whisker_mat = LineBasicMaterial.new()
        self._whisker_mesh = LineSegments.new(self._whisker, self._whisker_mat)
        self._group.add(self._whisker_mesh)
        self._group.position.copy(self._position)
        self._group.rotation.copy(self._rotation)
        self.recolor()

    def _update_angle(self):
        return math.atan2(self._position.y, self._position.x)

    def get_group_object(self):
        return self._group

    def orbit(self):
        x_pos = self._position.x
        y_pos = self._position.y
        theta = math.radians(self._orbit_angular_speed)
        self._position.x = x_pos * math.cos(theta) + y_pos * math.sin(theta)
        self._position.y = y_pos * math.cos(theta) - x_pos * math.sin(theta)
        self._group.position.copy(self._position)
        self._angle = self._update_angle()

    def rotate(self):
        self._rotation.x += math.radians(self._object_angular_speed)
        self._rotation.y += math.radians(self._object_angular_speed)
        self._rotation.z += math.radians(self._object_angular_speed)
        self._group.rotation.x = self._rotation.x
        self._group.rotation.y = self._rotation.y
        self._group.rotation.z = self._rotation.z

    def recolor(self):
        blue = Color.new(0x245fff)
        green = Color.new(0x77b90f)
        angle = abs(self._angle)
        half_pi = math.pi / 2
        # Left half
        if angle >= half_pi:
            shade = utils.map_linear(angle, math.pi, half_pi, 0, 0.5)
            outline_color = green.clone()
            other_outline_color = blue.clone()
        # Right half.
        else:
            shade = utils.map_linear(angle, 0, half_pi, 0, 0.5)
            outline_color = blue.clone()
            other_outline_color = green.clone()

        self._whisker_mat.color = outline_color.clone()
        self._whisker_mat.color.lerp(
            other_outline_color.clone(),
            # avoid obvious color bands
            shade + utils.rand_float(-0.02, 0.02))

    def _choose_orbit():
        # Randomly choose an orbit, based on a set of probabilities.
        # The probabilities favor larger orbits, as they have room for more whiskers.
        chance = utils.rand_float(0.0, 1.0)
        if chance < 0.16:
            return Whisker.ORBITS[0]
        if chance < 0.40:
            return Whisker.ORBITS[1]
        if chance < 0.72:
            return Whisker.ORBITS[2]
        if chance < 1.0:
            return Whisker.ORBITS[3]

        return 0

    def _position_on_orbit():
        # Generate a random position on the circumference of the orbit chosen for
        # this item.
        angle = utils.rand_float(0.0, math.tau)
        orbit = Whisker._choose_orbit()

        # Randomly offset the position on the orbit, so we don't end up with multiple
        # cubes orbiting on *exactly* the same circles.
        radius = orbit + utils.rand_float(0.0, Whisker.ORBITS[0])
        creation_x = math.cos(angle) * radius
        creation_y = math.sin(angle) * radius
        position = Vector3.new(creation_x, creation_y, 0)
        return [position, radius]


def _handle_resize(event):
    _CAMERA.aspect = js.window.innerWidth / js.window.innerHeight
    _CAMERA.updateProjectionMatrix()
    _RENDERER.setSize(js.window.innerWidth, js.window.innerHeight)
    _RENDERER.setPixelRatio(js.window.devicePixelRatio)


def _handle_click(event):
    global _CLICKED
    if _CLICKED == 0:
        _CAMERA.near = 31.9
        _CAMERA.far = 32.1
        _CAMERA.updateProjectionMatrix()
    if _CLICKED == 1:
        _CAMERA.near = 15
        _CAMERA.far = 150
        _CAMERA.updateProjectionMatrix()
    _CLICKED = _CLICKED + 1 if _CLICKED < 1 else 0


def _init():
    global _SCENE
    global _CAMERA
    global _RENDERER

    _SCENE = Scene.new()
    _CAMERA = PerspectiveCamera.new(
        50,  # F.O.V.
        _WIDTH / _HEIGHT,  # Aspect
        30,  # Near clip
        34  # Far clip
    )
    _CAMERA.lookAt(Vector3.new(0, 0, 0))
    _CAMERA.updateProjectionMatrix()
    _RENDERER = utils.renderer_config(WebGLRenderer, _WIDTH, _HEIGHT,
                                      Color.new(0x3e3e3e))  # Dark-ish grey


def _setup():
    global _WHISKERS

    num_whiskers = 100

    _CAMERA.setFocalLength = 70
    _CAMERA.position.x = 0
    _CAMERA.position.y = 0
    _CAMERA.position.z = 32
    _CAMERA.updateProjectionMatrix()
    _WHISKERS = [Whisker() for _ in range(num_whiskers)]
    for whiskers in _WHISKERS:
        _SCENE.add(whiskers.get_group_object())
    js.window.addEventListener('click', create_proxy(_handle_click))
    js.window.addEventListener('resize', create_proxy(_handle_resize))
    js.document.body.appendChild(_RENDERER.domElement)
    _RENDERER.setAnimationLoop(create_proxy(_animate))
    _RENDERER.render(_SCENE, _CAMERA)


def _animate(*args):
    for whiskers in _WHISKERS:
        whiskers.rotate()
        whiskers.orbit()
        whiskers.recolor()
    _RENDERER.render(_SCENE, _CAMERA)


pyscript_loader.close()

_init()
_setup()
_animate()
