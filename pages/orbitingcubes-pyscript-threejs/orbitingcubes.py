# 1. One hundred cubes
# 2. Of randomly-selected size
# 3. Each having semi-transparent fill and stroke
# 4. Each colored according to an underlying algorithm
# 5. Each rotating around its own center with a randomly-selected speed and
#    direction
# 6. Randomly distributed around the circumference of
# 7. One of several concentric circles
# 8. All cubes rotating at a randomly-selected speed and direction around
#    a common center point
#
# 2022-08 Update for breaking changes in pyscript and three, finally get three
#     working properly as a module, fix jsdelivr URLs, pin versions for all the
#     things, Python types (woohoo) thanks to pyodide basing on 3.11+
#
# Ported to pyscript/js by Ben Alkov 2022-05
# Initial implementation by Ben Alkov 2016-12 for #3December:
# https://codepen.io/tildebyte/pen/VmgBXj

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

from typing import Any, Tuple, Literal

from pyodide import ffi
from js import document, window
from js.three import (
    AmbientLight,
    BoxGeometry,
    Color,
    DirectionalLight,
    DoubleSide,
    EdgesGeometry,
    Euler,
    LineBasicMaterial,
    LineSegments,
    Mesh,
    MeshLambertMaterial,
    Object3D,
    PerspectiveCamera,
    Scene,
    Vector3,
    WebGLRenderer,
)

import utils

AmbientLight: ffi.JsProxy
BoxGeometry: ffi.JsProxy
Color: ffi.JsProxy
DirectionalLight: ffi.JsProxy
DoubleSide: ffi.JsProxy
EdgesGeometry: ffi.JsProxy
Euler: ffi.JsProxy
LineBasicMaterial: ffi.JsProxy
LineSegments: ffi.JsProxy
Mesh: ffi.JsProxy
MeshLambertMaterial: ffi.JsProxy
Object3D: ffi.JsProxy
PerspectiveCamera: ffi.JsProxy
Scene: ffi.JsProxy
Vector3: ffi.JsProxy
WebGLRenderer: ffi.JsProxy


