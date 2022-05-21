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

import js

from pyodide import create_proxy


from three import (
    BoxGeometry,
    Color,
    DirectionalLight,
    EdgesGeometry,
    Euler,
    FogExp2,
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

SCENE = None
LIGHT = None
CAMERA = None
RENDERER = None

GREY = Color.new('rgb(0, 6, 18)')
BLUE = Color.new('rgb(37, 37, 196)')
GREEN = Color.new('rgb(125, 181, 40)')
FOG = Color.new('rgb(0, 0, 0)')

NUM_CUBES = 100
cubes = None


class Cube():
    CUBE_MIN_SIZE = 0.75
    CUBE_MAX_SIZE = 1.5
    # [-0.06, 0.06] within 0.03 degree of 0
    ORBIT_LIMIT = 0.06
    ORBIT_TOLERANCE = 0.03
    # [-0.8, 0.8] within 0.3 degree of 0
    OBJECT_ROT_LIMIT = 0.8
    OBJECT_ROT_TOLERANCE = 0.3

    def __init__(self):
        self._size = utils.randFloat(Cube.CUBE_MIN_SIZE, Cube.CUBE_MAX_SIZE)
        self._position, self._opac = Cube._positionOnOrbit()
        self._angle = self._updateAngle()
        self._rotation = Euler.new(0, 0, utils.randFloat(0, math.tau))
        self._orbitAngularSpeed = utils.avoidZero(Cube.ORBIT_LIMIT,
                                                  Cube.ORBIT_TOLERANCE)
        self._objectAngularSpeed = utils.avoidZero(Cube.OBJECT_ROT_LIMIT,
                                                   Cube.OBJECT_ROT_TOLERANCE)
        self._cubeGeometry = BoxGeometry.new(self._size, self._size, self._size)
        # Or WireframeGeometry(geo) to render all edges.
        self._outlineGeometry = EdgesGeometry.new(self._cubeGeometry)
        self._cubeMaterial = MeshLambertMaterial.new(
            transparent=True,
            # More *transparent* away from the origin
            opacity=utils.mapLinear(self._opac * 0.8, 15, 3, 0.1, 1)
        )
        self._outlineMaterial = LineBasicMaterial.new(
            transparent=True,
            # More *opaque* away from the origin
            opacity=utils.mapLinear(self._opac * 0.8, 3, 15, 0.6, 1)
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
        angle = math.degrees(self._angle)
        # Left half
        if (90 <= angle <= 270):
            # 2nd quad
            if (90 <= angle <= 180):
                shade = utils.mapLinear(angle, 180, 90, 0, 0.5)

            # 3rd quad
            elif (180 < angle <= 270):
                shade = utils.mapLinear(angle, 180, 270, 0, 0.5)

            color = Color.new(GREEN)
            otherColor = Color.new(BLUE)

        # Right half
        else:
            # 1st quad
            if (0 <= angle < 90):
                shade = utils.mapLinear(angle, 0, 89.99, 0, 0.5)

            # 4th quad
            elif (270 < angle <= 360):
                shade = utils.mapLinear(angle, 360, 269.99, 0, 0.5)

            color = Color.new(BLUE)
            otherColor = Color.new(GREEN)

        self._cubeMaterial.color = color
        # This looks weird because, AFAICT, lerping with a var of type `Color`
        #     **overwrites** the var with the new `Color` value (as well as
        #     changing the color being lerped, as expected). I'm working around
        #     this by always creating entirely new `Color` vars each time. Which
        #     is probably overkill.
        self._cubeMaterial.color.lerp(Color.new(otherColor),
                                      shade + utils.randFloat(-0.02, 0.02))
        self._outlineMaterial.color = self._cubeMaterial.color

    def _chooseOrbit():
        # Randomly choose an orbit, based on a set of weights.
        # Tweak the orbits by adjusting the divisors.
        chance = utils.randFloat(0, 1)
        if (chance < 0.18):
            orbit = 3

        elif (chance < 0.50):
            orbit = 6

        elif (chance < 0.78):
            orbit = 9

        elif (chance < 1.0):
            orbit = 12

        return orbit

    def _positionOnOrbit():
        # Generate a random position on the circumference of the orbit chosen for
        # this item.
        angle = utils.randFloat(0, math.tau)
        # Slightly offsets the position so we don't end up with the
        # visible cubes orbiting on *exact* circles.
        radius = Cube._chooseOrbit() + utils.randFloat(0, 3)
        creationX = math.cos(angle) * radius
        creationY = math.sin(angle) * radius
        position = Vector3.new(creationX, creationY, 0)
        return [position, radius]


def init():
    Object3D.DefaultUp = Vector3.new(0, 0, 1)
    global SCENE
    global LIGHT
    global CAMERA
    global RENDERER

    py_canvas = js.document.getElementById('py_canvas')
    py_canvas.querySelector('.loading').remove()

    Width = js.window.innerWidth
    Height = js.window.innerHeight

    SCENE = Scene.new()
    LIGHT = DirectionalLight.new()
    CAMERA = PerspectiveCamera.new(
        50,  # F.O.V.
        Width / Height,  # Aspect
        10,  # Near clip
        300  # Far clip
    )
    CAMERA.up.set(0, 0, 1)
    RENDERER = utils.rendererConfig(WebGLRenderer, Width, Height, GREY)


def setup():
    global cubes

    # SCENE.fog = FogExp2.new(FOG, 0.022)
    SCENE.add(LIGHT)
    LIGHT.intensity = 1.0
    CAMERA.setFocalLength = 70
    CAMERA.position.x = 0
    CAMERA.position.y = 0
    CAMERA.position.z = 24
    CAMERA.lookAt(Vector3.new(0, 0, 0))

    cubes = [Cube() for _ in range(NUM_CUBES)]
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
