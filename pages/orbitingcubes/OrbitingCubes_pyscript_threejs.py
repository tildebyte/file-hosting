# 1. One hundred cubes
# 2. Of randomly-selected size
# 3. Each having semi-tranparent fill and stroke
# 4. Each colored according to an underlying algorithm
# 5. Each rotating around its own center with a randomly-selected speed and
#    direction
# 6. Randomly distributed around the circumference of
# 7. One of several concentric circles
# 8. All cubes rotating at a randomly-selected speed and direction around
#    a common center point
#
# Updated implemention, using pyscript and three.js by Ben Alkov May 2022
# Implementation by Ben Alkov December 2016

import math

# Not strictly necessary, but seeing naked e.g. `document`, `window`, etc. really bothers me
import js

from pyodide import create_proxy

from three import (
    AmbientLight,
    BoxBufferGeometry,
    Color,
    ColorManagement,
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
    Vector2,
    Vector3,
    WebGLRenderer,
)

import utils

WIDTH = js.window.innerWidth
HEIGHT = js.window.innerHeight
SCENE = None
AMB_LIGHT = None
LIGHT = None
CAMERA = None
RENDERER = None

cubes = None


class Cube():
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
    _cube_max_extent = math.sqrt(3) * CUBE_MAX_SIZE

    # First orbit is a little larger than the diagonal extent of the largest cube
    _first_orbit = _cube_max_extent + (CUBE_MAX_SIZE * 0.5)
    ORBITS = (_first_orbit, _first_orbit * 2,
              _first_orbit * 3, _first_orbit * 4)

    def __init__(self):
        self._size = utils.randFloat(Cube.CUBE_MIN_SIZE, Cube.CUBE_MAX_SIZE)
        self._position, self._radius = Cube._positionOnOrbit()
        self._angle = self._updateAngle()
        self._rotation = Euler.new(0.0, 0.0, utils.randFloat(0.0, math.tau))
        self._orbitAngularSpeed = utils.avoidZero(Cube.ORBIT_SPEED_LIMIT,
                                                  Cube.ORBIT_SPEED_TOLERANCE)
        self._objectAngularSpeed = utils.avoidZero(Cube.SELF_ROT_SPEED_LIMIT,
                                                   Cube.SELF_ROT_TOLERANCE)
        self._cubeGeometry = BoxBufferGeometry.new(self._size, self._size, self._size)
        self._outlineGeometry = EdgesGeometry.new(self._cubeGeometry)
        self._cubeMaterial = MeshLambertMaterial.new(
            transparent=True,
            side=DoubleSide,

            # More transparent *away from* the origin
            opacity=utils.mapLinear(self._radius * 0.8,
                                    Cube.ORBITS[0],  Cube.ORBITS[3], 1.0, 0.1)
        )
        self._outlineMaterial = LineBasicMaterial.new(
            transparent=True,
            side=DoubleSide,

            # More transparent *toward* the origin
            opacity=utils.mapLinear(self._radius * 0.8,
                                    Cube.ORBITS[0],  Cube.ORBITS[3], 0.6, 1.0)
        )
        self._outlineMesh = LineSegments.new(self._outlineGeometry,
                                             self._outlineMaterial)
        self._cubeMesh = Mesh.new(self._cubeGeometry,
                                  self._cubeMaterial)
        self._cubeMesh.position.copy(self._position)
        self._cubeMesh.rotation.copy(self._rotation)
        self._cubeMesh.add(self._outlineMesh)
        self.recolor()

    def _updateAngle(self):
        position = Vector2.new(self._position.x, self._position.y)

        # Returns radians!
        return position.angle()

    def getMeshObject(self):
        return self._cubeMesh

    def orbit(self):
        x = self._position.x
        y = self._position.y
        theta = math.radians(self._orbitAngularSpeed)
        self._position.x = x * math.cos(theta) + y * math.sin(theta)
        self._position.y = y * math.cos(theta) - x * math.sin(theta)
        self._cubeMesh.position.copy(self._position)
        self._angle = self._updateAngle()

    def rotate(self):
        self._rotation.x += math.radians(self._objectAngularSpeed)
        self._rotation.y += math.radians(self._objectAngularSpeed)
        self._rotation.z += math.radians(self._objectAngularSpeed)
        self._cubeMesh.rotation.x = self._rotation.x
        self._cubeMesh.rotation.y = self._rotation.y
        self._cubeMesh.rotation.z = self._rotation.z

    def recolor(self):
        blue = Color.new(0x2525C4)
        green = Color.new(0x7DB528)
        angle = math.degrees(self._angle)

        # Left half
        if (90 <= angle <= 270):
            # 2nd quad
            if (90 <= angle <= 180):
                shade = utils.mapLinear(angle, 180, 90, 0.0, 0.5)

            # 3rd quad
            elif (180 < angle <= 270):
                shade = utils.mapLinear(angle, 180, 270, 0.0, 0.5)

            color = green.clone()
            otherColor = blue.clone()

        # Right half
        else:
            # 1st quad
            if (0 <= angle < 90):
                shade = utils.mapLinear(angle, 0, 89.99, 0.0, 0.5)

            # 4th quad
            elif (270 < angle <= 360):
                shade = utils.mapLinear(angle, 360, 269.99, 0.0, 0.5)

            color = blue.clone()
            otherColor = green.clone()

        self._cubeMaterial.color = color.clone()
        self._cubeMaterial.color.lerp(otherColor.clone(),
                                      # avoid obvious color bands
                                      shade + utils.randFloat(-0.02, 0.02))
        self._outlineMaterial.color = self._cubeMaterial.color.clone()

        # Outline color is 50% more saturated, 15% darker than cube color
        self._outlineMaterial.color.offsetHSL(0.0, 0.50, -0.15)

    def _chooseOrbit():
        # Randomly choose an orbit, based on a set of probabilities.
        # The probabilities favor larger orbits, as they have more room for more cubes.
        chance = utils.randFloat(0.0, 1.0)
        if chance < 0.16:
            orbit = Cube.ORBITS[0]
        elif chance < 0.40:
            orbit = Cube.ORBITS[1]
        elif chance < 0.72:
            orbit = Cube.ORBITS[2]
        elif chance < 1.0:
            orbit = Cube.ORBITS[3]
        return orbit

    def _positionOnOrbit():
        # Generate a random position on the circumference of the orbit chosen for
        # this item.
        angle = utils.randFloat(0.0, math.tau)
        orbit = Cube._chooseOrbit()

        # Randomly offset the position on the orbit, so we don't end up with multiple
        # cubes orbiting on *exactly* the same circles.
        radius = orbit + utils.randFloat(0.0, Cube.ORBITS[0])
        creationX = math.cos(angle) * radius
        creationY = math.sin(angle) * radius
        position = Vector3.new(creationX, creationY, 0)
        return [position, radius]


