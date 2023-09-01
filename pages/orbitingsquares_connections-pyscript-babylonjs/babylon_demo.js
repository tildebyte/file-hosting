const createScene = function () {
    const origin = new BABYLON.Vector3.Zero()
    const x_axis = new BABYLON.Vector3(1, 0, 0)
    const y_axis = new BABYLON.Vector3(0, 1, 0)
    const z_axis = new BABYLON.Vector3(0, 0, 1)

    const scene = new BABYLON.Scene(engine)
    scene.ambientColor = new BABYLON.Color3(1, 1, 1)
    scene.diffuseColor = new BABYLON.Color3(1, 1, 1)
    scene.specularColor = new BABYLON.Color3(1, 1, 1)

    const camera = new BABYLON.ArcRotateCamera("Camera", -Math.PI / 2, Math.PI / 2, 3, origin)
    camera.attachControl(canvas, true)

    const light = new BABYLON.HemisphericLight("light", new BABYLON.Vector3(1, 1, 0))

	const redMat = new BABYLON.StandardMaterial("redMat", scene)
	redMat.diffuseColor = new BABYLON.Color3(0.99, 0.04, 0.04)
    redMat.alpha = 0.5

	const blueMat = new BABYLON.StandardMaterial("blueMat", scene)
	blueMat.diffuseColor = new BABYLON.Color3(0.18, 0.04, 0.99)
    blueMat.alpha = 0.5

    const plane = BABYLON.MeshBuilder.CreatePlane("plane", {size: 1, sideOrientation: BABYLON.Mesh.DOUBLESIDE})
    plane.material = redMat
    plane.enableEdgesRendering()
    plane.edgesWidth = 0.5
    plane.edgesColor = new BABYLON.Color4(0, 0, 1, 0.5)
    // plane.translate(x_axis, 1)
    // radians, CCW-based
    // plane.rotation.z  =  -0.1

    const plane2 = BABYLON.MeshBuilder.CreatePlane("plane", {size: 1, sideOrientation: BABYLON.Mesh.DOUBLESIDE})
    plane2.material = blueMat
    plane2.enableEdgesRendering()
    plane2.edgesWidth = 0.5
    plane2.edgesColor = new BABYLON.Color4(1, 0, 0, 0.5)
    plane2.translate(z_axis, 0.01)
    plane2.rotation.z  = -0.75

    return scene
};