# A wireframe box with colored edges which expands and contracts according
# to time-of-day.
# Inspired by *hms* from https://www.gysin-vanetti.com/hms
#
# Ported to pyscript/three.js by Ben Alkov 2022-06
# Initial Processing.py implementation by Ben Alkov 2015-02:
# https://github.com/jdf/processing.py/tree/master/mode/examples/Demos/Graphics/BoxClock
#
# 2022-08 Update for breaking changes in pyscript and three, finally get three
#     working properly as a module, fix jsdelivr URLs, pin versions for all the
#     things, Python types (woohoo) thanks to pyodide basing on 3.11+

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

import datetime as dt

from typing import Any

from pyodide import ffi

from js import document, Float32Array, window
from js.three import (
    BoxGeometry,
    BufferAttribute,
    BufferGeometry,
    Color,
    LineBasicMaterial,
    LineSegments,
    Mesh,
    MeshLambertMaterial,
    PerspectiveCamera,
    Scene,
    WebGLRenderer,
)

import utils

BoxGeometry: ffi.JsProxy
BufferAttribute: ffi.JsProxy
BufferGeometry: ffi.JsProxy
Color: ffi.JsProxy
LineBasicMaterial: ffi.JsProxy
LineSegments: ffi.JsProxy
Mesh: ffi.JsProxy
MeshLambertMaterial: ffi.JsProxy
PerspectiveCamera: ffi.JsProxy
Scene: ffi.JsProxy
WebGLRenderer: ffi.JsProxy
Float32Array: ffi.JsProxy
js: ffi.JsProxy


class Edges():
    def __init__(self, record: dict[str, ffi.JsProxy]) -> None:
        geometry: BufferGeometry = BufferGeometry.new()
        verts: Float32Array = record['verts']
        geometry.setAttribute('position', BufferAttribute.new(verts, 3))
        material: LineBasicMaterial = LineBasicMaterial.new(color=record['color'])
        self._lines_mesh: LineSegments = LineSegments.new(geometry, material)

    def get_mesh_object(self) -> LineSegments:
        return self._lines_mesh


def _handle_resize(event: Any) -> None:
    _CAMERA.aspect = window.innerWidth / window.innerHeight
    _CAMERA.updateProjectionMatrix()
    _RENDERER.setSize(window.innerWidth, window.innerHeight)
    _RENDERER.setPixelRatio(window.devicePixelRatio)


_WIDTH: int = window.innerWidth
_HEIGHT: int = window.innerHeight

_RED: Color = Color.new(0xad002b)
_GREEN: Color = Color.new(0x4dba00)
_BLUE: Color = Color.new(0x061982)
_BACKGROUND: Color = Color.new(0x191919)

_BOX: Mesh = None
_CAMERA: PerspectiveCamera = None
_RENDERER: WebGLRenderer = None
_SCENE: Scene = None

_DATA: dict[str, dict[str, ffi.JsProxy]] = {
    # Seconds - lines along `x`
    'seconds': {
        'verts': Float32Array.new([
                    -1.0, 1.0, 1.0,
                    1.0, 1.0, 1.0,
                    -1.0, -1.0, 1.0,
                    1.0, -1.0, 1.0,
                    -1.0, -1.0, -1.0,
                    1.0, -1.0, -1.0,
                    -1.0, 1.0, -1.0,
                    1.0, 1.0, -1.0
                  ]),
        'color': _RED
    },
    # Minutes - lines along `y`
    'minutes': {
        'verts': Float32Array.new([
                    -1.0, 1.0, 1.0,
                    -1.0, -1.0, 1.0,
                    1.0, 1.0, 1.0,
                    1.0, -1.0, 1.0,
                    1.0, 1.0, -1.0,
                    1.0, -1.0, -1.0,
                    -1.0, 1.0, -1.0,
                    -1.0, -1.0, -1.0
                  ]),
        'color': _GREEN
    },
    # Hours - lines along `z`
    'hours': {
        'verts': Float32Array.new([
                    -1.0, 1.0, -1.0,
                    -1.0, 1.0, 1.0,
                    1.0, 1.0, -1.0,
                    1.0, 1.0, 1.0,
                    1.0, -1.0, -1.0,
                    1.0, -1.0, 1.0,
                    -1.0, -1.0, -1.0,
                    -1.0, -1.0, 1.0
                ]),
        'color': _BLUE
    }
}


def _init() -> None:
    global _SCENE
    global _CAMERA
    global _RENDERER

    _SCENE = Scene.new()
    _CAMERA = PerspectiveCamera.new(
        50,  # F.O.V.
        _WIDTH / _HEIGHT,  # Aspect.
        0.1,  # Near clip.
        10000  # Far clip.
    )
    _RENDERER = utils.renderer_config(WebGLRenderer, _WIDTH, _HEIGHT, _BACKGROUND)


def _setup() -> None:
    global _BOX

    # Draw a 2x2x2 cube with edges colored according to the
    # current time.
    # Seconds - lines along local `x`: Red
    # Minutes - lines along local `y`: Green
    # Hours - lines along local `z`: Blue
    # Scale down a teensy bit to prevent edge/face "fighting"
    geometry: BoxGeometry = BoxGeometry.new(1.999, 1.999, 1.999)
    material: MeshLambertMaterial = MeshLambertMaterial.new(
        transparent=True,
        opacity=0)
    _CAMERA.position.z = 50
    _BOX = Mesh.new(geometry, material)
    for _, record in _DATA.items():
        edge: Edges = Edges(record).get_mesh_object()
        _BOX.add(edge)
    _SCENE.add(_BOX)
    window.addEventListener('resize', ffi.create_proxy(_handle_resize))
    document.body.appendChild(_RENDERER.domElement)
    _RENDERER.setAnimationLoop(ffi.create_proxy(_animate))
    _RENDERER.render(_SCENE, _CAMERA)


def _animate(*args: dict[str, Any]) -> None:
    tick = 0.0008
    date: dt.datetime = dt.datetime.now()
    seconds: int = int(utils.map_linear(date.second, 0, 59, 1, 12))
    minutes: int = int(utils.map_linear(date.minute, 0, 59, 1, 12))
    hours: int = int(utils.map_linear(date.hour, 0, 23, 1, 12))

    _BOX.rotation.x += tick
    _BOX.rotation.y += tick
    _BOX.rotation.z += tick
    _BOX.scale.x = seconds
    _BOX.scale.y = minutes
    _BOX.scale.z = hours
    _RENDERER.render(_SCENE, _CAMERA)

_init()
_setup()
_animate()
