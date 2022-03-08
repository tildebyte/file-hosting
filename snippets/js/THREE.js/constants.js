const TAU = Math.PI * 2,
    Width = window.innerWidth,
    Height = window.innerHeight,
    // (x, a1, a2, b1, b2)
    map = THREE.Math.mapLinear,
    // (x, y, t)
    lerp = THREE.Math.lerp,
    // (value, min, max)
    clamp = THREE.Math.clamp,
    // (x, min, max)
    // Returns the percentage (0-1) that x has moved between min and max,
    // with easing in to/out of min and max.
    smoothstep = THREE.Math.smoothstep,
    degToRad = THREE.Math.degToRad,
    radToDeg = THREE.Math.radToDeg,
    // (low, high) Random integer from low to high interval.
    randInt = THREE.Math.randInt,
    // (low, high) Random float from low to high interval.
    randFloat = THREE.Math.randFloat,
    randFLoatSpread = THREE.Math.randFloatSpread
