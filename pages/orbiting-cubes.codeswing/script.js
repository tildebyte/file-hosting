// 1. One hundred cubes
// 2. Of randomly-selected size
// 3. Each having semi-tranparent fill and stroke
// 4. Each colored according to an underlying algorithm
// 5. Each rotating around its own center with a randomly-selected speed and
//    direction
// 6. Randomly distributed around the circumference of
// 7. One of several concentric circles
// 8. All cubes rotating at a randomly-selected speed and direction around
//    a common center point
//
// Implementation by Ben Alkov December 2016

'use strict'


const GREY = new THREE.Color('rgb(70, 71, 76)'),
      BLUE = new THREE.Color('rgb(37, 37, 196)'),
      GREEN = new THREE.Color('rgb(125, 181, 40)'),
      FOG = new THREE.Color('rgb(0, 0, 0)')


let scene,
    camera,
    renderer,
    cubes = []


class Cube {
    constructor() {
        this.size = randFloat(0.75, 1.5)
        let returns = Cube.positionOnOrbit()
        this.position = returns[0]
        this.alpha = returns[1]
        this.angle = this.getAngle()
        this.rotation = new THREE.Euler(0, 0, randFloat(0, TAU))
        // [-0.19, 0.19] within 0.03 degree of 0.
        this.orbitAngularSpeed = avoidZero(0.19, 0.03)
        // [-1.5, 1.5] within 0.3 degree of 0.
        this.objectAngularSpeed = avoidZero(1.5, 0.3)
        this.cubeGeometry = new THREE.BoxGeometry(this.size, this.size, this.size)
        // Or WireframeGeometry(geo) to render all edges.
        this.outlineGeometry = new THREE.EdgesGeometry(this.cubeGeometry)
        this.cubeMaterial = new THREE.MeshBasicMaterial({
            'transparent': true,
            'opacity': map(this.alpha / 0.8, 0, 15, 0, 1)
        })
        this.outlineMaterial = new THREE.LineBasicMaterial({
            'transparent': true,
            'opacity': map(this.alpha, 0, 8, 0, 1),
            'linewidth': 2
        })
        this.cubeMesh = new THREE.Mesh(this.cubeGeometry, this.cubeMaterial)
        this.outlineMesh = new THREE.LineSegments(this.outlineGeometry,
                                                  this.outlineMaterial)
        this.cubeMesh.position.copy(this.position)
        this.cubeMesh.rotation.copy(this.rotation)
        this.cubeMesh.add(this.outlineMesh)
        this.recolor()
    }

    getMeshObject() {
        return this.cubeMesh
    }

    getAngle() {
        let position
        position = new THREE.Vector2(this.position.x, this.position.y)
        return position.angle()
    }

    orbit() {
        let x = this.position.x,
            y = this.position.y,
            theta = degToRad(this.orbitAngularSpeed)
        this.position.x = x * Math.cos(theta) + y * Math.sin(theta)
        this.position.y = y * Math.cos(theta) - x * Math.sin(theta)
        this.cubeMesh.position.copy(this.position)
        this.angle = this.getAngle()
    }

    rotate() {
        this.rotation.x += degToRad(this.objectAngularSpeed)
        this.rotation.y += degToRad(this.objectAngularSpeed)
        this.rotation.z += degToRad(this.objectAngularSpeed)
        this.cubeMesh.rotation.x = this.rotation.x
        this.cubeMesh.rotation.y = this.rotation.y
        this.cubeMesh.rotation.z = this.rotation.z
    }

    recolor() {
        // This looks weird because, AFAICT, lerping with a var of type `Color`
        //     **overwrites** the var with the new `Color` value (as well as
        //     changing the color being lerped, as expected). I'm working around
        //     this by always creating entirely new `Color` vars each time. Which
        //     is probably overkill.
        let color,
            otherColor,
            shade
        // Left half.
        if (degToRad(90) <= this.angle && this.angle <= degToRad(270)) {
            // 2nd quad.
            if (degToRad(90) <= this.angle && this.angle <= degToRad(180)) {
                shade = map(radToDeg(this.angle), 180, 90, 0, 0.5)
            }
            // 3rd quad.
            else if (degToRad(180) < this.angle && this.angle <= degToRad(270)) {
                shade = map(radToDeg(this.angle), 180, 270, 0, 0.5)
            }
            color = new THREE.Color(GREEN)
            otherColor = new THREE.Color(BLUE)
        }
        // Right half.
        else {
            // 1st quad.
            if (degToRad(0) <= this.angle && this.angle < degToRad(90)) {
                shade = map(radToDeg(this.angle), 0, 89.99, 0, 0.5)
            }
            // 4th quad.
            else if (degToRad(270) < this.angle && this.angle <= degToRad(360)) {
                shade = map(radToDeg(this.angle), 360, 269.99, 0, 0.5)
            }
            color = new THREE.Color(BLUE)
            otherColor = new THREE.Color(GREEN)
        }

        this.cubeMaterial.color = color
        this.cubeMaterial.color.lerp(new THREE.Color(otherColor),
                                      shade + randFloat(-0.02, 0.02))
        this.outlineMaterial.color = this.cubeMaterial.color
    }

    static chooseOrbit() {
        // Randomly choose an orbit, based on a set of weights.
        // Tweak the orbits by adjusting the divisors.
        let chance = Math.random(),
            orbit
        if (chance < 0.18) {
            orbit = 3
        }
        else if (chance < 0.50) {
            orbit = 6
        }
        else if (chance < 0.78) {
            orbit = 9
        }
        else if (chance < 1.0) {
            orbit = 12
        }
        return orbit
    }

    static positionOnOrbit() {
        let position,
            // Generate a random position on the circumference of the orbit chosen for
            // this item.
            angle = randFloat(0, TAU),
            // Slightly offsets the position so we don't end up with the
            // visible cubes orbiting on *exact* circles.
            radius = Cube.chooseOrbit() + randFloat(0, 3),
            creationX = Math.cos(angle) * radius,
            creationY = Math.sin(angle) * radius
        position =  new THREE.Vector3(creationX, creationY, 0)
        return [position, radius]
    }
}


window.requestAnimationFrame = platformRequestAnimationFrame()


function init() {
    if (!Detector.webgl) {Detector.addGetWebGLMessage()}
    scene = new THREE.Scene()
    scene.fog = new THREE.FogExp2(FOG, 0.018)
    camera = new THREE.PerspectiveCamera(
        18,  // F.O.V.
        Width / Height,  // Aspect.
        60,  // Near clip.
        100  // Far clip.
    )
    camera.position.y = -70
    camera.position.z = 30
    camera.lookAt(new THREE.Vector3(0, 0, 0))
    rendererConfig(GREY)
    window.addEventListener('resize', onWindowResize, false)
}


function setup() {
    for (let idx of _.range(100)) {
        cubes[idx] = new Cube()
        scene.add(cubes[idx].getMeshObject())
    }
}


function update() {
    for (let rect of cubes) {
        rect.rotate()
        rect.orbit()
        rect.recolor()
    }
}


function animate() {
    requestAnimationFrame(animate)
    update()
    renderer.render(scene, camera)
}


init()
setup()
animate()
