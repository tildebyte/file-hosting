import random

from typing import Any

import js


def avoid_zero(range_: float, tolerance: float) -> float:
    # Return a random value in the range from `-range` to strictly less than
    # `range`, excluding the inner range +/-`tolerance` (and, logically, zero as
    # well).
    attempt: float = rand_float(-range_, range_)
    while -tolerance < attempt and attempt < tolerance:
        attempt = rand_float(-range_, range_)
    return attempt


# Linear mapping from range [from_start, from_end] to range [to_start, to_end]
def map_linear(to_map: float,
               from_start: float, from_end: float,
               to_start: float, to_end: float) -> float:
    """Implementation as found in three.js
        Pending merge of https://github.com/pyodide/pyodide/pull/2520
    """
    return to_start + (to_map - from_start) * (to_end - to_start) / (from_end - from_start)


def platform_request_animation_frame() -> Any:
    return (js.window.requestAnimationFrame or
            js.window.mozRequestAnimationFrame or
            js.window.webkitRequestAnimationFrame)


# Random float from [low, high] interval
def rand_float(start: float, end: float) -> float:
    """Implementation as found in three.js
        Pending merge of https://github.com/pyodide/pyodide/pull/2520
    """
    return start + random.random() * (end - start)


def renderer_config(renderer: Any, width: int,
                    height: int, clear_color: int=0x000000) -> Any:
    renderer = renderer.new(
        powerPreference='high-performance',
        antialias=True,
        stencil=False,
        depth=True
    )
    renderer.setPixelRatio(js.window.devicePixelRatio)
    renderer.setSize(width, height)
    renderer.setClearColor(clear_color, 1.0)
    return renderer
