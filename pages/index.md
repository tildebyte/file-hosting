<!-- title: Pages -->
<!-- import "./static/css/solarized-dark.css" -->
<!-- import "./static/css/style-template.css" -->

# Pages

Sources available at [tildebyte/file-hosting][]

## Things for the web, written in Python

### Sketches and demos

- ```python
  # A wireframe box with colored edges which expands and contracts according to
  # time-of-day
  # Inspired by Gysin & Vanetti's [*hms*](https://www.gysin-vanetti.com/hms)
  ```

  - [BoxClock (pyscript & three.js)][]
- The rest of these are different visualizations of a recipe I used for a
  creative coding class (initially implemented using [processing.py][])

  ```python
  # 1. One hundred squares
  # 2. Of randomly-selected size
  # 3. Each having semi-tranparent fill and stroke
  # 4. Each colored according to an underlying algorithm
  # 5. Each rotating around its own center with a randomly-selected speed and
  #    direction
  # 6. Randomly distributed around the circumference of
  # 7. One of several concentric circles
  # 8. All squares rotating at a randomly-selected speed and direction around a
  #    common center point
  ```

  - [OrbitingSquares (pyscript & p5.js)][]
  - [OrbitingSquares (pyscript & three.js)][]
  - [OrbitingCubes (pyscript & three.js)][] (click or tap to change the visualization)
  - [OrbitingWhiskers (pyscript & three.js)][] (click or tap to change the visualization)

### Examples (minimal demos, ports of other's work)

- [Bouncy Bubbles (pyscript & p5.js)][]
- [Minimal demo (pyscript & Babylon.js)][]
- [REALLY minimal demo (pyscript & p5.js)][]

### Abandoned/buggy/experimental/incomplete/old/WIP sketches and demos

- [OrbitingSquares (transcrypt & pyp5js)][]

#### Tech used

- [Babylon.js][]
- [p5.js][]
- [pyp5js][]
- [pyscript][]
- [three.js][]
- [transcrypt][]

[Babylon.js]: https://www.babylonjs.com
[Bouncy Bubbles (pyscript & p5.js)]: ./bouncy-bubbles-pyscript-p5js/
[BoxClock (pyscript & three.js)]: ./boxclock-pyscript-threejs/
[Minimal demo (pyscript & Babylon.js)]: ./minimal-demo-pyscript-babylonjs.html
[REALLY minimal demo (pyscript & p5.js)]: ./minimal-demo-pyscript-p5js.html
[OrbitingCubes (pyscript & three.js)]: ./orbitingcubes-pyscript-threejs/
[OrbitingSquares (pyscript & p5.js)]: ./orbitingsquares-pyscript-p5js/
[OrbitingSquares (pyscript & three.js)]: ./orbitingsquares-pyscript-threejs/
[OrbitingSquares (transcrypt & pyp5js)]: ./orbitingsquares-transcrypt-pyp5js/
[OrbitingWhiskers (pyscript & three.js)]: ./orbitingwhiskers-pyscript-threejs/
[p5.js]: https://p5js.org
[processing.py]: https://py.processing.org
[pyp5js]: https://berinhard.github.io/pyp5js
[pyscript]: https://pyscript.net
[three.js]: https://threejs.org
[transcrypt]: https://transcrypt.org
[tildebyte/file-hosting]: https://github.com/tildebyte/file-hosting