class Cube():
    # js length units are in meters
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
    CUBE_MAX_EXTENT: float = math.sqrt(3) * CUBE_MAX_SIZE

    # First orbit is a little larger than the diagonal extent of the largest cube
    FIRST_ORBIT: float = CUBE_MAX_EXTENT + (CUBE_MAX_SIZE * 0.5)
    ORBITS: tuple[float, float, float, float] = (
        FIRST_ORBIT, FIRST_ORBIT * 2,
        FIRST_ORBIT * 3, FIRST_ORBIT * 4
    )

    def __init__(self) -> None:
        self._position: Vector3 = None
        self._radius: float = 0.0
        self._size: float = utils.rand_float(self.CUBE_MIN_SIZE, self.CUBE_MAX_SIZE)
        self._position, self._radius = Cube._position_on_orbit()
        self._angle: float = self._update_angle()
        self._rotation: Euler = Euler.new(0.0, 0.0, utils.rand_float(0.0, math.tau))
        self._orbit_angular_speed: float = utils.avoid_zero(self.ORBIT_SPEED_LIMIT,
                                                            self.ORBIT_SPEED_TOLERANCE)
        self._object_angular_speed: float = utils.avoid_zero(self.SELF_ROT_SPEED_LIMIT,
                                                             self.SELF_ROT_TOLERANCE)
        self._cube_geometry: BoxGeometry = BoxGeometry.new(self._size, self._size, self._size)
        self._outline_geometry: EdgesGeometry = EdgesGeometry.new(self._cube_geometry)
        alpha: float = utils.map_linear(self._radius, self.ORBITS[1] - 2, self.ORBITS[3], 1.0, 0.5)
        self._cube_material: MeshLambertMaterial = MeshLambertMaterial.new(
            transparent=True,
            side=DoubleSide,
            opacity=alpha)
        self._outline_material: LineBasicMaterial = LineBasicMaterial.new(
            transparent=True,
            side=DoubleSide,
            opacity=alpha)
        self._outline_mesh: LineSegments = LineSegments.new(self._outline_geometry,
                                              self._outline_material)
        self._cube_mesh: Mesh = Mesh.new(self._cube_geometry, self._cube_material)
        self._cube_mesh.position.copy(self._position)
        self._cube_mesh.rotation.copy(self._rotation)
        self._cube_mesh.add(self._outline_mesh)
        self.recolor()

    def _update_angle(self) -> float:
        return math.atan2(self._position.y, self._position.x)

    def get_mesh_object(self) -> Mesh:
        return self._cube_mesh

    def orbit(self) -> None:
        x_pos: float = self._position.x
        y_pos: float = self._position.y
        theta: float = math.radians(self._orbit_angular_speed)
        self._position.x = x_pos * math.cos(theta) + y_pos * math.sin(theta)
        self._position.y = y_pos * math.cos(theta) - x_pos * math.sin(theta)
        self._cube_mesh.position.copy(self._position)
        self._angle = self._update_angle()

    def rotate(self) -> None:
        self._rotation.x += math.radians(self._object_angular_speed)
        self._rotation.y += math.radians(self._object_angular_speed)
        self._rotation.z += math.radians(self._object_angular_speed)
        self._cube_mesh.rotation.x = self._rotation.x
        self._cube_mesh.rotation.y = self._rotation.y
        self._cube_mesh.rotation.z = self._rotation.z

    def recolor(self) -> None:
        blue: Color = Color.new(0x1515eb)
        dk_blue: Color = Color.new(0x0a0a73)
        green: Color = Color.new(0x95c251)
        dk_green: Color = Color.new(0x394a1f)
        angle: float = abs(self._angle)
        half_pi: float = math.pi / 2
        # Left half
        if angle >= half_pi:
            shade: float = utils.map_linear(angle, math.pi, half_pi, 0, 0.5)
            color: Color = green.clone()
            other_color: Color = blue.clone()
            outline_color: Color = dk_green.clone()
            other_outline_color: Color = dk_blue.clone()
        # Right half.
        else:
            shade = utils.map_linear(angle, 0, half_pi, 0, 0.5)
            color = blue.clone()
            other_color = green.clone()
            outline_color = dk_blue.clone()
            other_outline_color = dk_green.clone()

        self._cube_material.color = color.clone()
        self._cube_material.color.lerp(
            other_color.clone(),
            # avoid obvious color bands
            shade + utils.rand_float(-0.02, 0.02))
        self._outline_material.color = outline_color.clone()
        self._outline_material.color.lerp(
            other_outline_color.clone(),
            # avoid obvious color bands
            shade + utils.rand_float(-0.02, 0.02))

    @staticmethod
    def _choose_orbit() -> float:
        # Randomly choose an orbit, based on a set of probabilities.
        # The probabilities favor larger orbits, as they have room for more cubes.
        chance: float = utils.rand_float(0.0, 1.0)
        if chance < 0.16:
            return Cube.ORBITS[0]
        if chance < 0.40:
            return Cube.ORBITS[1]
        if chance < 0.72:
            return Cube.ORBITS[2]
        if chance < 1.0:
            return Cube.ORBITS[3]

        return 0

    @staticmethod
    def _position_on_orbit() -> Tuple[Vector3, float]:
        # Generate a random position on the circumference of the orbit chosen for
        # this item.
        angle: float = utils.rand_float(0.0, math.tau)
        orbit: float = Cube._choose_orbit()

        # Randomly offset the position on the orbit, so we don't end up with multiple
        # cubes orbiting on *exactly* the same circles.
        radius: float = orbit + utils.rand_float(0.0, Cube.ORBITS[0])
        creation_x: float = math.cos(angle) * radius
        creation_y: float = math.sin(angle) * radius
        position: Vector3 = Vector3.new(creation_x, creation_y, 0)
        return (position, radius)


_WIDTH: int = window.innerWidth
_HEIGHT: int = window.innerHeight

