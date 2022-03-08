function rendererConfig(clearColor=0x000000) {
    renderer = new THREE.WebGLRenderer({'antialias': true})
    renderer.setPixelRatio(window.devicePixelRatio)
    renderer.setSize(Width, Height)
    renderer.setClearColor(clearColor, 1.0)
    document.body.appendChild(renderer.domElement)
}