def init():
    global SCENE
    global AMB_LIGHT
    global LIGHT
    global CAMERA
    global RENDERER

    py_canvas = js.document.getElementById('py_canvas')
    py_canvas.querySelector('.loading').remove()

    ColorManagement.legacyMode = False

    # Global Z-up
    Object3D.DefaultUp = Vector3.new(0, 0, 1)

    SCENE = Scene.new()
    LIGHT = DirectionalLight.new()
    AMB_LIGHT = AmbientLight.new()
    CAMERA = PerspectiveCamera.new(
        50,  # F.O.V.
        WIDTH / HEIGHT,  # Aspect
        30,  # Near clip
        34  # Far clip
    )
    # Camera Z-up
    CAMERA.up.set(0, 0, 1)
    dk_blue = Color.new(0x111550)
    RENDERER = utils.rendererConfig(WebGLRenderer, WIDTH, HEIGHT, dk_blue)


def setup():
    global cubes

    num_cubes = 100

    CAMERA.setFocalLength = 70
    CAMERA.position.x = 0
    CAMERA.position.y = 0
    CAMERA.position.z = 32
    CAMERA.lookAt(Vector3.new(0, 0, 0))
    LIGHT.intensity = 2.0
    amber = Color.new(0xb3a297)
    AMB_LIGHT.color = amber
    AMB_LIGHT.intensity = 0.6
    SCENE.add(LIGHT)
    SCENE.add(AMB_LIGHT)
    cubes = [Cube() for _ in range(num_cubes)]
    for cube in cubes:
        SCENE.add(cube.getMeshObject())
    js.document.body.appendChild(RENDERER.domElement)
    js.window.requestAnimationFrame = utils.platformRequestAnimationFrame()
    RENDERER.render(SCENE, CAMERA)


def update():
    for cube in cubes:
        cube.rotate()
        cube.orbit()
        cube.recolor()


def animate(*args):
    js.window.requestAnimationFrame(create_proxy(animate))
    update()
    RENDERER.render(SCENE, CAMERA)


init()
setup()
animate()