_AMB_LIGHT: AmbientLight = None
_CAMERA: PerspectiveCamera = None
_CLICKED: int = 0
_LIGHT: DirectionalLight = None
_RENDERER: WebGLRenderer = None
_SCENE: Scene = None
_SCREEN_ORIENTATION: Literal['portrait', 'landscape'] = utils.screen_orientation()
_CUBES: list[Cube] = []


def _handle_resize(event: Any) -> None:
    _CAMERA.aspect = window.innerWidth / window.innerHeight
    _CAMERA.updateProjectionMatrix()
    _RENDERER.setSize(window.innerWidth, window.innerHeight)
    _RENDERER.setPixelRatio(window.devicePixelRatio)


def _handle_rotate(event) -> None:
    global _SCREEN_ORIENTATION
    current_orientation: Literal['portrait', 'landscape'] = utils.screen_orientation()
    if current_orientation is not _SCREEN_ORIENTATION:
        _SCREEN_ORIENTATION = current_orientation
        _RENDERER.render(_SCENE, _CAMERA)


def _handle_click(event: Any) -> None:
    global _CLICKED
    if _CLICKED == 0:
        _CAMERA.near = 31.9
        _CAMERA.far = 32.1
        _CAMERA.updateProjectionMatrix()
    if _CLICKED == 1:
        _CAMERA.position.y = -20
        _CAMERA.position.z = 20
        _CAMERA.near = 15
        _CAMERA.far = 150
        _CAMERA.lookAt(Vector3.new(0, 0, 0))
        _CAMERA.updateProjectionMatrix()
    if _CLICKED == 2:
        _CAMERA.position.y = -1
        _CAMERA.position.z = 32
        _CAMERA.lookAt(Vector3.new(0, 0, 0))
        _CAMERA.updateProjectionMatrix()
    _CLICKED = _CLICKED + 1 if _CLICKED < 2 else 0


def _init() -> None:
    global _SCENE
    global _AMB_LIGHT
    global _LIGHT
    global _CAMERA
    global _RENDERER

    _SCENE = Scene.new()

    # I can't find another way to do this...
    Object3D.DEFAULT_UP = Vector3.new(0, 0, 1)
    _LIGHT = DirectionalLight.new()
    Object3D.DEFAULT_UP = Vector3.new(0, 1, 0)
    _AMB_LIGHT = AmbientLight.new()
    _CAMERA = PerspectiveCamera.new(
        50,  # F.O.V.
        _WIDTH / _HEIGHT,  # Aspect
        30,  # Near clip
        34  # Far clip
    )
    _RENDERER = utils.renderer_config(WebGLRenderer, _WIDTH, _HEIGHT, 0x46474c)  # Middle grey


def _setup() -> None:
    global _CUBES

    num_cubes = 100

    _CAMERA.setFocalLength = 70
    _CAMERA.position.z = 32
    _CAMERA.lookAt(Vector3.new(0, 0, 0))
    _CAMERA.updateProjectionMatrix()
    _AMB_LIGHT.color = Color.new(0xb3a297)  # amber
    _AMB_LIGHT.intensity = 0.6
    _SCENE.add(_LIGHT)
    _SCENE.add(_AMB_LIGHT)
    _CUBES = [Cube() for _ in range(num_cubes)]
    for cube in _CUBES:
        _SCENE.add(cube.get_mesh_object())
    window.addEventListener('click', ffi.create_proxy(_handle_click))
    window.addEventListener('resize', ffi.create_proxy(_handle_resize))
    window.addEventListener('rotate', ffi.create_proxy(_handle_rotate))
    document.body.appendChild(_RENDERER.domElement)
    _RENDERER.setAnimationLoop(ffi.create_proxy(_animate))
    _RENDERER.render(_SCENE, _CAMERA)


def _animate(*args: dict[str, Any]) -> None:
    for cube in _CUBES:
        cube.rotate()
        cube.orbit()
        cube.recolor()
    _RENDERER.render(_SCENE, _CAMERA)

_init()
_setup()
_animate()
