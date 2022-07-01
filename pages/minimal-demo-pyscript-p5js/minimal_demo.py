# Ben Alkov, 2022-07

# Not strictly necessary, but seeing
# e.g. naked `document`, `window`, etc. really bothers me
import js

p5js = js.window.p5.new()


# These are named per convention: p5js doesn't know anything about them

def setup():
    js.window.createCanvas(200, 200)


def draw():
    js.window.background(0)
    js.window.fill(255)
    js.window.ellipse(100, 100, 50, 50)


setup()
draw()
