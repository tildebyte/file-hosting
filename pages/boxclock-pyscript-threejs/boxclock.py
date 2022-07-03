# A wireframe box with colored edges which expands and contracts according
# to time-of-day.
# Inspired by *hms* from https://www.gysin-vanetti.com/hms
#
# Ported to pyscript/three.js by Ben Alkov 2022-06
# Initial implementation by Ben Alkov 2016

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

# Not strictly necessary, but seeing naked e.g. `document`, `window`, etc. really bothers me
import js
from pyodide import create_proxy
from three import (
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

_WIDTH = js.window.innerWidth
_HEIGHT = js.window.innerHeight

_RED = Color.new(0xad002b)
_GREEN = Color.new(0x4dba00)
_BLUE = Color.new(0x061982)
_BACKGROUND = Color.new(0x191919)

_BOX = None
_CAMERA = None
_RENDERER = None
_SCENE = None

_DATA = {
    # Seconds - lines along `x`
    'seconds': {
        'verts': js.Float32Array.new([
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
        'verts': js.Float32Array.new([
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
        'verts': js.Float32Array.new([
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


class Edges():
    def __init__(self, record):
        geometry = BufferGeometry.new()
        verts = record['verts']
        geometry.setAttribute('position', BufferAttribute.new(verts, 3))
        material = LineBasicMaterial.new(color=record['color'])
        self._lines_mesh = LineSegments.new(geometry, material)

    def get_mesh_object(self):
        return self._lines_mesh


def _handle_resize(event):
    _CAMERA.aspect = js.window.innerWidth / js.window.innerHeight
    _CAMERA.updateProjectionMatrix()
    _RENDERER.setSize(js.window.innerWidth, js.window.innerHeight)
    _RENDERER.setPixelRatio(js.window.devicePixelRatio)


def _init():
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


def _setup():
    global _BOX

    # Draw a 2x2x2 cube with edges colored according to the
    # current time.
    # Seconds - lines along local `x`: Red
    # Minutes - lines along local `y`: Green
    # Hours - lines along local `z`: Blue
    # Scale down a teensy bit to prevent edge/face "fighting"
    geometry = BoxGeometry.new(1.999, 1.999, 1.999)
    material = MeshLambertMaterial.new(
        transparent=True,
        opacity=0)
    _CAMERA.position.z = 50
    _BOX = Mesh.new(geometry, material)
    for _, record in _DATA.items():
        edge = Edges(record).get_mesh_object()
        _BOX.add(edge)
    _SCENE.add(_BOX)
    js.window.addEventListener('resize', create_proxy(_handle_resize))
    js.document.body.appendChild(_RENDERER.domElement)
    _RENDERER.setAnimationLoop(create_proxy(_animate))
    _RENDERER.render(_SCENE, _CAMERA)


def _animate(*args):
    tick = 0.0008
    date = dt.datetime.now()
    seconds = utils.map_linear(date.second, 0, 59, 1, 12)
    minutes = utils.map_linear(date.minute, 0, 59, 1, 12)
    hours = utils.map_linear(date.hour, 0, 23, 1, 12)

    _BOX.rotation.x += tick
    _BOX.rotation.y += tick
    _BOX.rotation.z += tick
    _BOX.scale.x = seconds
    _BOX.scale.y = minutes
    _BOX.scale.z = hours
    _RENDERER.render(_SCENE, _CAMERA)


pyscript_loader.close()

_init()
_setup()
_animate()
