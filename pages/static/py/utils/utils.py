import js
import random


def avoidZero(range, tolerance):
    # Return a random value in the range from `-range` to strictly less than
    # `range`, excluding the inner range +/-`tolerance` (and, logically, zero as
    # well).
    value = randFloat(-range, range)
    while -tolerance < value and value < tolerance:
        value = randFloat(-range, range)
    return value


# Linear mapping from range [from_start, from_end] to range [to_start, to_end]
def mapLinear(x, from_start, from_end, to_start, to_end):
    """Implementation as found in three.js
        Pending merge of https://github.com/pyodide/pyodide/pull/2520
    """
    return to_start + (x - from_start) * (to_end - to_start) / (from_end - from_start)


def platformRequestAnimationFrame():
    return (js.window.requestAnimationFrame or
            js.window.mozRequestAnimationFrame or
            js.window.webkitRequestAnimationFrame)


# Random float from [low, high] interval
def randFloat(start, end):
    """Implementation as found in three.js
        Pending merge of https://github.com/pyodide/pyodide/pull/2520
    """
    return start + random.random() * (end - start)


def rendererConfig(renderer, width, height, clearColor=0x000000):
    renderer = renderer.new(
        powerPreference='high-performance',
        antialias=True,
        stencil=False,
        depth=True
    )
    renderer.setPixelRatio(js.window.devicePixelRatio)
    renderer.setSize(width, height)
    renderer.setClearColor(clearColor, 1.0)
    return renderer
