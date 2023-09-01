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
# 2022-08 Update for breaking changes in pyscript and three, finally get three
#     working properly as a module, fix jsdelivr URLs, pin versions for all the
#     things, Python types (woohoo) thanks to pyodide basing on 3.11+
#
# Updated implemention, using pyscript and three.js by Ben Alkov May 2022
# Port to three.js by Ben Alkov 2016-11-20 - 27 for Codevember:
# https://codepen.io/tildebyte/pen/LbqZMR
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

import math

from typing import Any

from pyodide import ffi
from js import document, window
from js.three import (
    Color,
    DoubleSide,
    EdgesGeometry,
    Euler,
    LineBasicMaterial,
    LineSegments,
    Mesh,
    MeshBasicMaterial,
    PerspectiveCamera,
    PlaneGeometry,
    Scene,
    Vector3,
    WebGLRenderer,
)

import utils

Color: ffi.JsProxy
DoubleSide: ffi.JsProxy
EdgesGeometry: ffi.JsProxy
Euler: ffi.JsProxy
LineBasicMaterial: ffi.JsProxy
LineSegments: ffi.JsProxy
Mesh: ffi.JsProxy
MeshBasicMaterial: ffi.JsProxy
PerspectiveCamera: ffi.JsProxy
PlaneGeometry: ffi.JsProxy
Scene: ffi.JsProxy
Vector3: ffi.JsProxy
WebGLRenderer: ffi.JsProxy


class Rect():
    # three.js length units are in meters
    RECT_MIN_SIZE = 0.75
    RECT_MAX_SIZE = 1.5

    def __init__(self) -> None:
        self._size: float = utils.rand_float(self.RECT_MIN_SIZE, self.RECT_MAX_SIZE)
        self._position: Vector3 = Rect._position_on_orbit()
        self._angle: float = self._get_angle()
        self._rotation: Euler = Euler.new(0, 0, utils.rand_float(0, math.tau))
        # [-0.19, 0.19] within 0.03 degree of 0.
        self._orbit_angular_speed: float = utils.avoid_zero(0.19, 0.03)
        # [-1.5, 1.5] within 0.3 degree of 0.
        self._object_angular_speed: float = utils.avoid_zero(1.25, 0.3)
        self._plane_geometry: PlaneGeometry = PlaneGeometry.new(self._size, self._size)
        self._outline_geometry: EdgesGeometry = EdgesGeometry.new(self._plane_geometry)
        self._plane_material: MeshBasicMaterial = MeshBasicMaterial.new(
            transparent=True,
            side=DoubleSide,
            opacity=0.35
        )
        self._outline_material: LineBasicMaterial = LineBasicMaterial.new(
            transparent=True,
            side=DoubleSide,
            opacity=0.65,
            linewidth=2
        )
        self._plane_mesh: Mesh = Mesh.new(self._plane_geometry, self._plane_material)
        self._outline_mesh: LineSegments = LineSegments.new(self._outline_geometry,
                                              self._outline_material)
        self._plane_mesh.position.copy(self._position)
        self._plane_mesh.rotation.copy(self._rotation)
        self._plane_mesh.add(self._outline_mesh)
        self.recolor()

    def get_mesh_object(self) -> Mesh:
        return self._plane_mesh

    def _get_angle(self) -> float:
        return math.atan2(self._position.y, self._position.x)

    def orbit(self) -> None:
        x_pos: float = self._position.x
        y_pos: float = self._position.y
        theta: float = math.radians(self._orbit_angular_speed)
        self._position.x = x_pos * math.cos(theta) + y_pos * math.sin(theta)
        self._position.y = y_pos * math.cos(theta) - x_pos * math.sin(theta)
        self._plane_mesh.position.copy(self._position)
        self._angle = self._get_angle()

    def rotate(self) -> None:
        self._rotation.z += math.radians(self._object_angular_speed)
        self._plane_mesh.rotation.z = self._rotation.z

    def recolor(self) -> None:
        blue: Color = Color.new(0x2525C4)
        green: Color = Color.new(0x7DB528)
        angle: float = abs(self._angle)
        half_pi: float = math.pi / 2
        # Left half
        if angle >= half_pi:
            shade: float = utils.map_linear(angle, math.pi, half_pi, 0, 0.5)
            color: Color = green.clone()
            other_color: Color = blue.clone()
        # Right half.
        else:
            shade = utils.map_linear(angle, 0, half_pi, 0, 0.5)
            color = blue.clone()
            other_color = green.clone()
        self._plane_material.color = color.clone()
        self._plane_material.color.lerp(other_color,
                                        shade + utils.rand_float(-0.02, 0.02))
        self._outline_material.color = self._plane_material.color

    @staticmethod
    def _choose_orbit() -> float:
        # Randomly choose an orbit, based on a set of weights.
        chance: float = utils.rand_float(0.0, 1.0)
        if chance < 0.18:
            return 3
        if chance < 0.50:
            return 6
        if chance < 0.78:
            return 9
        if chance < 1.0:
            return 12

        return 0

    @staticmethod
    def _position_on_orbit() -> Vector3:
        # Generate a random position on the circumference of the orbit chosen for
        # this item.
        angle: float = utils.rand_float(0, math.tau)
        # Slightly offsets the position so we don't end up with the
        # visible rects orbiting on *exact* circles.
        radius: float = Rect._choose_orbit() + utils.rand_float(0, 3)
        creation_x: float = math.cos(angle) * radius
        creation_y: float = math.sin(angle) * radius
        # Add a teensy z-offset to mitigate z-fighting
        creation_z: float = utils.rand_float(-0.01, 0.01)
        return Vector3.new(creation_x, creation_y, creation_z)


_HEIGHT: int = window.innerHeight
_WIDTH: int = window.innerWidth

_CAMERA: PerspectiveCamera = None
_RENDERER: WebGLRenderer = None
_SCENE: Scene = None

_RECTS: list[Rect] = []


def _handle_resize(event: Any) -> None:
    _CAMERA.aspect = window.innerWidth / window.innerHeight
    _CAMERA.updateProjectionMatrix()
    _RENDERER.setSize(window.innerWidth, window.innerHeight)
    _RENDERER.setPixelRatio(window.devicePixelRatio)


def _init() -> None:
    global _SCENE
    global _CAMERA
    global _RENDERER

    _SCENE = Scene.new()
    _CAMERA = PerspectiveCamera.new(
        50,  # F.O.V.
        _WIDTH / _HEIGHT,  # Aspect.
        19,  # Near clip.
        21  # Far clip.
    )
    _CAMERA.lookAt(Vector3.new(0, 0, 0))
    _CAMERA.updateProjectionMatrix()
    _RENDERER = utils.renderer_config(WebGLRenderer, _WIDTH, _HEIGHT, 0x46474c)  # Middle grey


def _setup() -> None:
    global _RECTS

    num_rects = 100

    _CAMERA.setFocalLength = 70
    _CAMERA.position.z = 20
    _CAMERA.updateProjectionMatrix()
    _RECTS = [Rect() for _ in range(num_rects)]
    for rect in _RECTS:
        _SCENE.add(rect.get_mesh_object())
    window.addEventListener('resize', ffi.create_proxy(_handle_resize))
    document.body.appendChild(_RENDERER.domElement)
    _RENDERER.setAnimationLoop(ffi.create_proxy(_animate))
    _RENDERER.render(_SCENE, _CAMERA)


def _animate(*args: dict[str, Any]) -> None:
    for rect in _RECTS:
        rect.rotate()
        rect.orbit()
        rect.recolor()
    _RENDERER.render(_SCENE, _CAMERA)

_init()
_setup()
_animate()
