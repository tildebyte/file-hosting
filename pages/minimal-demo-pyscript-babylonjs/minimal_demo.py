# Adapted from https://www.npmjs.com/package/babylonjs#user-content-usage, the most minimal
# example I could find anywhere
# Ported to pyscript by Ben Alkov, 2022-06

# Not strictly necessary, but seeing
# e.g. naked `document`, `window`, etc. really bothers me
import js
from pyodide import create_proxy

babylonjs = js.window.BABYLON


def _handle_render():
    scene.render()


def _handle_resize(*args):
    engine.resize()


canvas = js.document.getElementById("renderCanvas")
engine = babylonjs.Engine.new(canvas, True, preserveDrawingBuffer=True, stencil=True)


def create_scene(engine):
    scene = babylonjs.Scene.new(engine)
    camera = babylonjs.FreeCamera.new('camera1', babylonjs.Vector3.new(0, 5, -10), scene)
    camera.setTarget(babylonjs.Vector3.Zero())
    camera.attachControl(canvas, False)
    light = babylonjs.HemisphericLight.new('light1', babylonjs.Vector3.new(0, 1, 0), scene)
    sphere = babylonjs.Mesh.CreateSphere('sphere1', 16, 2, scene, False, babylonjs.Mesh.FRONTSIDE)
    sphere.position.y = 1
    ground = babylonjs.Mesh.CreateGround('ground1', 6, 6, 2, scene, False)
    return scene


scene = create_scene(engine)
engine.runRenderLoop(create_proxy(_handle_render))
js.window.addEventListener("resize", create_proxy(_handle_resize))
