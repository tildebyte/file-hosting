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

import math

# Not strictly necessary, but seeing naked e.g. `document`, `window`, etc. really bothers me
import js
from pyodide import create_proxy
from three import (
    BufferAttribute,
    BufferGeometry,
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

_CAMERA = None
_RENDERER = None
_SCENE = None
_HEIGHT = js.window.innerHeight
_WIDTH = js.window.innerWidth

_RECTS = []


class Rect():
    # three.js length units are in meters
    RECT_MIN_SIZE = 1.25
    RECT_MAX_SIZE = 2.0

    def __init__(self, index):
        self.index = index
        self._size = utils.rand_float(self.RECT_MIN_SIZE, self.RECT_MAX_SIZE)

        # The radius of a "bounding circle"
        # Pythagoras
        self.radius = (math.sqrt(2) * self._size) / 2
        self._position = Rect._position_on_orbit()
        self._angle = self._get_angle()
        self._rotation = Euler.new(0, 0, utils.rand_float(0, math.tau))
        # [-0.19, 0.19] within 0.03 degree of 0.
        self._orbit_angular_speed = utils.avoid_zero(0.19, 0.03)
        # [-1.5, 1.5] within 0.3 degree of 0.
        self._object_angular_speed = utils.avoid_zero(1.5, 0.3)
        self._plane_geometry = PlaneGeometry.new(self._size, self._size)
        self._outline_geometry = EdgesGeometry.new(self._plane_geometry)
        self._plane_material = MeshBasicMaterial.new(
            transparent=True,
            side=DoubleSide,
            opacity=utils.map_linear(self._size, 1.5, 0.75, 0.588, 0.784)
        )
        self._outline_material = LineBasicMaterial.new(
            transparent=True,
            side=DoubleSide,
            opacity=utils.map_linear(self._size, 1.5, 0.75, 0.588, 0.784),
            linewidth=2
        )
        self._plane_mesh = Mesh.new(self._plane_geometry, self._plane_material)
        self._outline_mesh = LineSegments.new(self._outline_geometry,
                                              self._outline_material)
        self._plane_mesh.position.copy(self._position)
        self._plane_mesh.rotation.copy(self._rotation)
        self._plane_mesh.add(self._outline_mesh)
        self.recolor()

    def get_mesh_object(self):
        return self._plane_mesh

    def _get_angle(self):
        return math.atan2(self._position.y, self._position.x)

    def orbit(self):
        x_pos = self._position.x
        y_pos = self._position.y
        theta = math.radians(self._orbit_angular_speed)
        self._position.x = x_pos * math.cos(theta) + y_pos * math.sin(theta)
        self._position.y = y_pos * math.cos(theta) - x_pos * math.sin(theta)
        self._plane_mesh.position.copy(self._position)
        self._angle = self._get_angle()

    def rotate(self):
        self._rotation.z += math.radians(self._object_angular_speed)
        self._plane_mesh.rotation.z = self._rotation.z

    def recolor(self):
        blue = Color.new(0x1515eb)
        dk_blue = Color.new(0x0a0a73)
        green = Color.new(0x95c251)
        dk_green = Color.new(0x394a1f)
        angle = abs(self._angle)
        half_pi = math.pi / 2
        # Left half
        if angle >= half_pi:
            shade = utils.map_linear(angle, math.pi, half_pi, 0, 0.5)
            color = green.clone()
            other_color = blue.clone()
            stroke_color = dk_green.clone()
            other_stroke_color = dk_blue.clone()
        # Right half.
        else:
            shade = utils.map_linear(angle, 0, half_pi, 0, 0.5)
            color = blue.clone()
            other_color = green.clone()
            stroke_color = dk_blue.clone()
            other_stroke_color = dk_green.clone()
        self._plane_material.color = color.clone()
        self._plane_material.color.lerp(other_color,
                                        shade + utils.rand_float(-0.02, 0.02))
        self._outline_material.color = stroke_color.clone()
        self._outline_material.color.lerp(other_stroke_color,
                                          shade + utils.rand_float(-0.02, 0.02))

    def _choose_orbit():
        # Randomly choose an orbit, based on a set of weights.
        chance = utils.rand_float(0.0, 1.0)
        if chance < 0.18:
            return 3
        if chance < 0.50:
            return 6
        if chance < 0.78:
            return 9
        if chance < 1.0:
            return 12

        return 0

    def _position_on_orbit():
        # Generate a random position on the circumference of the orbit chosen for
        # this item.
        angle = utils.rand_float(0, math.tau)
        # Slightly offsets the position so we don't end up with the
        # visible rects orbiting on *exact* circles.
        radius = Rect._choose_orbit() + utils.rand_float(0, 3)
        creation_x = math.cos(angle) * radius
        creation_y = math.sin(angle) * radius
        # Add a teensy z-offset to mitigate z-fighting
        creation_z = utils.rand_float(-0.01, 0.01)
        return Vector3.new(creation_x, creation_y, creation_z)


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
        19,  # Near clip.
        21  # Far clip.
    )

    _CAMERA.lookAt(Vector3.new(0, 0, 0))
    _CAMERA.updateProjectionMatrix()
    _RENDERER = utils.renderer_config(WebGLRenderer, _WIDTH, _HEIGHT, Color.new(0x46474c))


def _setup():
    global _RECTS

    num_rects = 100

    _CAMERA.setFocalLength = 70
    _CAMERA.position.z = 20
    _CAMERA.updateProjectionMatrix()
    _RECTS = [Rect(index) for index in range(num_rects)]
    for rect in _RECTS:
        _SCENE.add(rect.get_mesh_object())
    js.window.addEventListener('resize', create_proxy(_handle_resize))
    js.document.body.appendChild(_RENDERER.domElement)
    _RENDERER.setAnimationLoop(create_proxy(_animate))
    _RENDERER.render(_SCENE, _CAMERA)


def _animate(*args):
    def connect(this_rect, other_rect, scene):
        lines = {}
        distance = this_rect._position.distance(other_rect.position)
        if (distance < this_rect.radius + other_rect.radius):
            # and distance > abs(this_rect.radius - other_rect.radius)):
            if check_in_dict():
                # # Update the line with world positions of boxes
                # points = []
                # for box in boxes:
                #     box_position = Vector3.new()
                #     box.getWorldPosition(box_position)
                #     points.append(box_position)
                # line.geometry.setFromPoints(points)
            else:
                line = BufferGeometry.new()
                verts = js.Float32Array.new([
                    this_rect._position.x, this_rect._position.y, this_rect._position.z,
                    other_rect.position.x, other_rect.position.y, other_rect.position.z
                    ])
                line.setAttribute('position', BufferAttribute.new(verts, 3))
                line_mat = LineBasicMaterial.new()
                line_mesh = LineSegments.new(line, line_mat)
                add_to_dict()
                scene.add(line_mesh)
        else:
            delete_from_dict()

    def update():
        for this_rect in _RECTS:
            for other_rect in _RECTS:
                if other_rect.index != this_rect.index:
                    connect(this_rect, other_rect)

    for rect in _RECTS:
        update()
        rect.rotate()
        rect.orbit()
        rect.recolor()
    _RENDERER.render(_SCENE, _CAMERA)


pyscript_loader.close()

_init()
_setup()
_animate()
