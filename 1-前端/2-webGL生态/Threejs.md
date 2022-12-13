## Rotation

### reorder

`mesh.rotation.reorder('YXZ')`

reorder the rotation order of X Y Z



## AxesHelper

AxesHelper：

```js
const axesHelper = new AxesHelper(7)

scene.add(axesHelper) 
```



## clock

### getElapsedTime

get elapsed time

```js
clock.getElapsedTime()
```



## Controls

### OrbitControls

Orbit controls allow the camera to orbit around a target.



## gsap (npm package -- transform and rotation)

### transform

```js
gsap.to(group.position, {
    duration: 5,
    z: 2,
})
```

### rotation

```js
gsap.to(group.rotation, {
  duration: 5,
  z: Math.PI * 2,
})
```





## full Screen and exit

```js
/**
 * double click to fullScreen
 */
window.addEventListener("dblclick", () => {
  const fullScreen =
    document.fullscreenElement || document.webkitFullscreenElement;
  if (!fullScreen) {
    if (canvas.requestFullscreen) {
      canvas.requestFullscreen();
    } else if (canvas.webkitRequestFullscreen) {
      canvas.webkitRequestFullscreen();
    }
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen();
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen();
    }
  }
});
```



## show Mesh by wire

```ture
const material = new THREE.MeshBasicMaterial({ 
  color: 0xff0000, 
  wireframe: true 
});
```



## BufferAttribute

1. instantiate a geometry
2. make BufferAttribute
3. set BufferAtrribute

```js
const geometry = new THREE.BufferGeometry() // instantiate a geometry
const array = new Float32Array([
  0, 0, 0,
  0, 1, 0,
  1, 0, 0
])
const positionsAttribute = new THREE.BufferAttribute(array, 3) // make BufferAttribute
geometry.setAttribute('position', positionsAttribute) // set BufferAtrribute
```



## dat.gui

document:

[dat.gui/API.md at master · dataarts/dat.gui (github.com)](https://github.com/dataarts/dat.gui/blob/master/API.md)



transform:

```js
// x y z
gui.add(mesh.position, 'x', -3, 3, 0.01).name('boxX')
gui.add(mesh.position, 'y', -3, 3, 0.01)
gui.add(mesh.position, 'z', -3, 3, 0.01)
```

visible

```js
gui.add(mesh, 'visible')
```

wire frame

```js
gui.add(material, 'wireframe')
```

color

```js
const boxColor = {
    color: 0xff0000
}
gui.addColor(boxColor, 'color')
    .onChange((val) => {
        material.color.set(val) 
    })
```

defined function （such as spin）

```
parameters.spin = () => {
    mesh.rotation.set(0, 0, 0)
    gsap.to(mesh.rotation, {
        y: Math.PI,
        duration: 2
    })
}
gui.add(parameters, 'spin')
```

