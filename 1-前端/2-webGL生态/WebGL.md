# WebGL 基础

## WebGL 简介

[ WebGL](https://www.khronos.org/webgl/) 使得网页在支持 HTML [`<canvas>`](https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element/canvas) 标签的浏览器中，不需要使用任何插件，便可以使用基于 [OpenGL ES](https://www.khronos.org/opengles/) 2.0 的 API 在 canvas 中进行 3D 渲染. WebGL 程序由 javascript 的控制代码，和在计算机的**图形处理单元**（GPU, Graphics Processing Unit）中执行的特效代码(shader code，渲染代码) 组成. WebGL 元素可以和其他 HTML 元素混合, 并且会和页面的其他部分或页面背景相合成. ---MDN

 WebGL 运行在一个特殊的 HTML`<canvas>`标签中，可以允许开发者使用 javascript 渲染并硬件(GPU)加速。由于其运行在`<canvas>`中，WebGL 也可以所有的 DOM 接口完全集成。这意味着 WebGL 可以运行在很多不同的设备中，如电脑手机或者 TV。

WebGL 比典型的 web 技术稍微复杂一些，因为它被设计成直接与你的显卡一起工作。这是相当底层的。这使得它能够快速地进行复杂的 3D 渲染，包括大量的计算。

## WebGL 渲染管线`rendering pipeline`（WebGL 渲染过程）

<img src="https://dev.opera.com/articles/introduction-to-webgl-part-1/rendering-pipeline.jpg" alt="img" style="zoom: 67%;" />

 这个过程从**创建顶点阵列**开始的。它是包含顶点属性的数组，比如顶点在 3D 空间中的位置和关于顶点纹理、颜色或如何受光照(顶点法线)影响的信息。 这些数组可以从 3D 模型或者程序创建的数据又或者某些为几何形状提供数组的库中获得。

 接着这些数据数组会通过一组或者多组顶层缓冲区的形式发送给 GPU。同时可能还需要提供一个指向顶点元素的附加索引数组。这些索引数组用来控制如何组装三角形。

 GPU 首先从顶点缓冲区中读取每个选定的顶点，并在**顶点着色器**中运行它。顶点着色器是一个程序，它以一组顶点属性作为输入，并输出一组新的属性。这个属性中至少包含着顶点着色器计算的顶点在屏幕空间中的投影位置。但它也可以为每个顶点生成颜色或纹理坐标等其他属性。你可以编写自己的顶点着色器，或者使用 WebGL 库提供的顶点着色器。

 然后 GPU 将顶点连接起来形成三角形。它通过按照索引数组指定的顺序获取顶点，并将它们分组为三个集合来实现这一点。

 光栅化程序获取每个三角形，剪辑它，丢弃屏幕以外的部分，并将剩余的可见部分分解成像素大小的片段。顶点着色器的其他顶点属性的输出也被插值到每个三角形的栅格化表面上，最终为每个片段分配一个平滑的梯度值。

 光栅化形成的像素片段通过片段着色器进行处理（ 常见的片段着色器操作包括纹理映射和光照 ），片段着色器为每一个像素输出颜色和深度并将其绘制到 frameBuffer 上。由于**GPU 的特性**，这里对**每个像素的绘制**都是独立运行的，这使得它能够执行最复杂的效果。这里可以对照 CPU 和 GPU 的处理方式不同进行理解：

<img src="https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/1652286577565.png" alt="1652286577565" style="zoom:67%;" />

<img src="https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/1652286609973.png" alt="1652286609973" style="zoom:67%;" />

framebuffer 不仅仅是一个 2D 图像，除了有一个多个色彩缓冲区外，它还具有一个`deep buffer 深度缓冲区`或者/和一个` stencil buffer 模板缓冲区`，都可以在绘画前用来过滤片段。 深度测试丢弃已经绘制的对象后面的对象。模板测试使用绘制到模板缓冲区中的形状来约束帧缓冲区的可绘制部分 。

幸存于这两个过滤器的片段的颜色值与它们重写的颜色值混合，最终的颜色、深度和模板值被绘制到相应的缓冲区中。缓冲区输出也可以用作其他渲染项目的纹理输入。

(tips: 注意第四步中的三角形组装部分，为什么是三角形？这是因为大部分的实时 3D 图像都是以三角形为基本元素的。)

## WebGL 容器（坐标系）

与 canvas 的坐标系不同，WebGL 使用的是**正交右手坐标系**，**每个方向都有可以使用的值的区间，超过该区间的图像不会被绘制。**

<img src="https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/1652326774764.png" alt="1652326774764" style="zoom:67%;" />

这样的设计可以减少不必要的开销，因为在坐标区间外的图像是不回被绘制的。

- x 轴最左边为-1，最右边为 1；
- y 轴最下边为-1，最上边为 1；
- z 轴朝向你的方向最大值为 1，远离你的方向最大值为-1；

注：这些值与 Canvas 的尺寸无关，无论 Canvas 的长宽比是多少，WebGL 的区间值都是一致的(-1 到 1）。

<img src="https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/1652342481445.png" alt="1652342481445" style="zoom:67%;" />

## 先从 WebGL 绘制一个点开始

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
    <!-- 矩阵和向量库 https://gitee.com/wizardAEI/resource 找glMatrix.js-->
    <script src="glMatrix.js"></script>
  </head>
  <body>
    <canvas id="weblCanvas" width="640" height="480">
      你的浏览器似乎不支持或者禁用了HTML5 <code>&lt;canvas&gt;</code> 元素.
    </canvas>
    <script type="text/javascript" src="main.js"></script>
  </body>
</html>
```

```js
/*
 * @Descripttion:
 * @Author: Wang Dejiang(aei)
 * @Date: 2022-05-12 16:52:42
 * @LastEditors: Wang Dejiang(aei)
 * @LastEditTime: 2022-05-12 20:32:23
 */

/**
 * @type {WebGLRenderingContext}
 */
let webgl = null

/**
 * @description mat4是从glMatrix引入的对象，该库利用提前设置的矩阵更快的生成坐标系
 */
let projMat4 = mat4.create()

//顶点着色器程序
let vertexString = `
attribute vec4 a_position;
uniform mat4 proj;
void main() {
    gl_Position = proj * a_position;
    gl_PointSize = 20.0;
}
`
//片段着色器程序
let fragmentString = `
void main() {
    gl_FragColor = vec4(0, 1.0, 1.0, 1.0);
}
`
;(function init() {
  initWebgl() //初始化webgl
  initShader() //初始化shader
  initBuffer() //输出对应buffer
  draw() //根据buffer提示画图
})()

function initWebgl() {
  let webglDiv = document.getElementById('weblCanvas')
  webgl = webglDiv.getContext('webgl')
  //设置视口
  webgl.viewport(0, 0, webglDiv.clientWidth, webglDiv.clientHeight)
  //这里用来利用glMatrix库生成一个转换坐标矩阵
  mat4.ortho(0, webglDiv.clientWidth, webglDiv.clientHeight, 0, -1, 1, projMat4)
}
function initShader() {
  //创建顶点着色器和片着色器并和对应的程序进行绑定
  let vsshader = webgl.createShader(webgl.VERTEX_SHADER)
  let fssagder = webgl.createShader(webgl.FRAGMENT_SHADER)
  webgl.shaderSource(vsshader, vertexString)
  webgl.shaderSource(fssagder, fragmentString)

  //编译shader
  webgl.compileShader(vsshader)
  webgl.compileShader(fssagder)

  //创建并绑定程序
  let program = webgl.createProgram()
  webgl.attachShader(program, vsshader)
  webgl.attachShader(program, fssagder)

  //链接并使用程序
  webgl.linkProgram(program)
  webgl.useProgram(program)

  webgl.program = program
}
function initBuffer() {
  //获取a_position数据并赋值给webgl
  let aPosition = webgl.getAttribLocation(webgl.program, 'a_position')
  //位置信息，参数分别为x,y,z,w等同于三维坐标(x/w,y/w,z/w)
  let pointPosition = new Float32Array([100.0, 100.0, 0.0, 1.0])
  //将位置信息赋值给webgl
  webgl.vertexAttrib4fv(aPosition, pointPosition)

  //获取uniform数据并赋值给webgl，这里的proj用作转换坐标系(将canvas坐标映射到webgl标准坐标系上)
  let uniformproj = webgl.getUniformLocation(webgl.program, 'proj')
  webgl.uniformMatrix4fv(uniformproj, false, projMat4)
}
function draw() {
  //冲刷颜色，这里将整体涂黑
  webgl.clearColor(0.0, 0.0, 0.0, 1.0)
  webgl.clear(webgl.COLOR_BUFFER_BIT)
  //通过buffer画上图像，表示绘画点，从下标1开始，只画一个
  webgl.drawArrays(webgl.POINTS, 0, 1)
}
```

根据上面的渲染管道流程，可以比较好的理解以上流程，这里主要说明模板字符转中的内容含义：

```js
attribute vec4 a_position;
uniform mat4 proj;
void main() {
    gl_Position = proj * a_position;
    gl_PointSize = 60.0;
}
```

第一行声明了一个 vec4 类型的变量，attribute 是一个存储限定符，被它所修饰的变量是从外部传入顶点属性的。它是 WebGL 外部顶点信息传入 WebGL 内部的桥梁变量，用 attribute 修饰的值只能出现在顶点着色器中。 vec4 类型是 4 维向量类型，用于表示顶点的坐标信息。 即`let pointPosition = new Float32Array([100.0, 100.0, 0.0, 1.0])`着段代码中的数据类型。`

uniform 类型表示可以出现在顶点着色器和片元着色器中的，表示统一的值。proj 指的是通过引入的 glMatrix 库算出的一个矩阵，通过矩阵来算出屏幕中的值转换成正交右手坐标系的位置。

void main 表示顶点着色器的 main 函数，类似于 C 语言的 main 函数，他是顶点着色器中的唯一入口函数。

gl_Position 是顶点着色器中的内置变量，它就表示了当前顶点的实际位置，所以我们需要将从外界接受信息的 a_position 和 proj 的值赋给 gl_Position 这个变量。

gl_PointSize 是顶点着色器中一个点的 size。

```js
void main() {
    gl_FragColor = vec4(0, 0, 1.0, 1.0);
}
```

main 函数中，定义了每一个片段的颜色。

## 绘制多个点

我们将 initBuffer 和 draw 两个函数进行修改，达到画多个点目的：

```js
function initBuffer() {
  //位置信息，参数分别为x,y,z,w等同于三维坐标(x/w,y/w,z/w)
  let pointPosition
  let aPosition = webgl.getAttribLocation(webgl.program, 'a_position')

  //通过鼠标点击添加点,注意坐标系的转换(这里使用的WebGL的坐标系是正交右手坐标系)
  document.addEventListener('mousedown', e => {
    let x = e.clientX,
      y = e.clientY
    let pointx = x - e.target.getBoundingClientRect().left,
      pointy = y - e.target.getBoundingClientRect().top
    points.push(pointx, pointy, 0.0, 1.0)
    pointPosition = new Float32Array(points)
    let pointBuffer = webgl.createBuffer()
    //指定类型为数组buffer
    webgl.bindBuffer(webgl.ARRAY_BUFFER, pointBuffer)
    //设置数据
    webgl.bufferData(webgl.ARRAY_BUFFER, pointPosition, webgl.STATIC_DRAW)
    webgl.enableVertexAttribArray(aPosition)
    webgl.vertexAttribPointer(aPosition, 4, webgl.FLOAT, false, 4 * 4, 0 * 4)
    draw()
  })
  //获取uniform数据并赋值
  let uniformproj = webgl.getUniformLocation(webgl.program, 'proj')
  webgl.uniformMatrix4fv(uniformproj, false, projMat4)
}
function draw() {
  //冲刷颜色，这里将整体涂黑
  webgl.clearColor(0.0, 0.0, 0.0, 1.0)
  webgl.clear(webgl.COLOR_BUFFER_BIT)
  //通过buffer画上图像
  webgl.drawArrays(webgl.POINTS, 0, points.length)
}
```

<img src="https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/1652404218368.png" alt="1652404218368" style="zoom:50%;" />

这里我们也可以自己去算从平面坐标转换成 webgl 坐标系的值，通过该图：

![1652326774764](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/1652326774764.png)

可以得出此时：

```js
;(pointx = (x - e.target.getBoundingClientRect().left - 320) / 320),
  (pointy = (240 - y - e.target.getBoundingClientRect().top) / 240)
```

那么我们就可以取消使用 glMatrix 相关的值了，最简单的做法，可以直接去除在模板字符串中的 proj：

```
let vertexString = `
attribute vec4 a_position;
uniform mat4 proj;
void main() {
    gl_Position =  a_position;
    gl_PointSize = 20.0;
}
```

## 绘制线

### 两个点连线

```js
function initBuffer() {
  let aPosition = webgl.getAttribLocation(webgl.program, 'a_position')
  let arr = [100.0, 100.0, 0.0, 1.0, 200.0, 100.0, 0.0, 1.0]
  let pointPosition = new Float32Array(arr)
  let lineBuffer = webgl.createBuffer()
  //由于是多个点，所以使用buffer类API直接绑定
  webgl.bindBuffer(webgl.ARRAY_BUFFER, lineBuffer)
  webgl.bufferData(webgl.ARRAY_BUFFER, pointPosition, webgl.STATIC_DRAW)
  webgl.enableVertexAttribArray(aPosition)
  webgl.vertexAttribPointer(aPosition, 4, webgl.FLOAT, false, 4 * 4, 0 * 4)
  //获取uniform数据并赋值
  let uniformproj = webgl.getUniformLocation(webgl.program, 'proj')
  webgl.uniformMatrix4fv(uniformproj, false, projmat4)
}
function draw() {
  //冲刷颜色，这里将整体涂黑
  webgl.clearColor(0.0, 0.0, 0.0, 1.0)
  webgl.clear(webgl.COLOR_BUFFER_BIT, webgl.DEPTH_BUFFER_BIT)
  //通过buffer画上图像，由于是两个点，最后一个参数count为2，注意这里使用的LINES，所以buffer内的坐标点数只能是偶数，每两个点连一条线
  webgl.drawArrays(webgl.LINES, 0, 2)
}
```

## 绘制三个点（奇数）的线

改变 arr 中的点数：

```js
let arr = [
  100.0, 100.0, 0.0, 1.0, 200.0, 100.0, 0.0, 1.0, 300.0, 200.0, 0.0, 1.0,
]
```

改变`drawAraays使用的API`

```js
function draw() {
  webgl.clearColor(0.0, 0.0, 0.0, 1.0)
  webgl.clear(webgl.COLOR_BUFFER_BIT, webgl.DEPTH_BUFFER_BIT)
  //使用LINE_STRIP，使点依次连接
  webgl.drawArrays(webgl.LINE_STRIP, 0, 3)
}
```

此外，还有`LINE_LOOP`（收尾相连）等 API

## 绘制三角形和多边形

### 三角形

改变 draw：

```
function draw() {
  //冲刷颜色，这里将整体涂黑
  webgl.clearColor(0.0, 0.0, 0.0, 1.0)
  webgl.clear(webgl.COLOR_BUFFER_BIT, webgl.DEPTH_BUFFER_BIT)
  //通过buffer画上图像
  webgl.drawArrays(webgl.TRIANGLES, 0, 3)
}
```

或者`webgl.drawArrays`使用`TRIANGLE_STRIP`：前三个点构成一个三角形，从第二个点开始的三个点在构成一个三角形，依次类推。

以及`TRIANGLE_FAN`：前三个点连接成一个三角形（注意是逆时针），之后最后一条线和第四个点连接成第二个三角形（一样是逆时针），以此类推。

### 多边形

做一个五角星，其中心在 webgl 的投影坐标系的中心。

此时使用投影变换的优势不大了，所以我们尝试直接使用投影坐标系的坐标：

```js
/**
 * @type {WebGLRenderingContext}
 */
let webgl = null

let points = []

// 顶点着色器程序
let vertexString = `
attribute vec4 a_position;
void main() {
    gl_Position = a_position;
    gl_PointSize = 20.0;
}
`
// 片段着色器
let fragmentString = `
void main() {
    gl_FragColor = vec4(0, 1.0, 1.0, 1.0);
}
`
;(function init() {
  initWebgl()
  initShader()
  initBuffer()
  draw()
})()

function initWebgl() {
  let webglDiv = document.getElementById('weblCanvas')
  webgl = webglDiv.getContext('webgl')
  //设置视口
  webgl.viewport(0, 0, webglDiv.clientWidth, webglDiv.clientHeight)
}
function initShader() {
  ////创建顶点着色器和片着色器并和对应的程序进行绑定
  let vsshader = webgl.createShader(webgl.VERTEX_SHADER)
  let fssagder = webgl.createShader(webgl.FRAGMENT_SHADER)
  webgl.shaderSource(vsshader, vertexString)
  webgl.shaderSource(fssagder, fragmentString)

  //编译shader
  webgl.compileShader(vsshader)
  webgl.compileShader(fssagder)

  //创建并绑定程序
  let program = webgl.createProgram()
  webgl.attachShader(program, vsshader)
  webgl.attachShader(program, fssagder)

  //链接并使用程序
  webgl.linkProgram(program)
  webgl.useProgram(program)

  webgl.program = program
}
function initBuffer() {
  let aPosition = webgl.getAttribLocation(webgl.program, 'a_position')
  let arr = [
    0.0, 0.8, 0.0, 1.0,

    -0.17, 0.15, 0.0, 1.0,

    -0.8, 0.0, 0.0, 1.0,

    -0.2, -0.2, 0.0, 1.0,

    -0.5, -0.9, 0.0, 1.0,

    0.0, -0.45, 0.0, 1.0,

    0.5, -0.9, 0.0, 1.0,

    0.2, -0.2, 0.0, 1.0,

    0.8, 0.0, 0.0, 1.0,

    0.17, 0.15, 0.0, 1.0,
  ]
  let pointPosition = new Float32Array(arr)
  let lineBuffer = webgl.createBuffer()
  webgl.bindBuffer(webgl.ARRAY_BUFFER, lineBuffer)
  webgl.bufferData(webgl.ARRAY_BUFFER, pointPosition, webgl.STATIC_DRAW)
  webgl.enableVertexAttribArray(aPosition)
  webgl.vertexAttribPointer(aPosition, 4, webgl.FLOAT, false, 4 * 4, 0 * 4)
}
function draw() {
  //冲刷颜色，这里将整体涂黑
  webgl.clearColor(0.0, 0.0, 0.0, 1.0)
  webgl.clear(webgl.COLOR_BUFFER_BIT, webgl.DEPTH_BUFFER_BIT)
  //通过buffer画上图像
  webgl.drawArrays(webgl.LINE_LOOP, 0, 10)
}
```

<img src="https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/1652700475129.png" alt="1652700475129" style="zoom:50%;" />

## 绘制多个三角形

### 索引值数组和索引缓冲区

索引值数组是通过列出数据数组中的索引值来进行复用顶点的数组，这里稍加改变绘制三角形时的 buffeinit 函数：

```js
function initBuffer() {
  let aPosition = webgl.getAttribLocation(webgl.program, 'a_position')
  //我们需要复用其中的顶点来画多个三角形
  let arr = [
    100.0, 100.0, 0.0, 1.0,

    100.0, 250.0, 0.0, 1.0,

    250.0, 300.0, 0.0, 1.0,

    300.0, 350.0, 0.0, 1.0,

    400.0, 400.0, 0.0, 1.0,
  ]
  //索引值数组，利用其复用顶点
  let arrIndex = [
    0,
    1,
    2, //第一个三角形
    0,
    3,
    4, //第二个三角形
  ]

  let pointPosition = new Float32Array(arr)
  let lineBuffer = webgl.createBuffer()
  webgl.bindBuffer(webgl.ARRAY_BUFFER, lineBuffer)
  webgl.bufferData(webgl.ARRAY_BUFFER, pointPosition, webgl.STATIC_DRAW)
  webgl.enableVertexAttribArray(aPosition)
  webgl.vertexAttribPointer(aPosition, 4, webgl.FLOAT, false, 4 * 4, 0 * 4)

  //创建索引缓冲区
  let indexArrData = new Uint16Array(arrIndex)
  let indexBuffer = webgl.createBuffer()
  webgl.bindBuffer(webgl.ELEMENT_ARRAY_BUFFER, indexBuffer)
  webgl.bufferData(webgl.ELEMENT_ARRAY_BUFFER, indexArrData, webgl.STATIC_DRAW)

  //获取uniform数据并赋值
  let uniformproj = webgl.getUniformLocation(webgl.program, 'proj')
  webgl.uniformMatrix4fv(uniformproj, false, projmat4)
}
```

这里 draw 函数使用新的 API，`drawElements`

```js
function draw() {
  //冲刷颜色，这里将整体涂黑
  webgl.clearColor(0.0, 0.0, 0.0, 1.0)
  webgl.clear(webgl.COLOR_BUFFER_BIT, webgl.DEPTH_BUFFER_BIT)
  //参数分别为 mode 点的个数 数据类型 偏移量
  webgl.drawElements(webgl.TRIANGLES, 6, webgl.UNSIGNED_SHORT, 0)
}
```

## 三角形旋转

```js
//将相关方法，属性包裹在对象中，防止污染
const myWebGl = {
  /**
   * @type {WebGLRenderingContext}
   */
  webgl: null,
  vertexString: `
    attribute vec3 a_position;
    void main() {
      gl_Position = vec4(a_position, 1.0);
    }
  `,
  fragmentString: `
    void main() {
      gl_FragColor = vec4(0.0, 0.0, 1.0, 1.0);
    }
  `,
  vsshader: null,
  fsshader: null,
  program: null,
  init() {
    this.creatWebGl()
    this.creatShader()
    this.creatBuffer()
    this.draw()
  },
  creatWebGl() {
    let webGlDiv = document.getElementById('weblCanvas')
    this.webgl = webGlDiv.getContext('webgl')
    this.webgl.viewport(0, 0, webGlDiv.clientWidth, webGlDiv.clientHeight)
  },
  creatShader() {
    this.vsshader = this.webgl.createShader(this.webgl.VERTEX_SHADER)
    this.fsshader = this.webgl.createShader(this.webgl.FRAGMENT_SHADER)
    this.webgl.shaderSource(this.vsshader, this.vertexString)
    this.webgl.shaderSource(this.fsshader, this.fragmentString)

    this.webgl.compileShader(this.vsshader, this.vertexString)
    this.webgl.compileShader(this.fsshader, this.fragmentString)
    this.check('compile')

    this.program = this.webgl.createProgram()
    this.webgl.attachShader(this.program, this.vsshader)
    this.webgl.attachShader(this.program, this.fsshader)

    this.webgl.linkProgram(this.program)
    this.check('link')

    this.webgl.useProgram(this.program)
  },
  creatBuffer() {
    //由于没有使用矩阵转换库，所以这里直接使用webgl投影坐标系
    let arr = [0.9, 0.8, 0.0, 0.2, 0.2, 0.0, 0.4, -0.1, 0.0]
    let floatArr = new Float32Array(arr)
    let buffer = this.webgl.createBuffer(floatArr)
    this.webgl.bindBuffer(this.webgl.ARRAY_BUFFER, buffer)
    this.webgl.bufferData(
      this.webgl.ARRAY_BUFFER,
      floatArr,
      this.webgl.STATIC_DRAW
    )
    let aPosition = this.webgl.getAttribLocation(this.program, 'a_position')
    this.webgl.vertexAttribPointer(aPosition, 3, this.webgl.FLOAT, false, 0, 0)
    this.webgl.enableVertexAttribArray(aPosition)
  },
  /**
   * @description 三角形
   */
  draw() {
    this.webgl.clearColor(0.0, 0.0, 0.0, 1.0)
    this.webgl.clear(this.webgl.COLOR_BUFFER_BIT)
    this.webgl.drawArrays(this.webgl.TRIANGLES, 0, 3)
  },
  /**
   * @description 在编译和连接测试后执行check获取status，如果有异常就打印
   * @param {"link"|"compile"} str
   */
  check(str) {
    if (str === 'compile') {
      if (
        !this.webgl.getShaderParameter(this.vsshader, this.webgl.COMPILE_STATUS)
      ) {
        console.log(this.webgl.getShaderInfoLog(this.vsshader))
      }
      if (
        !this.webgl.getShaderParameter(this.fsshader, this.webgl.COMPILE_STATUS)
      ) {
        console.log(this.webgl.getShaderInfoLog(this.fsshader))
      }
    }
    if (str === 'link') {
      if (
        !this.webgl.getProgramParameter(this.program, this.webgl.LINK_STATUS)
      ) {
        console.log(this.webgl.getShaderInfoLog(this.vsshader))
      }
      if (
        !this.webgl.getProgramParameter(this.program, this.webgl.LINK_STATUS)
      ) {
        console.log(this.webgl.getShaderInfoLog(this.fsshader))
      }
    }
    return
  },
}

document.getElementById('weblCanvas').onload = myWebGl.init()
```

做好了三角形的操作，我们进行旋转。

首先需要定义一个 uniform 变量，表明旋转角度，并进行变换（可参考 WebGL 编程指南 p91-p93）：

这里的变换为：`x' = x cosβ - y sinβ`，`y' = x sinβ + y cosβ` `z' = z ` （绕圆心逆时针旋转 β° 时）

```js
vertexString: `
    attribute vec3 a_position;
    uniform float angle;
    void main() {
      gl_Position = vec4(a_position.x * cos(angle) - a_position.y * sin(angle), a_position.x * sin(angle) + a_position.y * cos(angle), a_position.z, 1.0);
    }
  `,
```

之后赋值 uniform 变量并传入 shader：

```js
createBuffer() {
...
	let uAngle = this.webgl.getUniformLocation(this.program, 'angle')
    let angle = (90 * Math.PI) / 180
    this.webgl.uniform1f(uAngle, angle)
}
```

前后对比可以发现发生了旋转

## 实现按键控制方块移动

**前置知识**：这里使用到了 [KeyboardEvent](https://developer.mozilla.org/zh-CN/docs/Web/API/KeyboardEvent) 键盘事件和 [window.requestAnimationFrame](https://developer.mozilla.org/zh-CN/docs/Web/API/Window/requestAnimationFrame) API 实现动画

在这之前，我们先思考如何实现把上面的三角形旋转变成动态的：

```js
//在myWebGl中加入count
const myWebGl = {
count: 1
...
creatBuffer() {
    ...
    let angle = (this.count * Math.PI) / 180 //将90度替换为count
}
}

//改变onload并加入requestAnimationFrame API
document.getElementById('weblCanvas').onload = (() => {
  myWebGl.init()
  window.requestAnimationFrame(function () {
    myWebGl.count += 0.1
    myWebGl.creatBuffer()
    myWebGl.draw()
    window.requestAnimationFrame(arguments.callee)
  })
})()
```

相似的，我们只要通过声明另外一些 uniform 变量，根据这些变量来控制整体的坐标变化，同时增加按键监听事件，就可以完成相应功能了。

我们将赋值 uniform 的过程单独提出作为一个函数`bindUniform`:

```js
const myWebGl = {
  //...
  bindUniform() {},
  creatBuffer() {
    //由于没有使用矩阵转换库，所以这里直接使用webgl投影坐标系
    let arr = [0.0, 0.0, 0.0]
    let floatArr = new Float32Array(arr)
    let buffer = this.webgl.createBuffer(floatArr)
    this.webgl.bindBuffer(this.webgl.ARRAY_BUFFER, buffer)
    this.webgl.bufferData(
      this.webgl.ARRAY_BUFFER,
      floatArr,
      this.webgl.STATIC_DRAW
    )
    let aPosition = this.webgl.getAttribLocation(this.program, 'a_position')
    this.webgl.vertexAttribPointer(aPosition, 3, this.webgl.FLOAT, false, 0, 0)
    this.webgl.enableVertexAttribArray(aPosition)
    this.bindUniform()
  },
  /**
   * @description 点
   */
  draw() {
    this.webgl.clearColor(0.0, 0.0, 0.0, 1.0)
    this.webgl.clear(this.webgl.COLOR_BUFFER_BIT)
    this.webgl.drawArrays(this.webgl.POINTS, 0, 1)
  },
  //...
}

//重写顶点着色器函数：changex和changey改变点位置
myWebGl.vertexString = `
  attribute vec3 a_position;
  uniform float changex, changey;
  void main() {
    gl_Position = vec4(a_position.x + changex, a_position.y + changey, a_position.z, 1.0);
    gl_PointSize = 20.0;
  }
`
myWebGl.changex = 0
myWebGl.changey = 0

//重写bindform，将changex和changey赋值
myWebGl.bindUniform = function () {
  let x = this.webgl.getUniformLocation(this.program, 'changex')
  let y = this.webgl.getUniformLocation(this.program, 'changey')
  this.webgl.uniform1f(x, this.changex)
  this.webgl.uniform1f(y, this.changey)
}

document.getElementById('weblCanvas').onload = (() => {
  myWebGl.init()
  //加入按键事件
  document.onkeydown = ev => {
    if (ev.key == 'w') myWebGl.changey += 0.01
    if (ev.key == 's') myWebGl.changey -= 0.01
    if (ev.key == 'a') myWebGl.changex -= 0.01
    if (ev.key == 'd') myWebGl.changex += 0.01
  }
  //requestAnimationFrame API实现动画
  window.requestAnimationFrame(function () {
    myWebGl.creatBuffer()
    myWebGl.draw()
    window.requestAnimationFrame(arguments.callee)
  })
})()
```

## WebGL 纹理

**前置知识**

纹理映射：用准备好的图片，为光栅化之后的每一个片涂上合适的颜色。

<img src="https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/1653816758931.png" alt="1653816758931" style="zoom:50%;" />

我们还需要了解几个 API 概念（包括上面的 pixelStorei）：

[WebGLRenderingContext.texParameter[fi]() - Web API 接口参考 | MDN (mozilla.org)](https://developer.mozilla.org/zh-CN/docs/Web/API/WebGLRenderingContext/texParameter)

[WebGLRenderingContext.texImage2D() - Web API 接口参考 | MDN (mozilla.org)](https://developer.mozilla.org/zh-CN/docs/Web/API/WebGLRenderingContext/texImage2D)

整理之前的`myWebGl`对象，将不经常更改的程序内置，精简程序：

```js
const myWebGl = {
  /**
   * @type {WebGLRenderingContext}
   */
  webgl: null,
  vertexString: ``,
  fragmentString: ``,
  vsshader: null,
  fsshader: null,
  program: null,
  init() {
    this.creatWebGl()
    this.creatShader()
    this.creatBuffer()
    this.draw()
  },
  creatWebGl() {
    let webGlDiv = document.getElementById('weblCanvas')
    this.webgl = webGlDiv.getContext('webgl')
    this.webgl.viewport(0, 0, webGlDiv.clientWidth, webGlDiv.clientHeight)
  },
  creatShader() {
    this.vsshader = this.webgl.createShader(this.webgl.VERTEX_SHADER)
    this.fsshader = this.webgl.createShader(this.webgl.FRAGMENT_SHADER)
    this.webgl.shaderSource(this.vsshader, this.vertexString)
    this.webgl.shaderSource(this.fsshader, this.fragmentString)

    this.webgl.compileShader(this.vsshader, this.vertexString)
    this.webgl.compileShader(this.fsshader, this.fragmentString)
    this.program = this.webgl.createProgram()
    this.webgl.attachShader(this.program, this.vsshader)
    this.webgl.attachShader(this.program, this.fsshader)

    this.webgl.linkProgram(this.program)
    this.webgl.useProgram(this.program)
  },
  creatBuffer() {},
  draw() {},
}
```

这里我们主要是处理**片段着色器**和数据(buffer)部分来进行纹理映射，并通过相关的 API 画出纹理：

```js
//注意，这里使用的是从canvas坐标系映射到webgl标准坐标系

//改变片段着色器：
//这里的texture2D是一个转换颜色的函数，从而在每一个像素上都涂上颜色
myWebGl.fragmentString = `
precision mediump float;
uniform sampler2D texture;
void main() {
  vec4 color = texture2D(texture, gl_PointCoord);
  if(color.a < 0.1) discard;
  gl_FragColor = color
}
`
//处理buffer和图片
myWebGl.createBufffer = function() {
    let pointPosition = new Float32Array([
      100.0, 100.0, 0.0, 1.0, 100.0, 200.0, 0.0, 1.0, 200.0, 200.0, 0.0, 1.0,
    ])//使用canvas坐标系
    let aPosition = this.webgl.getAttribLocation(this.program, 'a_position')
    let buffer = this.webgl.createBuffer()
    this.webgl.bindBuffer(this.webgl.ARRAY_BUFFER, buffer)
    this.webgl.bufferData(
      this.webgl.ARRAY_BUFFER,
      pointPosition,
      this.webgl.STATIC_DRAW
    )
    this.webgl.vertexAttribPointer(aPosition, 4, this.webgl.FLOAT, false, 16, 0)
    this.webgl.enableVertexAttribArray(aPosition)
    this.bindUniform() //在这里绑定uniform
    //定义一个混合像素算法的函数
    this.webgl.enable(this.webgl.BLEND)
    this.webgl.blendFunc(
      this.webgl.SRC_ALPHA,
      this.webgl.ONE_MINUS_CONSTANT_ALPHA
    )

    //加载本地图片
    let textureHandle = this.webgl.createTexture()
    textureHandle.image = new Image()
    //选择一张图片作为纹理图
    textureHandle.image.src = 'fog.png'
    textureHandle.image.onload = () => {
      this.webgl.bindTexture(this.webgl.TEXTURE_2D, textureHandle)
      //对纹理进行相关处理
      this.webgl.texImage2D(
        this.webgl.TEXTURE_2D,
        0,
        this.webgl.RGBA,
        this.webgl.RGBA,
        this.webgl.UNSIGNED_BYTE,
        textureHandle.image
      )
      this.webgl.texParameteri(
        this.webgl.TEXTURE_2D,
        this.webgl.TEXTURE_MAG_FILTER,
        this.webgl.NEAREST
      )
      this.webgl.texParameteri(
        this.webgl.TEXTURE_2D,
        this.webgl.TEXTURE_MIN_FILTER,
        this.webgl.NEAREST
      )
      this.webgl.texParameteri(
        this.webgl.TEXTURE_2D,
        this.webgl.TEXTURE_WRAP_S,
        this.webgl.REPEAT
      )
      this.webgl.texParameteri(
        this.webgl.TEXTURE_2D,
        this.webgl.TEXTURE_WRAP_T,
        this.webgl.REPEAT
      )
      this.webgl.uniform1i(this.uniformTexture, 0)
      this.draw()
    }
}
myWebGl.bindUniform = function () {
  //获取uniform数据并赋值
  this.projmat4 = mat4.create()
  let webGlDiv = document.getElementById('weblCanvas')
  mat4.ortho(
    0,
    webGlDiv.clientWidth,
    webGlDiv.clientHeight,
    0,
    -1,
    1,
    this.projmat4
  )
  let uniformproj = this.webgl.getUniformLocation(this.program, 'proj')
  this.webgl.uniformMatrix4fv(uniformproj, false, this.projmat4)
}
draw() {
    webgl.clearColor(1.0, 0.0, 0.0, 1.0)
    webgl.clear(webgl.COLOR_BUFFER_BIT | webgl.DEPTH_BUFFER_BIT)
    webgl.enable(webgl.DEPTH_TEST)
    //三个点
    webgl.drawArrays(webgl.POINTS, 0, 3)
}
```

我们着重分析片段着色器的`main`函数的作用：

```C
precision mediump float;
uniform sampler2D texture;
void main() {
  vec4 color = texture2D(texture, gl_PointCoord);
  if(color.a < 0.1) discard;
  gl_FragColor = color
}
```

首先`texture2D`作为一个着色器语言的内建函数，可以用来获取对应位置的纹理的颜色值。

得到的`color`具有 r,b,b,a 四个属性，对应着 RGBA

之后判断改颜色的透明度值是否小于 0.1，小于则使用特殊的跳出语句(discard)丢弃片段。从而完成对纹理的渲染。

## WebGL 多纹理

### 绘制方法

1. 多次绘制，叠加绘制
2. 运用多个纹理单元，在一次绘制中绘制多纹理

### 绘制过程

激活对应的纹理(activeTexture) -> 绑定纹理 -> 使用传入着色器的相关数据，利用算法进行运算并且着色

这里用到了新的 API：

[WebGLRenderingContext.activeTexture() - Web API 接口参考 | MDN (mozilla.org)](https://developer.mozilla.org/zh-CN/docs/Web/API/WebGLRenderingContext/activeTexture)

[WebGLRenderingContext.bindTexture() - Web API 接口参考 | MDN (mozilla.org)](https://developer.mozilla.org/zh-CN/docs/Web/API/WebGLRenderingContext/bindTexture)

### 纹理坐标系系统

<img src="https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/1653984796092.png" alt="1653984796092" style="zoom:50%;" />

和 canvas 坐标系作比较，图像坐标系是与 canvas 坐标系相同，但是 WebGL 纹理坐标系的 y 轴与 canvas 坐标系互为相反数。

底部的函数：[webgl.pixelStorei ](https://developer.mozilla.org/zh-CN/docs/Web/API/WebGLRenderingContext/pixelStorei) 是用来处理图像预处理的函数，其中的`webgl.UNPACK_FLIP_Y_WEBGL`用于翻转 y 轴，将图像坐标转换成 webgl 纹理坐标。

### 实战

首先我们使用多个绘制单元进行绘制的方法。同时激活多个纹理单元并且绑定。

使用以下两张图片作为纹理：

![fog](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/fog.png)

<img src="https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/bac.jpg" alt="bac" style="zoom:10%;" />

编辑着色器部分，以及 buffer 和 draw 程序：

```js
myWebGl.vertexString = `
attribute vec4 a_position;
uniform mat4 proj;
attribute vec2 outUV;
varying vec2 inUV;
void main(void) {
  gl_Position = proj * a_position;
  inUV = outUV;
}
  `
myWebGl.fragmentString = `
precision mediump float;
uniform sampler2D texture;
uniform sampler2D texture1;
uniform float anim;
varying vec2 inUV;
void main() {
  vec4 color1 = texture2D(texture, inUV);
  vec4 color2 = texture2D(texture1, vec2(inUV.x + anim, inUV.y));
  gl_FragColor = color1 + color2;
}
  `
myWebGl.initTexture = function (str) {
  let textureHandle = this.webgl.createTexture()
  textureHandle.image = new Image()
  textureHandle.image.src = str
  textureHandle.image.onload = () => {
    this.webgl.bindTexture(this.webgl.TEXTURE_2D, textureHandle)
    this.webgl.texImage2D(
      this.webgl.TEXTURE_2D,
      0,
      this.webgl.RGBA,
      this.webgl.RGBA,
      this.webgl.UNSIGNED_BYTE,
      textureHandle.image
    )
    this.webgl.texParameteri(
      this.webgl.TEXTURE_2D,
      this.webgl.TEXTURE_MAG_FILTER,
      this.webgl.LINEAR
    )
    this.webgl.texParameteri(
      this.webgl.TEXTURE_2D,
      this.webgl.TEXTURE_MIN_FILTER,
      this.webgl.LINEAR
    )
    this.webgl.texParameteri(
      this.webgl.TEXTURE_2D,
      this.webgl.TEXTURE_WRAP_S,
      this.webgl.CLAMP_TO_EDGE
    )
    this.webgl.texParameteri(
      this.webgl.TEXTURE_2D,
      this.webgl.TEXTURE_WRAP_T,
      this.webgl.CLAMP_TO_EDGE
    )
  }
  return textureHandle
}

myWebGl.creatBuffer = function () {
  //四组坐标的前四个数字代表webgl标准坐标系坐标，后两个数字代表对应的webgl纹理坐标系坐标，根据上面的坐标系图可以清楚的得知其转换关系
  const arr = [
    0, 0, 0.0, 1, 0, 0,

    0, 500, 0, 1, 0, 1,

    500, 500, 0, 1, 1, 1,

    500, 0, 0, 1, 1, 0,
  ]
  //建立索引值数组，为了在draw方法中使用drawElements函数，这里为了绘制一个正方形，其实就是绘制链两个三角形
  const arrIndex = [
    0,
    1,
    2, //第一个三角形

    2,
    0,
    3, //第二个三角形
  ]
  //配置顶点缓冲区
  let pointPosition = new Float32Array(arr)
  let aPosition = this.webgl.getAttribLocation(this.program, 'a_position')
  let lineBuffer = this.webgl.createBuffer()
  this.webgl.bindBuffer(this.webgl.ARRAY_BUFFER, lineBuffer)
  this.webgl.bufferData(
    this.webgl.ARRAY_BUFFER,
    pointPosition,
    this.webgl.STATIC_DRAW
  )
  this.webgl.enableVertexAttribArray(aPosition)
  this.webgl.vertexAttribPointer(
    aPosition,
    4,
    this.webgl.FLOAT,
    false,
    6 * 4,
    0 * 4
  )
  //创建索引缓冲区
  let indexArrData = new Uint8Array(arrIndex)
  let indexBuffer = this.webgl.createBuffer()
  this.webgl.bindBuffer(this.webgl.ELEMENT_ARRAY_BUFFER, indexBuffer)
  this.webgl.bufferData(
    this.webgl.ELEMENT_ARRAY_BUFFER,
    indexArrData,
    this.webgl.STATIC_DRAW
  )
  //获取uniform数据并赋值
  this.projmat4 = mat4.create()
  let webGlDiv = document.getElementById('weblCanvas')
  mat4.ortho(
    0,
    webGlDiv.clientWidth,
    webGlDiv.clientHeight,
    0,
    -1,
    1,
    this.projmat4
  )
  let uniformproj = this.webgl.getUniformLocation(this.program, 'proj')
  this.webgl.uniformMatrix4fv(uniformproj, false, this.projmat4)
  //outUV 代表UV坐标系，即纹理坐标系
  const attribOutUV = this.webgl.getAttribLocation(this.program, 'outUV')
  this.webgl.enableVertexAttribArray(attribOutUV)
  this.webgl.vertexAttribPointer(
    attribOutUV,
    2,
    this.webgl.FLOAT,
    false,
    6 * 4,
    4 * 4
  ) //这里最后一个参数为偏移量，设置成 4 * 4 表明偏移4个下标
  //配置纹理数据用于shader
  this.uniformTexture = this.webgl.getUniformLocation(this.program, 'texture')
  this.uniformTexture1 = this.webgl.getUniformLocation(this.program, 'texture1')
  this.texture = this.initTexture('bac.jpg')
  this.texture1 = this.initTexture('fog.png')
}

myWebGl.draw = function () {
  this.webgl.clearColor(0.0, 1.0, 0.0, 1.0)
  this.webgl.clear(this.webgl.COLOR_BUFFER_BIT | this.webgl.DEPTH_BUFFER_BIT)
  this.webgl.enable(this.webgl.DEPTH_TEST)

  //设置anim变量用作纹理动画
  let uniformAnim = this.webgl.getUniformLocation(this.program, 'anim')
  this.count = isNaN(this.count) ? 0 : (this.count + 0.01) % 0.7
  console.log(this.count)
  this.webgl.uniform1f(uniformAnim, this.count)
  //激活两个纹理单元
  this.webgl.activeTexture(this.webgl.TEXTURE0)
  this.webgl.bindTexture(this.webgl.TEXTURE_2D, this.texture)
  this.webgl.uniform1i(this.uniformTexture, 0)
  this.webgl.activeTexture(this.webgl.TEXTURE1)
  this.webgl.bindTexture(this.webgl.TEXTURE_2D, this.texture1)
  this.webgl.uniform1i(this.uniformTexture1, 1)

  this.webgl.drawElements(this.webgl.TRIANGLES, 6, this.webgl.UNSIGNED_BYTE, 0)
}

//为了实现动画效果，使用requestAnimationFrame
document.getElementById('weblCanvas').onload = (() => {
  myWebGl.init()
  window.requestAnimationFrame(function () {
    myWebGl.draw()
    window.requestAnimationFrame(arguments.callee)
  })
})()
```

<img src="https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/202261gif1.gif" alt="202261gif1" style="zoom:67%;" />

分析着色器部分：

```c
//顶点着色器
attribute vec4 a_position;
uniform mat4 proj;
attribute vec2 outUV;
varying vec2 inUV;
void main(void) {
  gl_Position = proj * a_position;
  inUV = outUV; //将纹理坐标传递到inUV
}

//片段着色器
precision mediump float;
uniform sampler2D texture;
uniform sampler2D texture1;
uniform float anim;
varying vec2 inUV;
void main() {
  //texture2D内置函数根据纹理图片和纹理坐标，返回相图片对应位置的颜色
  vec4 color1 = texture2D(texture, inUV);
  //这里的anim作为x轴的偏移量，用作纹理的偏移，从而制造动画效果
  vec4 color2 = texture2D(texture1, vec2(inUV.x + anim, inUV.y));
  //颜色叠加，也就是把纹理叠加
  gl_FragColor = color1 + color2;
}

```

分析图片`onload`后，对图片进行映射处理的相关 API：

```js
this.webgl.bindTexture(this.webgl.TEXTURE_2D, textureHandle)
this.webgl.texImage2D(
  this.webgl.TEXTURE_2D,
  0,
  this.webgl.RGBA,
  this.webgl.RGBA,
  this.webgl.UNSIGNED_BYTE,
  textureHandle.image
)
this.webgl.texParameteri(
  this.webgl.TEXTURE_2D,
  this.webgl.TEXTURE_MAG_FILTER,
  this.webgl.LINEAR
)
this.webgl.texParameteri(
  this.webgl.TEXTURE_2D,
  this.webgl.TEXTURE_MIN_FILTER,
  this.webgl.LINEAR
)
this.webgl.texParameteri(
  this.webgl.TEXTURE_2D,
  this.webgl.TEXTURE_WRAP_S,
  this.webgl.CLAMP_TO_EDGE
)
this.webgl.texParameteri(
  this.webgl.TEXTURE_2D,
  this.webgl.TEXTURE_WRAP_T,
  this.webgl.CLAMP_TO_EDGE
)
```

## WebGL 动画变换

在之前的案例中，其实已经实现了一些运动效果，是利用的`requestanimationframe`API,让 webgl 在每一帧内渲染一次（ 回调函数执行次数通常是每秒 60 次 ）。而在每次渲染之前，通过改变一些坐标的偏移量，并传入片段着色器来在新的位置上渲染图形从而达到动画效果。

### 变换矩阵

当我们进行简单的坐标移动时，采用偏移量或者简单计算都是可行的。如果遇到复杂的移动如旋转等，就可以借助**变换矩阵**来完成这项工作。

变化矩阵的用法，可以参考 [计算机图形学一：基础变换矩阵总结(缩放，旋转，位移) - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/144323332)

所以，我们就可以使用`n*n`的矩阵来完成对一个 n 维坐标的变换。

我们利用变换矩阵，来完成一个移动案例：

```js
//对封装的myWebGl进行shader，buffer，和渲染方法的更改
myWebGl.vertexString = `
  attribute vec4 a_position;
  uniform mat4 u_formMatrix;
  void main(void) {
    gl_Position = u_formMatrix * a_position;
  }
    `
myWebGl.fragmentString = `
  precision mediump float;
  void main() {
    gl_FragColor = vec4(1.0,0.0,0.0,1.0);
  }
    `

myWebGl.creatBuffer = function () {
  //四组坐标的钱四个数字代表webgl标准坐标系坐标，后两个数字代表对应的webgl纹理坐标系坐标，根据上面的坐标系图可以清楚的得知其转换关系
  const arr = [
    0, 0, 0.0, 1, 0, 0,

    0, 0.5, 0, 1, 0, 1,

    0.5, 0.5, 0, 1, 1, 1,

    0.5, 0, 0, 1, 1, 0,
  ]
  //建立索引值数组，为了在draw方法中使用drawElements函数，这里为了绘制一个正方形，其实就是绘制链两个三角形
  const arrIndex = [
    0,
    1,
    2, //第一个三角形

    2,
    0,
    3, //第二个三角形
  ]
  let offset = 0.1
  //定义变换矩阵 由于webgl是按照列储存的，所以这里的矩阵其实是变换矩阵的转置矩阵，所以这里的offset是作用在x上的
  const matrixArr = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, offset, 0, 0, 1]
  //配置顶点缓冲区
  let pointPosition = new Float32Array(arr)
  let aPosition = this.webgl.getAttribLocation(this.program, 'a_position')
  let lineBuffer = this.webgl.createBuffer()
  this.webgl.bindBuffer(this.webgl.ARRAY_BUFFER, lineBuffer)
  this.webgl.bufferData(
    this.webgl.ARRAY_BUFFER,
    pointPosition,
    this.webgl.STATIC_DRAW
  )
  this.webgl.enableVertexAttribArray(aPosition)
  this.webgl.vertexAttribPointer(
    aPosition,
    4,
    this.webgl.FLOAT,
    false,
    6 * 4,
    0 * 4
  )
  //创建索引缓冲区
  let indexArrData = new Uint8Array(arrIndex)
  let indexBuffer = this.webgl.createBuffer()
  this.webgl.bindBuffer(this.webgl.ELEMENT_ARRAY_BUFFER, indexBuffer)
  this.webgl.bufferData(
    this.webgl.ELEMENT_ARRAY_BUFFER,
    indexArrData,
    this.webgl.STATIC_DRAW
  )
  //绑定变换矩阵
  let matrixData = new Float32Array(matrixArr)
  let uniformMatrix = this.webgl.getUniformLocation(
    this.program,
    'u_formMatrix'
  )
  this.webgl.uniformMatrix4fv(uniformMatrix, false, matrixData)
}

myWebGl.draw = function () {
  this.webgl.clearColor(0.0, 1.0, 0.0, 1.0)
  this.webgl.clear(this.webgl.COLOR_BUFFER_BIT | this.webgl.DEPTH_BUFFER_BIT)
  this.webgl.enable(this.webgl.DEPTH_TEST)

  this.webgl.drawElements(this.webgl.TRIANGLES, 6, this.webgl.UNSIGNED_BYTE, 0)
}

document.getElementById('weblCanvas').onload = (() => {
  myWebGl.init()
  window.requestAnimationFrame(function () {
    myWebGl.draw()
    window.requestAnimationFrame(arguments.callee)
  })
})()
```

通过改变`offset`变量，就可以控制正方形的移动。

同时，我们也可以将`offset`绑定在`myWebGl`对象上，通过在函数内使用`this.offset`引用。这样，我们就可以在`requestAnimationFrame`回调内改变`offset`变量值，从而改变变换矩阵。然后重新执行`createBuffer`和`draw`函数，从而实现动画效果。

<img src="https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/202262gif1.gif" alt="202262gif1" style="zoom:50%;" />

同样的，采用其他的变换矩阵也可以实现伸缩，旋转等效果或者一些复合变换效果。

例如缩放的变换矩阵可以如下：

```js
0.5, 0, 0, 0
0, 0.5, 0, 0
0, 0, 1.0, 0
0, 0, 0, 1.0
```

在实际使用中，根据不同的变换效果，很多 webgl 矩阵库将这些变换矩阵封装成了方法直接使用。

## WebGL 三维世界

三维物体其实是由很多个二维三角形组成的：

![1654158511702](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/1654158511702.png)



## 视点与视线

想象一个照相机，作为照相的人，**视点**就是照相机的镜头的中心点，**目标点**就是照相的目标物体，也是最终的成像。**视线**是视点和目标点的连线。

<img src="https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/1656689718808.png" style="zoom:50%;" />

### 实战部分：

这里，为了解决越来越多的代码和`main.js`对`gl-matrix.js`的依赖，我们引入`rollup`对程序进行打包：

（注：gl-matrix就是glMatrix官网下载的较新的版本）

首先，我们使用终端安装rollup：`npm i rollup` 以及 npm i rollup-plugin-commonjs 前者是rollup本身，后者是rollup的commonjs插件， 使得rollup可以翻译commonjs的模块。

在`package.json`文件中添加npm scripts命令"dev": "rollup -c -i main.js -o dist/index.js --watch"，在命令行中输入`npm run dev`来进行打包，并具有热更新功能。 

我们配置一个rollup配置文件：

```js
import commonjs from 'rollup-plugin-commonjs'
export default {
  input: './main.js',
  output: {
    file: './dist/index.js',
    format: 'iife',
  },
  plugins: [commonjs()],
}
```

写一个html：

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    <canvas id="weblCanvas" width="640" height="480">
      你的浏览器似乎不支持或者禁用了HTML5 <code>&lt;canvas&gt;</code> 元素.
    </canvas>
    <script type="text/javascript" src="./dist/index.js"></script>
  </body>
</html>
```

然后载入如下的main.js文件：

```js
const mat4 = require('./gl-matrix').mat4

const myWebGl = {
  /**
   * @type {WebGLRenderingContext}
   */
  webgl: null,
  vertexString: ``,
  fragmentString: ``,
  vsshader: null,
  fsshader: null,
  program: null,
  init() {
    this.creatWebGl()
    this.creatShader()
    this.creatBuffer()
    this.draw()
  },
  creatWebGl() {
    let webGlDiv = document.getElementById('weblCanvas')
    this.webgl = webGlDiv.getContext('webgl')
    this.webgl.viewport(0, 0, webGlDiv.clientWidth, webGlDiv.clientHeight)
  },
  creatShader() {
    this.vsshader = this.webgl.createShader(this.webgl.VERTEX_SHADER)
    this.fsshader = this.webgl.createShader(this.webgl.FRAGMENT_SHADER)
    this.webgl.shaderSource(this.vsshader, this.vertexString)
    this.webgl.shaderSource(this.fsshader, this.fragmentString)

    this.webgl.compileShader(this.vsshader, this.vertexString)
    this.webgl.compileShader(this.fsshader, this.fragmentString)
    this.program = this.webgl.createProgram()
    this.webgl.attachShader(this.program, this.vsshader)
    this.webgl.attachShader(this.program, this.fsshader)

    this.webgl.linkProgram(this.program)
    this.webgl.useProgram(this.program)
  },
  creatBuffer() {},
  draw() {},
}

//这里引入颜色变量来根据顶点渲染不同的颜色
myWebGl.vertexString = `
attribute vec4 a_position;
uniform mat4 u_formMatrix;
attribute vec4 a_color;
varying vec4 color;
void main(void) {
    gl_Position = u_formMatrix * a_position;
    color = a_color;
}
    `
myWebGl.fragmentString = `
precision mediump float;
varying vec4 color; 
void main() {
    gl_FragColor = color;
}
`

myWebGl.creatBuffer = function () {
  let arr = [
    0.0, 0.5, -0.4, 1, 0.4, 1.0, 0.4, 1,  //每一行前四个代表一个顶点，后四个代表颜色
    -0.5, -0.5, -0.4, 1, 0.4, 1.0, 0.4, 1,
    0.5, -0.5, -0.4, 1, 0.4, 1.0, 0.4, 1,

    0.5, 0.4, -0.2, 1, 1.0, 1.0, 0.4, 1, 
    -0.5, 0.4, -0.2, 1, 1.0, 1.0, 0.4, 1,
    0.0, -0.6, -0.2, 1, 1.0, 1.0, 0.4, 1,

    0.0, 0.5, 0.0, 1, 0.4, 0.4, 1.0, 1, 
    -0.5, -0.5, 0.0, 1, 0.4, 0.4, 1.0, 1,
    0.5, -0.5, 0.0, 1, 0.4, 0.4, 1.0, 1,

    // 0.0, 0.6, -0.4, 1,    0.4, 1.0, 1,1, // The back green one
    // -0.5, -0.4, -0.4,  1, 0.4, 1.0, 1,1,
    // 0.5, -0.4, -0.4, 1,  0.4, 1.0,1,1,

    // 0.5, 0.4, -0.2,  1, 1.0, 1.0, 0.4,1, // The middle yellow one
    // -0.5, 0.4, -0.2, 1,  1.0, 1.0, 0.4,1,
    // 0.0, -0.6, -0.2,1,   1.0, 1.0, 0.4,1,

    // 0.0, 0.5, 0.0,  1,   0.4, 0.4, 1.0,1, // The front blue one
    // -0.5, -0.5, 0.0,1,  0.4, 0.4, 1.0,1,
    // 0.5, -0.5, 0.0, 1,  0.4, 0.4, 1.0,1,
  ]

  let pointPosition = new Float32Array(arr)
  let aPsotion = this.webgl.getAttribLocation(myWebGl.program, 'a_position')
  let triangleBuffer = this.webgl.createBuffer()
  this.webgl.bindBuffer(this.webgl.ARRAY_BUFFER, triangleBuffer)
  this.webgl.bufferData(
    this.webgl.ARRAY_BUFFER,
    pointPosition,
    this.webgl.STATIC_DRAW
  )
  this.webgl.enableVertexAttribArray(aPsotion)
  this.webgl.vertexAttribPointer(aPsotion, 4, this.webgl.FLOAT, false, 8 * 4, 0)
  let aColor = this.webgl.getAttribLocation(myWebGl.program, 'a_color')
  this.webgl.enableVertexAttribArray(aColor)
  this.webgl.vertexAttribPointer(
    aColor,
    4,
    this.webgl.FLOAT,
    false,
    8 * 4,
    4 * 4
  )

  let modelView = mat4.create() //创建一个空矩阵
  mat4.identity(modelView)//将空矩阵单元化
  modelView = mat4.lookAt(modelView, [0.2, 0.2, 0.2], [0, 0, 0], [0, 1, 0])//创建一个视图矩阵，参数分别为，输出，视点，目标点，上方向

  let uniformMatrix1 = this.webgl.getUniformLocation(
    myWebGl.program,
    'u_formMatrix'
  )
  this.webgl.uniformMatrix4fv(uniformMatrix1, false, modelView)
}

myWebGl.draw = function () {
  this.webgl.clearColor(0.0, 1.0, 0.0, 1.0)
  this.webgl.clear(this.webgl.COLOR_BUFFER_BIT | this.webgl.DEPTH_BUFFER_BIT)
  this.webgl.drawArrays(this.webgl.TRIANGLES, 0, 9)
}

document.getElementById('weblCanvas').onload = (() => {
  myWebGl.init()
})()
```

最终得到：

<img src="https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/Snipaste_2022-07-02_15-23-05.png" style="zoom:50%;" />

再尝试将creatBuffer中的数组的前三组注释，释放后三组，可以得到：

<img src="https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/Snipaste_2022-07-02_15-22-36.png" style="zoom:50%;" />

这样的差距是由于我们的顶点位置的变化导致的。

同时我们可以改变这个`mat4.lookAt`函数，来改变视点，从而获得新的图像：

```js
modelView = mat4.lookAt(modelView, [0.2, 0.2, 0.2], [0, 0, 0], [0, 1, 0])
```

<img src="https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/Snipaste_2022-07-02_15-45-29.png" style="zoom:50%;" />

这里的核心就在于**视图矩阵的构建**：

```js
let modelView = mat4.create() //创建一个空矩阵
  mat4.identity(modelView)//将空矩阵单元化
  modelView = mat4.lookAt(modelView, [0.2, 0.2, 0.2], [0, 0, 0], [0, 1, 0])//创建一个模型矩阵，参数分别为，输出，视点，目标点，上方向
```

为了更加明显的感受视点的变化带来的最终图像的不同，我们可以将构建视图矩阵的视点参数通过`requestAnimationFrame`改变，来动态观察效果。或者通过监听键盘监听函数，来改变参数，从而主动改变视图矩阵。

同时，我们也可以使用视图矩阵(通过mat4.rorate方法生成的矩阵，可以将矩阵旋转和视图矩阵相乘，来得到新的矩阵同时受视点和视图矩阵的影响。

例如：

```js
myWebGl.angleX = 0
myWebGl.angleY = 0
myWebGl.creatBuffer = function () {
  let arr = [
    0.0, 0.5, -0.4, 1, 0.4, 1.0, 0.4, 1,  //每一行前四个代表一个顶点，后四个代表颜色
    -0.5, -0.5, -0.4, 1, 0.4, 1.0, 0.4, 1,
    0.5, -0.5, -0.4, 1, 0.4, 1.0, 0.4, 1,

    0.5, 0.4, -0.2, 1, 1.0, 1.0, 0.4, 1, 
    -0.5, 0.4, -0.2, 1, 1.0, 1.0, 0.4, 1,
    0.0, -0.6, -0.2, 1, 1.0, 1.0, 0.4, 1,

    0.0, 0.5, 0.0, 1, 0.4, 0.4, 1.0, 1, 
    -0.5, -0.5, 0.0, 1, 0.4, 0.4, 1.0, 1,
    0.5, -0.5, 0.0, 1, 0.4, 0.4, 1.0, 1,
  ]

  let pointPosition = new Float32Array(arr)
  let aPsotion = this.webgl.getAttribLocation(myWebGl.program, 'a_position')
  let triangleBuffer = this.webgl.createBuffer()
  this.webgl.bindBuffer(this.webgl.ARRAY_BUFFER, triangleBuffer)
  this.webgl.bufferData(
    this.webgl.ARRAY_BUFFER,
    pointPosition,
    this.webgl.STATIC_DRAW
  )
  this.webgl.enableVertexAttribArray(aPsotion)
  this.webgl.vertexAttribPointer(aPsotion, 4, this.webgl.FLOAT, false, 8 * 4, 0)
  let aColor = this.webgl.getAttribLocation(myWebGl.program, 'a_color')
  this.webgl.enableVertexAttribArray(aColor)
  this.webgl.vertexAttribPointer(aColor, 4, this.webgl.FLOAT, false, 8 * 4, 4 * 4)
  
  //创建一个空矩阵作为模型矩阵
  let ModelMatrix = mat4.create();
  mat4.identity(ModelMatrix);
  let angle = Math.PI / 180 * 50; //旋转50度
  mat4.rotate(ModelMatrix, ModelMatrix, angle, [0, 0, 1])//旋转模型
  //构建一个空矩阵作为视图矩阵
  let ViewMatrix = mat4.create() 
  mat4.identity(ViewMatrix)//将空矩阵单元化
  mat4.lookAt(ViewMatrix, [this.angleX, this.angleY, 0.2], [0, 0, 0], [0, 1, 0])//创建一个视点矩阵，参数分别为，输出，视点，目标点，上方向

  //构造一个模型矩阵
  let mvMatrix = mat4.create();
  mat4.multiply(mvMatrix, ViewMatrix, ModelMatrix)

  let uniformMatrix1 = this.webgl.getUniformLocation(
    myWebGl.program,
    'u_formMatrix'
  )
  this.webgl.uniformMatrix4fv(uniformMatrix1, false, mvMatrix)
}

document.onkeydown = ev => {
  switch (ev.key) {
    case 'w':
      myWebGl.angleY += 0.01   
      break;
    case 's':
      myWebGl.angleY -= 0.01  
      break;
    case 'a':
      myWebGl.angleX -= 0.01
      console.log(myWebGl.angleX)  
      break;
    case 'd': 
      myWebGl.angleX += 0.01 
      break;
  }
}

document.getElementById('weblCanvas').onload = (() => {
  myWebGl.init()
  const animate = function() {
    myWebGl.creatBuffer()
    myWebGl.draw()
    window.requestAnimationFrame(animate)
  }
  animate()
})()
```

着色器和draw函数均不变，最终可以得到(wsad控制视点上下左右)：

<img src="https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20220717gif.gif" style="zoom:50%;" />



## 可视域

我们发现上面的三角形在动起来时，会出现三角形边缘被切割的现象导致不完整。这就是因为可视域。

webGL中可视域被封装成一个正方体，在正方体外的顶点或片段不进行渲染，在视觉效果上，我们会看不到对应的区域。

以正射投影为例：

<img src="https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/Snipaste_2022-07-03_23-28-56.png" style="zoom:50%;" />



## 投影矩阵

上面说过了正射投影，我们还需要了解一下其他的投影矩阵，例如透视透视投影：

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/Snipaste_2022-07-17_22-06-11.png)

在透视投影下，产生的三维场景更加有深度感，更加自然，因为我们平时观察真实世界用的也是透视投影。

我们建立一个由透视投影生成的webgl图像：

```js
myWebGl.vertexString = `
attribute vec4 a_position;
uniform mat4 u_formMatrix;
uniform mat4 proj;
attribute vec4 a_color;
varying vec4 color;
void main(void){
    gl_Position =   u_formMatrix * a_position;
    color = a_color;
}
    `
myWebGl.fragmentString = `
precision mediump float;
varying vec4 color; 
void main() {
    gl_FragColor = color;
}
`
myWebGl.angle = 90
myWebGl.creatBuffer = function () {
  let webGlDiv = document.getElementById('weblCanvas')  
  let ProjMatrix  = mat4.create()
  mat4.identity(ProjMatrix)
  //生成一个投影矩阵，对应的参数分别是，输出的矩阵，投影矩阵中视线的夹角，可是空间的长宽比，near和far
  mat4.perspective(ProjMatrix, myWebGl.angle * Math.PI / 180, webGlDiv.clientWidth/webGlDiv.clientHeight,1,100)  
  
  let arr = [
    0.0, 70, -40, 1,      1, 0,  0, 1,
    -50, -30, -40, 1,     1, 0,  0, 1, // 红色
    50, -30, -40, 1,      1, 0,  0, 1,

    50, 40, -20, 1, 1.0, 1.0,  0.4, 1,
    -50, 40, -20, 1, 1.0, 1.0,  0.4, 1,
    0.0, -60,-20, 1, 1.0, 1.0,  0.4, 1,// 黄色

    0.0, 50, 0.0, 1,  0.4,  0.4, 1.0, 1,
    -50, -50, 0.0, 1,  0.4,  0.4, 1.0, 1,
    50, -50, 0.0, 1,  0.4,  0.4, 1.0, 1, // 蓝色
  ]

  let pointPosition = new Float32Array(arr)
  let aPsotion = this.webgl.getAttribLocation(myWebGl.program, 'a_position')
  let triangleBuffer = this.webgl.createBuffer()
  this.webgl.bindBuffer(this.webgl.ARRAY_BUFFER, triangleBuffer)
  this.webgl.bufferData(
    this.webgl.ARRAY_BUFFER,
    pointPosition,
    this.webgl.STATIC_DRAW
  )
  this.webgl.enableVertexAttribArray(aPsotion)
  this.webgl.vertexAttribPointer(aPsotion, 4, this.webgl.FLOAT, false, 8 * 4, 0)
  let aColor = this.webgl.getAttribLocation(myWebGl.program, 'a_color')
  this.webgl.enableVertexAttribArray(aColor)
  this.webgl.vertexAttribPointer(
    aColor,
    4,
    this.webgl.FLOAT,
    false,
    8 * 4,
    4 * 4
  )
  
  let uniformMatrix1 = this.webgl.getUniformLocation(
    myWebGl.program,
    'u_formMatrix'
  )
  this.webgl.uniformMatrix4fv(uniformMatrix1, false, ProjMatrix)
}

myWebGl.draw = function () {
  this.webgl.clearColor(0.0, 1.0, 0.0, 1.0)
  this.webgl.clear(this.webgl.COLOR_BUFFER_BIT | this.webgl.DEPTH_BUFFER_BIT)
  this.webgl.drawArrays(this.webgl.TRIANGLES, 0, 9)
}

document.onkeydown = ev => {
  switch (ev.key) {
    case 'w':
      myWebGl.angle += 1
      console.log(angle)
      break
    case 's':
      myWebGl.angle -= 1
      console.log(angle)
      break
  }
}

document.getElementById('weblCanvas').onload = (() => {
  myWebGl.init()
  const animate = function () {
    myWebGl.creatBuffer()
    myWebGl.draw()
    window.requestAnimationFrame(animate)
  }
  animate()
})()
```

其中最重要的就是`mat4.perspective`生成投影矩阵这个函数。

同时，我们将模型矩阵（M），视图矩阵（V），投影矩阵（P) 三位一体，形成mvp矩阵，就可以更加灵活的展现三维视图了。

我们可以根据前两个样例的代码，简单的修改一下`createBuffer`里的代码：

```js
myWebGl.angleX = 0
myWebGl.angleY = 0
myWebGl.angle = 120
myWebGl.creatBuffer = function () {
  let webGlDiv = document.getElementById('weblCanvas')  
  let ProjMatrix  = mat4.create()
  mat4.identity(ProjMatrix)
  //生成一个投影矩阵，对应的参数分别是，输出的矩阵，投影矩阵中视线的夹角，可是空间的长宽比，near和far
  mat4.perspective(ProjMatrix, myWebGl.angle * Math.PI / 180, webGlDiv.clientWidth/webGlDiv.clientHeight,1,100)  
  
  //创建一个空矩阵作为模型矩阵
  let ModelMatrix = mat4.create();
  mat4.identity(ModelMatrix);
  let angle = Math.PI / 180 * 50; //旋转50度
  mat4.rotate(ModelMatrix, ModelMatrix, angle, [0, 0, 1])//旋转模型
  //构建一个空矩阵作为视图矩阵
  let ViewMatrix = mat4.create() 
  mat4.identity(ViewMatrix)//将空矩阵单元化
  mat4.lookAt(ViewMatrix, [this.angleX, this.angleY, 0.2], [0, 0, 0], [0, 1, 0])//创建一个视点矩阵，参数分别为，输出，视点，目标点，上方向
  let mvMatrix =  mat4.create();
  mat4.multiply(mvMatrix,ViewMatrix,ModelMatrix);
  let mvpMatrix = mat4.create();
  mat4.multiply(mvpMatrix,ProjMatrix,mvMatrix);
  
  let arr = [
    0.0, 70, -40, 1,      1, 0,  0, 1,
    -50, -30, -40, 1,     1, 0,  0, 1, // 红色
    50, -30, -40, 1,      1, 0,  0, 1,

    50, 40, -20, 1, 1.0, 1.0,  0.4, 1,
    -50, 40, -20, 1, 1.0, 1.0,  0.4, 1,
    0.0, -60,-20, 1, 1.0, 1.0,  0.4, 1,// 黄色

    0.0, 50, 0.0, 1,  0.4,  0.4, 1.0, 1,
    -50, -50, 0.0, 1,  0.4,  0.4, 1.0, 1,
    50, -50, 0.0, 1,  0.4,  0.4, 1.0, 1, // 蓝色
  ]

  let pointPosition = new Float32Array(arr)
  let aPsotion = this.webgl.getAttribLocation(myWebGl.program, 'a_position')
  let triangleBuffer = this.webgl.createBuffer()
  this.webgl.bindBuffer(this.webgl.ARRAY_BUFFER, triangleBuffer)
  this.webgl.bufferData(
    this.webgl.ARRAY_BUFFER,
    pointPosition,
    this.webgl.STATIC_DRAW
  )
  this.webgl.enableVertexAttribArray(aPsotion)
  this.webgl.vertexAttribPointer(aPsotion, 4, this.webgl.FLOAT, false, 8 * 4, 0)
  let aColor = this.webgl.getAttribLocation(myWebGl.program, 'a_color')
  this.webgl.enableVertexAttribArray(aColor)
  this.webgl.vertexAttribPointer(
    aColor,
    4,
    this.webgl.FLOAT,
    false,
    8 * 4,
    4 * 4
  )
  
  let uniformMatrix1 = this.webgl.getUniformLocation(
    myWebGl.program,
    'u_formMatrix'
  )
  this.webgl.uniformMatrix4fv(uniformMatrix1, false, mvpMatrix)
}

myWebGl.draw = function () {
  this.webgl.clearColor(0.0, 1.0, 0.0, 1.0)
  this.webgl.clear(this.webgl.COLOR_BUFFER_BIT | this.webgl.DEPTH_BUFFER_BIT)
  this.webgl.drawArrays(this.webgl.TRIANGLES, 0, 9)
}

document.onkeydown = ev => {
  switch (ev.key) {
    case 'z':
      myWebGl.angle += 1
      console.log(myWebGl.angle)
      break
    case 'x':
      myWebGl.angle -= 1
      console.log(myWebGl.angle)
      break
    case 'w':
      myWebGl.angleY += 0.01
      console.log(myWebGl.angleY)   
      break;
    case 's':
      myWebGl.angleY -= 0.01 
      console.log(myWebGl.angleY) 
      break;
    case 'a':
      myWebGl.angleX -= 0.01
      console.log(myWebGl.angleX)  
      break;
    case 'd': 
      myWebGl.angleX += 0.01
      console.log(myWebGl.angleX) 
      break;
  }
}
```

最终效果：

<img src="https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/2022717gif2.gif" style="zoom: 50%;" />



## 深度缓冲区

深度缓冲区用于记录每个像素的深度值，通过深度缓冲区，我们可以进行深度测试，从而确定像素的渲染关系，保证渲染正确。深度其实就是该像素点在三维世界中距离摄像机的距离，深度缓存中存储着每个像素点的深度值，深度值越大则距离摄像机越远。

**为什么使用深度缓冲区呢？**

由于webgl默认采用的是**画家算法**来进行绘制和渲染，所以当我们后加载的图形的深度是更大时，根据画家算法，还是会把后画的图形覆盖在前面的图形上。为了更加直观的说明问题，可以通过视点与视线的最后一个实例，改变三个三角形图形数组中的位置，对比不同来理解画家算法带来的对图像渲染的错误处理。

### 深度冲突

深度冲突是指两个深度相同的图形重叠时，由于计算机不知道该绘制哪个图形，所以产生了冲突。解决这个冲突的方法是给定一个偏移值，从而让两个图形深度有稍微的不同，从而解决冲突。



### 开启深度缓冲区

开启深度缓冲区只需要在draw函数中启用深度测试即可：

```js
myWebGl.draw = function () {
  this.webgl.clearColor(0.0, 1.0, 0.0, 1.0)
  this.webgl.clear(this.webgl.COLOR_BUFFER_BIT | this.webgl.DEPTH_BUFFER_BIT)
  this.webgl.enable(this.webgl.DEPTH_TEST)
  this.webgl.drawArrays(this.webgl.TRIANGLES, 0, 9)
}
```



## 绘制一个正方体

完整代码：

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    <canvas id="weblCanvas" width="1024" height="768">
      你的浏览器似乎不支持或者禁用了HTML5 <code>&lt;canvas&gt;</code> 元素.
    </canvas>
    <script type="text/javascript" src="./dist/index.js"></script>
  </body>
</html>
```

```js
const mat4 = require('./gl-matrix').mat4

const myWebGl = {
  /**
   * @type {WebGLRenderingContext}
   */
  webgl: null,
  vertexString: ``,
  fragmentString: ``,
  vsshader: null,
  fsshader: null,
  program: null,
  init() {
    this.creatWebGl()
    this.creatShader()
    this.creatBuffer()
    this.draw()
  },
  creatWebGl() {
    let webGlDiv = document.getElementById('weblCanvas')
    this.webgl = webGlDiv.getContext('webgl')
    this.webgl.viewport(0, 0, webGlDiv.clientWidth, webGlDiv.clientHeight)
  },
  creatShader() {
    this.vsshader = this.webgl.createShader(this.webgl.VERTEX_SHADER)
    this.fsshader = this.webgl.createShader(this.webgl.FRAGMENT_SHADER)
    this.webgl.shaderSource(this.vsshader, this.vertexString)
    this.webgl.shaderSource(this.fsshader, this.fragmentString)

    this.webgl.compileShader(this.vsshader, this.vertexString)
    this.webgl.compileShader(this.fsshader, this.fragmentString)
    this.program = this.webgl.createProgram()
    this.webgl.attachShader(this.program, this.vsshader)
    this.webgl.attachShader(this.program, this.fsshader)

    this.webgl.linkProgram(this.program)
    this.webgl.useProgram(this.program)
  },
  creatBuffer() {},
  draw() {},
}

//这里引入颜色变量来根据顶点渲染不同的颜色
myWebGl.vertexString = `
attribute vec4 a_position;
uniform mat4 u_formMatrix;
void main(void) {
    gl_Position = u_formMatrix * a_position;
}
    `
myWebGl.fragmentString = `
precision mediump float;
void main() {
  gl_FragColor =vec4(0.0,1.0,1.0,1.0);
}
`
myWebGl.angle = 45
myWebGl.creatBuffer = function () {  
  //创建一个空矩阵作为模型矩阵
  let ModelMatrix = mat4.create();
  mat4.identity(ModelMatrix);
  mat4.translate(ModelMatrix, ModelMatrix, [1, 0, 0]); //平移
  //构建一个空矩阵作为视图矩阵
  let ViewMatrix = mat4.create() 
  mat4.identity(ViewMatrix)//将空矩阵单元化
  mat4.lookAt(ViewMatrix, [5, 5, 5], [0, 0, 0], [0, 0, 1])//创建一个视点矩阵，参数分别为，输出，视点，目标点，上方向
  let mvMatrix =  mat4.create();
  mat4.multiply(mvMatrix,ViewMatrix,ModelMatrix);
  //生成一个投影矩阵，对应的参数分别是，输出的矩阵，投影矩阵中视线的夹角，可是空间的长宽比，near和far
  let webGlDiv = document.getElementById('weblCanvas')  
  let ProjMatrix  = mat4.create()
  mat4.identity(ProjMatrix)
  mat4.perspective(ProjMatrix, myWebGl.angle * Math.PI / 180, webGlDiv.clientWidth/webGlDiv.clientHeight, 1, 1000)  
  //mvp矩阵
  let mvpMatrix = mat4.create();
  mat4.multiply(mvpMatrix,ProjMatrix,mvMatrix);
  //    v6----- v5
  //   /|      /|
  //  v1------v0|
  //  | |     | |
  //  | |v7---|-|v4
  //  |/      |/
  //  v2------v3

  let arr =[
    1, 1, 1, 1,  -1, 1, 1, 1,  -1, -1, 1, 1,  1, 1, 1, 1,  -1, -1, 1, 1,  1, -1, 1, 1,   //前面

    1, 1, -1, 1,  1, 1, 1, 1,  1, -1, 1, 1,  1, 1, -1, 1,  1, -1, 1, 1,  1, -1, -1, 1,  //右

    -1, 1, -1, 1,  1, 1, -1, 1,  1, -1, -1, 1,  -1, 1, -1, 1,  1, -1, -1, 1,  -1, -1, -1, 1, //后

    -1, 1, 1, 1,  -1, 1, -1, 1,  -1, -1, -1, 1,  -1, 1, 1, 1,  -1, -1, -1, 1,  -1, -1, 1, 1, //左

    -1, 1, -1, 1,  -1, 1, 1, 1,  1, 1, 1, 1,  -1, 1, -1, 1,  1, 1, 1, 1,  1, 1, -1, 1,  //上

    -1, -1, 1, 1,  -1, -1, -1, 1,  1, -1, -1, 1,  -1, -1, 1, 1,  1, -1, -1, 1,  1, -1, 1, 1,  //下
  ]

  let pointPosition = new Float32Array(arr)
  let aPsotion = this.webgl.getAttribLocation(myWebGl.program, 'a_position')
  let triangleBuffer = this.webgl.createBuffer()
  this.webgl.bindBuffer(this.webgl.ARRAY_BUFFER, triangleBuffer)
  this.webgl.bufferData(
    this.webgl.ARRAY_BUFFER,
    pointPosition,
    this.webgl.STATIC_DRAW
  )
  this.webgl.enableVertexAttribArray(aPsotion)
  this.webgl.vertexAttribPointer(aPsotion, 4, this.webgl.FLOAT, false, 4 * 4, 0)
  
  let uniformMatrix1 = this.webgl.getUniformLocation(
    myWebGl.program,
    'u_formMatrix'
  )
  this.webgl.uniformMatrix4fv(uniformMatrix1, false, mvpMatrix)
}

myWebGl.draw = function () {
  this.webgl.clearColor(0.0, 0.0, 0.0, 1.0)
  this.webgl.clear(this.webgl.COLOR_BUFFER_BIT | this.webgl.DEPTH_BUFFER_BIT)
  this.webgl.enable(this.webgl.DEPTH_TEST) //开启深度缓冲来解决画家算法问题
  this.webgl.drawArrays(this.webgl.TRIANGLES, 0, 36)
}

document.onkeydown = ev => {
  switch (ev.key) {
    case 'z':
      myWebGl.angle += 1
      console.log(myWebGl.angle)
      break
    case 'x':
      myWebGl.angle -= 1
      console.log(myWebGl.angle)
      break
  }
}

document.getElementById('weblCanvas').onload = (() => {
  myWebGl.init()
  const animate = function() {
    myWebGl.creatBuffer()
    myWebGl.draw()
    window.requestAnimationFrame(animate)
  }
  animate()
})()
```

效果：

<img src="https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/Snipaste_2022-07-18_22-56-01.png" style="zoom:50%;" />

需要指出的是，每个面都是由六个顶点绘制而成，这是因为一个面是由两个三角形拼接而成的，而绘制一个三角形则需要三个顶点。

同时我们可以给每个三角形加上颜色(通过给每个顶点定义颜色)，从而达到绘制每个面带有颜色的三角形。

除了通过顶点添加颜色以外，我们还可以选择使用纹理覆盖的形式来把



## 绘制一个穿衣服的正方体

我们对上面的代码进行修改，首先，我们需要将着色器部分改变：

顶点着色器：

```glsl
attribute vec4 a_position;
uniform mat4 u_formMatrix;
attribute vec4 a_color;
varying vec4 color;
void main(void){
    gl_Position =   u_formMatrix * a_position;
    color = a_color;
}
```

片元着色器：

```glsl
precision mediump float;
varying vec4 color;
void main() {
  gl_FragColor = color;
}
```



然后我们改变数据，将之前的arr，每个点后面都再跟4个点，来表示该点的颜色：

```js
arr = [
				1, 1, 1, 1, 1.0, 1.0, 1.0, 1.0, -1, 1, 1, 1, 1.0, 1.0, 1.0, 1.0, -1, -1, 1, 1, 1.0, 1.0, 1.0, 1.0, 1, 1, 1, 1, 1.0, 1.0, 1.0, 1.0, -1, -1, 1, 1, 1.0, 1.0, 1.0, 1.0, 1, -1, 1, 1, 1.0, 1.0, 1.0, 1.0,  //前面

                1, 1, -1, 1, 0.0, 1.0, 1.0, 1.0, 1, 1, 1, 1, 0.0, 1.0, 1.0, 1.0, 1, -1, 1, 1, 0.0, 1.0, 1.0, 1.0, 1, 1, -1, 1, 0.0, 1.0, 1.0, 1.0, 1, -1, 1, 1, 0.0, 1.0, 1.0, 1.0, 1, -1, -1, 1, 0.0, 1.0, 1.0, 1.0, //右

                -1, 1, -1, 1, 1.0, 0.0, 0.0, 1.0, 1, 1, -1, 1, 1.0, 0.0, 0.0, 1.0, 1, -1, -1, 1, 1.0, 0.0, 0.0, 1.0, -1, 1, -1, 1, 1.0, 0.0, 0.0, 1.0, 1, -1, -1, 1, 1.0, 0.0, 0.0, 1.0, -1, -1, -1, 1, 1.0, 0.0, 0.0, 1.0,//后

                -1, 1, 1, 1, 1.0, 1.0, 1, 1.0, -1, 1, -1, 1, 1.0, 1.0, 1, 1.0, -1, -1, -1, 1, 1.0, 1.0, 1, 1.0, -1, 1, 1, 1, 1.0, 1.0, 1, 1.0, -1, -1, -1, 1, 1.0, 1.0, 1, 1.0, -1, -1, 1, 1, 1.0, 1.0, 1, 1.0,//左

                -1, 1, -1, 1, 0.0, 1.0, 1.0, 1.0, -1, 1, 1, 1, 0.0, 1.0, 1.0, 1.0, 1, 1, 1, 1, 0.0, 1.0, 1.0, 1.0, -1, 1, -1, 1, 0.0, 1.0, 1.0, 1.0, 1, 1, 1, 1, 0.0, 1.0, 1.0, 1.0, 1, 1, -1, 1, 0.0, 1.0, 1.0, 1.0, //上

                -1, -1, 1, 1, 1.0, 1.0, 0, 1.0, -1, -1, -1, 1, 1.0, 1.0, 0, 1.0, 1, -1, -1, 1, 1.0, 1.0, 0, 1.0, -1, -1, 1, 1, 1.0, 1.0, 0, 1.0, 1, -1, -1, 1, 1.0, 1.0, 0, 1.0, 1, -1, 1, 1, 1.0, 1.0, 0, 1.0, //下
]
```

之后我们将表示颜色的点读入；

```js
let aColor = this.webgl.getAttribLocation(this.program, 'a_color') 
this.webgl.enableVertexAttribArray(aColor)
this.webgl.vertexAttribPointer(aColor, 4, this.webgl.FLOAT, false, 8 * 4, 4 * 4)
```

同时由于arr数据改变，我们也需要更改顶点的读入：

```js
this.webgl.enableVertexAttribArray(aPsotion)
this.webgl.vertexAttribPointer(aPsotion, 4, this.webgl.FLOAT, false, 8 * 4, 0) //4 * 4 -> 8 * 4
```

这样，我们既可以得到如下图形：

<img src="https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20220918180701.png" style="zoom: 25%;" />

注意我们的绘画函数，将深色缓冲区功能打开：

```js
myWebGl.draw = function () {
  this.webgl.clearColor(0.0, 0.0, 0.0, 1.0)
  this.webgl.clear(this.webgl.COLOR_BUFFER_BIT | this.webgl.DEPTH_BUFFER_BIT)
  this.webgl.enable(this.webgl.DEPTH_TEST)  // 深色缓冲区
  this.webgl.drawArrays(this.webgl.TRIANGLES, 0, 36)
}
```

就可以得到：

<img src="https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20220918180836.png" style="zoom: 25%;" />



同时我们也可以将纹理的功能引入，使用图片作为纹理素材（以下代码是对绘制正方体的原始代码改造）

改变我们的着色器代码（引入UV坐标，将图片坐标映射到顶点）

```js
let vertexstring = `
        attribute vec4 a_position;
        uniform mat4 u_formMatrix;
        attribute vec2 a_outUV;
        varying vec2 v_inUV;
        void main(void){
            gl_Position = u_formMatrix * a_position;
            v_inUV = a_outUV;
        }
        `;
let fragmentstring = `
        precision mediump float;
        uniform sampler2D texture;
        varying vec2 v_inUV;
        void main(void){
          gl_FragColor =texture2D(texture, v_inUV);
        }
        `;
```

我们更改arr数据，并且加入UV坐标(每一组前4个代表顶点坐标，后两个代表uv坐标)：

```js
let arr = [
    1, 1, 1, 1, 1, 1,    -1, 1,1, 1, 0, 1,    - 1,-1, 1, 1, 0, 0,     1,1,1, 1, 1, 1,     - 1,- 1,1, 1, 0, 0,    1,- 1, 1, 1, 1, 0,   //前面

    1, 1, -1, 1,1, 1,     1, 1, 1, 1,0, 1,     1, -1, 1, 1, 0, 0,     1, 1, -1, 1,1,1,    1, -1, 1, 1,0,0,       1, -1, -1, 1,1,0,  //右

    -1, 1, -1, 1,1,1,     1, 1, -1, 1,0,1,     1, -1, -1, 1,0,0,      -1, 1, -1, 1,1,1,   1, -1, -1, 1,0,0,     -1, -1, -1, 1,1,0, //后


    -1, 1, 1, 1,1,1,      -1, 1, -1, 1,1,0,    -1, -1, -1, 1,0,0,     -1, 1, 1, 1,1,1,    -1, -1, -1, 1,0,0,     -1, -1, 1, 1,1,0, //左

    -1, 1, -1, 1, 0,1,    -1, 1, 1, 1, 0,0,    1, 1, 1, 1,1,0,        -1, 1, -1, 1,0,1,    1, 1, 1, 1,1,0,        1, 1, -1, 1,1,1,  //上

    -1, -1, 1, 1,0,1,     -1, -1, -1, 1,0,0,    1, -1, -1, 1,1,0,     -1, -1, 1, 1,0,1,    1, -1, -1, 1,1,0,      1, -1, 1, 1,1,1,  //下
    ]

...

this.webgl.vertexAttribPointer(aPsotion, 4, this.webgl.FLOAT, false, 6 * 4, 0);

let attribOutUV = this.webgl.getAttribLocation(myWebGl.program, "a_outUV");
this.webgl.enableVertexAttribArray(attribOutUV);
this.webgl.vertexAttribPointer(attribOutUV, 2, this.webgl.FLOAT, false, 6 * 4, 4 * 4);

```

最后我们加入纹理：

```js
  myWebGl.uniformTexture = this.webgl.getUniformLocation(myWebGl.program, "texture");

  myWebGl.texture = initTexture("bac.jpg", this.webgl); //初始化纹理并返回texture

  function initTexture(imageFile, webgl) {
    let textureHandle = webgl.createTexture();
    textureHandle.image = new Image();
    textureHandle.image.src = imageFile;
    textureHandle.image.onload = function () {
        handleLoadedTexture(textureHandle, webgl)
    }
    return textureHandle;
  }
  function handleLoadedTexture(texture, webgl) {

      webgl.bindTexture(webgl.TEXTURE_2D, texture);
      webgl.pixelStorei(webgl.UNPACK_FLIP_Y_WEBGL, 666);

      webgl.texImage2D(webgl.TEXTURE_2D, 0, webgl.RGBA, webgl.RGBA, webgl.UNSIGNED_BYTE, texture.image);
      webgl.texParameteri(webgl.TEXTURE_2D, webgl.TEXTURE_MAG_FILTER, webgl.LINEAR);// 纹理放大方式
      webgl.texParameteri(webgl.TEXTURE_2D, webgl.TEXTURE_MIN_FILTER, webgl.LINEAR);// 纹理缩小方式
      webgl.texParameteri(webgl.TEXTURE_2D, webgl.TEXTURE_WRAP_S, webgl.CLAMP_TO_EDGE);// 纹理水平填充方式
      webgl.texParameteri(webgl.TEXTURE_2D, webgl.TEXTURE_WRAP_T, webgl.CLAMP_TO_EDGE);// 纹理垂直填充方式
      webgl.clearColor(0, 0, 0, 1);
      webgl.clear(webgl.COLOR_BUFFER_BIT | webgl.DEPTH_BUFFER_BIT);
      webgl.enable(webgl.DEPTH_TEST);
      webgl.activeTexture(webgl.TEXTURE0);
      webgl.bindTexture(webgl.TEXTURE_2D, texture);
      webgl.uniform1i(myWebGl.uniformTexture, 0);
      webgl.drawArrays(webgl.TRIANGLES, 0, 36);
  }
```

就可以得到如下带纹理的正方体了：

<img src="https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20220918204923.png" style="zoom: 33%;" />

## 光照

先了解几个概念：

光照类型：

<img src="https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20220918211447.png" style="zoom: 67%;" />

光照分为：平行光，点光源光，环境光。

反射类型：

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20220918212159.png)

反射分为漫反射，环境反射。（还有镜面反射，理想状态下）

法线：

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20220918212939.png)



## 平行光（漫反射）

基本公式：

**环境反射光颜色 = 入射光颜色 × 表面基底色 × cosθ **

cosθ = 光线方向 · 法线方向

示例代码

```js
const mat4 = require('./gl-matrix').mat4

const myWebGl = {
  /**
   * @type {WebGLRenderingContext}
   */
  webgl: null,
  vertexString: ``,
  fragmentString: ``,
  vsshader: null,
  fsshader: null,
  program: null,
  init() {
    this.creatWebGl()
    this.creatShader()
    this.creatBuffer()
    this.draw()
  },
  creatWebGl() {
    let webGlDiv = document.getElementById('weblCanvas')
    this.webgl = webGlDiv.getContext('webgl') 
    this.webgl.viewport(0, 0, webGlDiv.clientWidth, webGlDiv.clientHeight)
  },
  creatShader() {
    this.vsshader = this.webgl.createShader(this.webgl.VERTEX_SHADER)
    this.fsshader = this.webgl.createShader(this.webgl.FRAGMENT_SHADER)
    this.webgl.shaderSource(this.vsshader, this.vertexString)
    this.webgl.shaderSource(this.fsshader, this.fragmentString)

    this.webgl.compileShader(this.vsshader, this.vertexString)
    this.webgl.compileShader(this.fsshader, this.fragmentString)
    this.program = this.webgl.createProgram()
    this.webgl.attachShader(this.program, this.vsshader)
    this.webgl.attachShader(this.program, this.fsshader)

    this.webgl.linkProgram(this.program)
    this.webgl.useProgram(this.program)
  },
  creatBuffer() {},
  draw() {},
}

//这里引入颜色变量来根据顶点渲染不同的颜色
myWebGl.vertexString = `
  attribute vec4 a_position;
  uniform mat4 u_formMatrix;
  attribute vec4 a_Normal;
  uniform vec3 u_LightDirection;
  uniform vec3 u_DiffuseLight;
  uniform vec3 u_AmbientLight;
  varying vec4 v_Color;
  void main(void){
  gl_Position = u_formMatrix * a_position;
  vec3 normal = normalize(a_Normal.xyz);
  vec3 LightDirection = normalize(u_LightDirection.xyz);
  float nDotL = max(dot(LightDirection, normal), 0.0);
  vec3 diffuse = u_DiffuseLight * vec3(1.0,0,1.0)* nDotL;
  vec3 ambient = u_AmbientLight * vec3(1.0,0,1.0);
  v_Color = vec4(diffuse + ambient, 1);
  }`
myWebGl.fragmentString = `
    precision mediump float;
    varying vec4 v_Color;
    void main(void){
      gl_FragColor =v_Color;
    }
`
myWebGl.angle = 45
myWebGl.creatBuffer = function () {  
  //创建一个空矩阵作为模型矩阵
  let ModelMatrix = mat4.create();
  mat4.identity(ModelMatrix);
  mat4.translate(ModelMatrix, ModelMatrix, [1, 0, 0]); //平移
  //构建一个空矩阵作为视图矩阵
  let ViewMatrix = mat4.create() 
  mat4.identity(ViewMatrix)//将空矩阵单元化
  mat4.lookAt(ViewMatrix, [5, 5, 5], [0, 0, 0], [0, 0, 1])//创建一个视点矩阵，参数分别为，输出，视点，目标点，上方向
  let mvMatrix =  mat4.create();
  mat4.multiply(mvMatrix,ViewMatrix,ModelMatrix);
  //生成一个投影矩阵，对应的参数分别是，输出的矩阵，投影矩阵中视线的夹角，可是空间的长宽比，near和far
  let webGlDiv = document.getElementById('weblCanvas')  
  let ProjMatrix  = mat4.create()
  mat4.identity(ProjMatrix)
  mat4.perspective(ProjMatrix, myWebGl.angle * Math.PI / 180, webGlDiv.clientWidth/webGlDiv.clientHeight, 1, 1000)  
  //mvp矩阵
  let mvpMatrix = mat4.create();
  mat4.multiply(mvpMatrix,ProjMatrix,mvMatrix);
  //    v6----- v5
  //   /|      /|
  //  v1------v0|
  //  | |     | |
  //  | |v7---|-|v4
  //  |/      |/
  //  v2------v3

    let arr = [
        1.0, 1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, 1.0, -1.0, 1.0, 1.0, // v0-v1-v2-v3 
        1.0, 1.0, 1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, 1.0, -1.0, 1.0, // v0-v3-v4-v5 
        1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, 1.0, // v0-v5-v6-v1 
        -1.0, 1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, -1.0, 1.0, -1.0, -1.0, 1.0, 1.0, // v1-v6-v7-v2 
        -1.0, -1.0, -1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, // v7-v4-v3-v2 
        1.0, -1.0, -1.0, 1.0, -1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, 1.0, -1.0, 1.0 // v4-v7-v6-v5 

    ]
    let normals = new Float32Array([
        0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0,  // v0-v1-v2-v3 front
        1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0,  // v0-v3-v4-v5 right
        0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,  // v0-v5-v6-v1 up
        -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0,  // v1-v6-v7-v2 left
        0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0,  // v7-v4-v3-v2 down
        0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0   // v4-v7-v6-v5 back
    ]);
    let index = [
        0, 1, 2, 0, 2, 3,    // front
        4, 5, 6, 4, 6, 7,    // right
        8, 9, 10, 8, 10, 11,    // up
        12, 13, 14, 12, 14, 15,    // left
        16, 17, 18, 16, 18, 19,    // down
        20, 21, 22, 20, 22, 23     // back
    ];

  let pointPosition = new Float32Array(arr)
  let aPsotion = this.webgl.getAttribLocation(myWebGl.program, 'a_position')
  let triangleBuffer = this.webgl.createBuffer()
  this.webgl.bindBuffer(this.webgl.ARRAY_BUFFER, triangleBuffer)
  this.webgl.bufferData(
    this.webgl.ARRAY_BUFFER,
    pointPosition,
    this.webgl.STATIC_DRAW
  )
  this.webgl.enableVertexAttribArray(aPsotion)
  this.webgl.vertexAttribPointer(aPsotion, 4, this.webgl.FLOAT, false, 4 * 4, 0)


  let aNormal = this.webgl.getAttribLocation(myWebGl.program, "a_Normal")
  let normalsBuffer = this.webgl.createBuffer()
  let normalsArr = new Float32Array(normals)
  this.webgl.bindBuffer(this.webgl.ARRAY_BUFFER, normalsBuffer)
  this.webgl.bufferData(this.webgl.ARRAY_BUFFER, normalsArr, this.webgl.STATIC_DRAW)
  this.webgl.enableVertexAttribArray(aNormal)
  this.webgl.vertexAttribPointer(aNormal, 3, this.webgl.FLOAT, false, 3 * 4, 0)
  
  let u_DiffuseLight = this.webgl.getUniformLocation(myWebGl.program, 'u_DiffuseLight');
  let u_LightDirection = this.webgl.getUniformLocation(myWebGl.program, 'u_LightDirection');
  let u_AmbientLight = this.webgl.getUniformLocation(myWebGl.program, 'u_AmbientLight');
  this.webgl.uniform3f(u_DiffuseLight, 1.0, 1.0, 1.0)
  this.webgl.uniform3fv(u_LightDirection, [0, 0, 10.0])
  this.webgl.uniform3f(u_AmbientLight, 0.2, 0.2, 0.2)

  let indexBuffer = this.webgl.createBuffer();
  let indices = new Uint8Array(index);
  this.webgl.bindBuffer(this.webgl.ELEMENT_ARRAY_BUFFER, indexBuffer);
  this.webgl.bufferData(this.webgl.ELEMENT_ARRAY_BUFFER, indices, this.webgl.STATIC_DRAW);

  let uniformMatrix1 = this.webgl.getUniformLocation(
    myWebGl.program,
    'u_formMatrix'
  )
  this.webgl.uniformMatrix4fv(uniformMatrix1, false, mvpMatrix)
}

myWebGl.draw = function () {
  this.webgl.clearColor(0.0, 0.0, 0.0, 1.0)
  this.webgl.clear(this.webgl.COLOR_BUFFER_BIT | this.webgl.DEPTH_BUFFER_BIT)
  this.webgl.enable(this.webgl.DEPTH_TEST) //开启深度缓冲来解决画家算法问题
  this.webgl.drawElements(this.webgl.TRIANGLES, 36, this.webgl.UNSIGNED_BYTE, 0)
}

document.onkeydown = ev => {
  switch (ev.key) {
    case 'z':
      myWebGl.angle += 1
      console.log(myWebGl.angle)
      break
    case 'x':
      myWebGl.angle -= 1
      console.log(myWebGl.angle)
      break
  }
}

document.getElementById('weblCanvas').onload = (() => {
  myWebGl.init()
  const animate = function() {
    myWebGl.creatBuffer()
    myWebGl.draw()
    window.requestAnimationFrame(animate)
  }
  animate()
})()
```

可以看到一个有一面很亮的正方体：

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20220921003656.png)

其中的顶点着色器，有几个函数需要去了解一下：

`normalize()` 归一化 

`dot()` cosθ

以及顶点着色器中的几个变量的含义：

```js
vec3 diffuse = u_DiffuseLight * vec3(1.0,0,1.0)* nDotL; //反射光

vec3 ambient = u_AmbientLight * vec3(1.0,0,1.0); //环境光
```



## 点光源

点光源中，由于不是平行光，所以我们需要当前光线方向来计算cosθ

基本公式：

**环境反射光颜色 = 入射光颜色 × 表面基底色 × cosθ **

cosθ = 光线方向 · 法线方向

和第一个唯一不同的就是我们的光线方向是动态的，需要实时去计算。

这需要我们变动顶点着色器shader

```glsl
attribute vec4 a_position;
uniform mat4 u_formMatrix;
attribute vec4 a_Normal;
uniform vec3 u_PointLightPosition;
uniform vec3 u_DiffuseLight;
uniform vec3 u_AmbientLight;
varying vec4 v_Color;
uniform mat4 u_NormalMatrix;
void main(void){
    gl_Position = u_formMatrix * a_position;

    vec3 normal = normalize(vec3(u_NormalMatrix * a_Normal));
    vec3 lightDirection = normalize( vec3(gl_Position.xyz)-u_PointLightPosition );
    float nDotL = max(dot(lightDirection, normal), 0.0);
    vec3 diffuse = u_DiffuseLight * vec3(1.0,0,1.0)* nDotL;
    vec3 ambient = u_AmbientLight * vec3(1.0,0,1.0);
    v_Color = vec4(diffuse + ambient, 1);
}
```

这里我们主要改动了：

```glsl
normalize( vec3(gl_Position.xyz)-u_PointLightPosition );
```

因为最开始的光线为平行光，现在的光线变成了点光源，我们通过点光源和顶点相减得到当前的光线方向。

同时引入了新变量：u_NormalMatrix用来进行矩阵变换（法向量齐次矩阵）。

新的createBuffer函数如下：

```js
myWebGl.creatBuffer = function () {  
  //创建一个空矩阵作为模型矩阵
  let ModelMatrix = mat4.create();
  mat4.identity(ModelMatrix);
  mat4.translate(ModelMatrix, ModelMatrix, [0, 0, 0]); //平移
  //构建一个空矩阵作为视图矩阵
  let ViewMatrix = mat4.create() 
  mat4.identity(ViewMatrix)//将空矩阵单元化
  mat4.lookAt(ViewMatrix, [5, 5, 5], [0, 0, 0], [0, 1, 0])//创建一个视点矩阵，参数分别为，输出，视点，目标点，上方向
  let mvMatrix =  mat4.create();
  mat4.multiply(mvMatrix,ViewMatrix,ModelMatrix);
  //生成一个投影矩阵，对应的参数分别是，输出的矩阵，投影矩阵中视线的夹角，可是空间的长宽比，near和far
  let webGlDiv = document.getElementById('weblCanvas')  
  let ProjMatrix  = mat4.create()
  mat4.identity(ProjMatrix)
  mat4.perspective(ProjMatrix, myWebGl.angle * Math.PI / 180, webGlDiv.clientWidth/webGlDiv.clientHeight, 1, 1000)  
  //mvp矩阵
  let mvpMatrix = mat4.create();
  mat4.multiply(mvpMatrix,ProjMatrix,mvMatrix);
  //    v6----- v5
  //   /|      /|
  //  v1------v0|
  //  | |     | |
  //  | |v7---|-|v4
  //  |/      |/
  //  v2------v3

    let arr = [
        1.0, 1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, 1.0, -1.0, 1.0, 1.0, // v0-v1-v2-v3 
        1.0, 1.0, 1.0, 1.0, 1.0, -1.0, 1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, 1.0, -1.0, 1.0, // v0-v3-v4-v5 
        1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, 1.0, // v0-v5-v6-v1 
        -1.0, 1.0, 1.0, 1.0, -1.0, 1.0, -1.0, 1.0, -1.0, -1.0, -1.0, 1.0, -1.0, -1.0, 1.0, 1.0, // v1-v6-v7-v2 
        -1.0, -1.0, -1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, -1.0, 1.0, 1.0, -1.0, -1.0, 1.0, 1.0, // v7-v4-v3-v2 
        1.0, -1.0, -1.0, 1.0, -1.0, -1.0, -1.0, 1.0, -1.0, 1.0, -1.0, 1.0, 1.0, 1.0, -1.0, 1.0 // v4-v7-v6-v5 

    ]
    let normals = new Float32Array([
        0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0,  // v0-v1-v2-v3 front
        1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0,  // v0-v3-v4-v5 right
        0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 1.0, 0.0,  // v0-v5-v6-v1 up
        -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0,  // v1-v6-v7-v2 left
        0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0,  // v7-v4-v3-v2 down
        0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0, 0.0, 0.0, -1.0   // v4-v7-v6-v5 back
    ]);
    let index = [
        0, 1, 2, 0, 2, 3,    // front
        4, 5, 6, 4, 6, 7,    // right
        8, 9, 10, 8, 10, 11,    // up
        12, 13, 14, 12, 14, 15,    // left
        16, 17, 18, 16, 18, 19,    // down
        20, 21, 22, 20, 22, 23     // back
    ];

  let pointPosition = new Float32Array(arr)
  let aPsotion = this.webgl.getAttribLocation(myWebGl.program, 'a_position')
  let triangleBuffer = this.webgl.createBuffer()
  this.webgl.bindBuffer(this.webgl.ARRAY_BUFFER, triangleBuffer)
  this.webgl.bufferData(
    this.webgl.ARRAY_BUFFER,
    pointPosition,
    this.webgl.STATIC_DRAW
  )
  this.webgl.enableVertexAttribArray(aPsotion)
  this.webgl.vertexAttribPointer(aPsotion, 4, this.webgl.FLOAT, false, 4 * 4, 0)


  let aNormal = this.webgl.getAttribLocation(myWebGl.program, "a_Normal")
  let normalsBuffer = this.webgl.createBuffer()
  let normalsArr = new Float32Array(normals)
  this.webgl.bindBuffer(this.webgl.ARRAY_BUFFER, normalsBuffer)
  this.webgl.bufferData(this.webgl.ARRAY_BUFFER, normalsArr, this.webgl.STATIC_DRAW)
  this.webgl.enableVertexAttribArray(aNormal)
  this.webgl.vertexAttribPointer(aNormal, 3, this.webgl.FLOAT, false, 3 * 4, 0)

  let uniformNormalMatrix = this.webgl.getUniformLocation(myWebGl.program, "u_NormalMatrix");
  let normalMatrix = mat4.create();
  mat4.identity(normalMatrix);
  mat4.invert(normalMatrix,ModelMatrix);
  mat4.transpose(normalMatrix,ModelMatrix);
  this.webgl.uniformMatrix4fv(uniformNormalMatrix, false, normalMatrix);
  
  let u_DiffuseLight = this.webgl.getUniformLocation(myWebGl.program, 'u_DiffuseLight');
  let u_PointLightPosition = this.webgl.getUniformLocation(myWebGl.program, 'u_PointLightPosition');
  let u_AmbientLight = this.webgl.getUniformLocation(myWebGl.program, 'u_AmbientLight');
  this.webgl.uniform3f(u_DiffuseLight, 1.0, 1.0, 1.0)
  this.webgl.uniform3fv(u_PointLightPosition, [-1, 2, 0])
  this.webgl.uniform3f(u_AmbientLight, 0.2, 0.2, 0.2)


  let indexBuffer = this.webgl.createBuffer();
  let indices = new Uint8Array(index);
  this.webgl.bindBuffer(this.webgl.ELEMENT_ARRAY_BUFFER, indexBuffer);
  this.webgl.bufferData(this.webgl.ELEMENT_ARRAY_BUFFER, indices, this.webgl.STATIC_DRAW);

  let uniformMatrix1 = this.webgl.getUniformLocation(
    myWebGl.program,
    'u_formMatrix'
  )
  this.webgl.uniformMatrix4fv(uniformMatrix1, false, mvpMatrix)
}
```

我们就可以得到如下的图

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/image-20220923233737125.png)

## 环境光

环境光指那些经光源（点光源或者平行光源）发出后，被墙壁等物体多次反射，然后照射到物体表面的光。环境光从各个角度照射物体，其强度都是一致的。环境光不需要指定位置和方向，只需要指定颜色即可。

相关公式：

漫反射光颜色 = 入射光颜色 × 表面基底色

这里的着色器shader改变：

```glsl
attribute vec4 a_position;
uniform mat4 u_formMatrix;
uniform vec3 u_AmbientLight;
varying vec4 v_Color;
void main(void){
    gl_Position = u_formMatrix * a_position;
    vec3 ambient = u_AmbientLight * vec3(1.0,0,1.0);
    v_Color = vec4(ambient, 1);
}
```

可以看出现在只剩下一个环境光的强度了

其他部分只需要做出相应删减，就可以得到以下（这个正方体一开始很暗）：

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20220924001944.png)



## 逐顶点光照和逐片元光照

  **逐顶点计算**指的是在每个顶点进行颜色值的计算（前面的代码都是在顶点上计算颜色或光照后的颜色，最后通过varying类型的变量传递到片元着色器 ），逐片元则是在片元着色器中对每一个片元进行计算并着色。 

  我们分别对一个球体进行逐顶点和逐片元光照：

  逐顶点：

   ![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20220927225223.png)

  逐片元：

   ![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20220927225441.png)

可以看到，逐片元计算的球体对光照的显示更加平滑。

代码部分：

```js
const mat4 = require("./gl-matrix").mat4;

const myWebGl = {
  /**
   * @type {WebGLRenderingContext}
   */
  webgl: null,
  vertexString: ``,
  fragmentString: ``,
  vsshader: null,
  fsshader: null,
  program: null,
  init() {
    this.creatWebGl();
    this.creatShader();
    this.creatBuffer();
    this.draw();
  },
  creatWebGl() {
    let webGlDiv = document.getElementById("weblCanvas");
    this.webgl = webGlDiv.getContext("webgl");
    this.webgl.viewport(0, 0, webGlDiv.clientWidth, webGlDiv.clientHeight);
  },
  creatShader() {
    this.vsshader = this.webgl.createShader(this.webgl.VERTEX_SHADER);
    this.fsshader = this.webgl.createShader(this.webgl.FRAGMENT_SHADER);
    this.webgl.shaderSource(this.vsshader, this.vertexString);
    this.webgl.shaderSource(this.fsshader, this.fragmentString);

    this.webgl.compileShader(this.vsshader, this.vertexString);
    this.webgl.compileShader(this.fsshader, this.fragmentString);
    this.program = this.webgl.createProgram();
    this.webgl.attachShader(this.program, this.vsshader);
    this.webgl.attachShader(this.program, this.fsshader);

    this.webgl.linkProgram(this.program);
    this.webgl.useProgram(this.program);
  },
  creatBuffer() {},
  draw() {},
};

//这里引入颜色变量来根据顶点渲染不同的颜色
myWebGl.vertexString = `
attribute vec4 a_position;
uniform mat4 u_formMatrix;
attribute vec4 a_Normal;
varying vec4 v_Normal;
varying vec4 v_position;
void main(void){
gl_Position = u_formMatrix * a_position;
v_position = gl_Position;
v_Normal= a_Normal;
}`;
myWebGl.fragmentString = `
precision mediump float;
   
varying vec4 v_Normal;
varying vec4 v_position;
uniform vec3 u_PointLightPosition;
uniform vec3 u_DiffuseLight;
uniform vec3 u_AmbientLight;
void main(void){
vec3 normal = normalize(v_Normal.xyz);
vec3 lightDirection = normalize(u_PointLightPosition - vec3(v_position.xyz));
float nDotL = max(dot(lightDirection, normal), 0.0);
vec3 diffuse = u_DiffuseLight * vec3(1.0,0,1.0)* nDotL;
vec3 ambient = u_AmbientLight * vec3(1.0,0,1.0);

  gl_FragColor =vec4(diffuse + ambient, 1);
}
`;
myWebGl.angle = 45;
myWebGl.creatBuffer = function () {
  // 创建mvp矩阵
  //创建一个空矩阵作为模型矩阵
  let ModelMatrix = mat4.create();
  mat4.identity(ModelMatrix);
  mat4.translate(ModelMatrix, ModelMatrix, [0, 0, 0]); //平移
  //构建一个空矩阵作为视图矩阵
  let ViewMatrix = mat4.create();
  mat4.identity(ViewMatrix); //将空矩阵单元化
  mat4.lookAt(ViewMatrix, [5, 5, 5], [0, 0, 0], [0, 1, 0]); //创建一个视点矩阵，参数分别为，输出，视点，目标点，上方向
  let mvMatrix = mat4.create();
  mat4.multiply(mvMatrix, ViewMatrix, ModelMatrix);
  //生成一个投影矩阵，对应的参数分别是，输出的矩阵，投影矩阵中视线的夹角，可是空间的长宽比，near和far
  let webGlDiv = document.getElementById("weblCanvas");
  let ProjMatrix = mat4.create();
  mat4.identity(ProjMatrix);
  mat4.perspective(
    ProjMatrix,
    (myWebGl.angle * Math.PI) / 180,
    webGlDiv.clientWidth / webGlDiv.clientHeight,
    1,
    1000
  );
  //mvp矩阵
  let mvpMatrix = mat4.create();
  mat4.multiply(mvpMatrix, ProjMatrix, mvMatrix);
  let uniformMatrix1 = this.webgl.getUniformLocation(
    myWebGl.program,
    "u_formMatrix"
  );
  this.webgl.uniformMatrix4fv(uniformMatrix1, false, mvpMatrix);


  // 添加数据并读入shader
  let positions = []
  let indices = []
  let SPHERE_DIV = 15;

  let i, ai, si, ci;
  let j, aj, sj, cj;
  let p1, p2;

  // Generate coordinates
  for (j = 0; j <= SPHERE_DIV; j++) {
    aj = (j * Math.PI) / SPHERE_DIV;
    sj = Math.sin(aj);
    cj = Math.cos(aj);
    for (i = 0; i <= SPHERE_DIV; i++) {
      ai = (i * 2 * Math.PI) / SPHERE_DIV;
      si = Math.sin(ai);
      ci = Math.cos(ai);

      positions.push(ci * sj); // X
      positions.push(cj); // Y
      positions.push(si * sj); // Z
    }
  }

  for (j = 0; j < SPHERE_DIV; j++) {
    for (i = 0; i < SPHERE_DIV; i++) {
      p1 = j * (SPHERE_DIV + 1) + i;
      p2 = p1 + (SPHERE_DIV + 1);

      indices.push(p1);
      indices.push(p2);
      indices.push(p1 + 1);

      indices.push(p1 + 1);
      indices.push(p2);
      indices.push(p2 + 1);
    }
  }

  let pointPosition = new Float32Array(positions);
  let aPsotion = this.webgl.getAttribLocation(myWebGl.program, "a_position");
  let triangleBuffer = this.webgl.createBuffer();
  this.webgl.bindBuffer(this.webgl.ARRAY_BUFFER, triangleBuffer);
  this.webgl.bufferData(
    this.webgl.ARRAY_BUFFER,
    pointPosition,
    this.webgl.STATIC_DRAW
  );
  this.webgl.enableVertexAttribArray(aPsotion);
  this.webgl.vertexAttribPointer(
    aPsotion,
    3,
    this.webgl.FLOAT,
    false,
    0,
    0
  );

  let aNormal = this.webgl.getAttribLocation(myWebGl.program, "a_Normal");
  let normalsBuffer = this.webgl.createBuffer();
  let normalsArr = new Float32Array(positions);
  this.webgl.bindBuffer(this.webgl.ARRAY_BUFFER, normalsBuffer);
  this.webgl.bufferData(
    this.webgl.ARRAY_BUFFER,
    normalsArr,
    this.webgl.STATIC_DRAW
  );
  this.webgl.enableVertexAttribArray(aNormal);
  this.webgl.vertexAttribPointer(aNormal, 3, this.webgl.FLOAT, false, 0, 0);

  let u_DiffuseLight = this.webgl.getUniformLocation(myWebGl.program, 'u_DiffuseLight');
  this.webgl.uniform3f(u_DiffuseLight, 1.0, 1.0, 1.0);
  let u_LightDirection = this.webgl.getUniformLocation(myWebGl.program, 'u_PointLightPosition');
  this.webgl.uniform3fv(u_LightDirection, [3.0, 3.0, 4.0]);
  let u_AmbientLight = this.webgl.getUniformLocation(myWebGl.program, 'u_AmbientLight');
  this.webgl.uniform3f(u_AmbientLight, 0.2, 0., 0.2);




  let indexBuffer = this.webgl.createBuffer();
  let indices1 = new Uint8Array(indices);
  this.webgl.bindBuffer(this.webgl.ELEMENT_ARRAY_BUFFER, indexBuffer);
  this.webgl.bufferData(this.webgl.ELEMENT_ARRAY_BUFFER, indices1, this.webgl.STATIC_DRAW);
};

myWebGl.draw = function () {
  this.webgl.clearColor(0.0, 0.0, 0.0, 1.0);
  this.webgl.clear(this.webgl.COLOR_BUFFER_BIT | this.webgl.DEPTH_BUFFER_BIT);
  this.webgl.enable(this.webgl.DEPTH_TEST); //开启深度缓冲来解决画家算法问题
  this.webgl.drawElements(
    this.webgl.TRIANGLES,
    1350,
    this.webgl.UNSIGNED_BYTE,
    0
  );
};

document.onkeydown = (ev) => {
  switch (ev.key) {
    case "z":
      myWebGl.angle += 1;
      console.log(myWebGl.angle);
      break;
    case "x":
      myWebGl.angle -= 1;
      console.log(myWebGl.angle);
      break;
  }
};

document.getElementById("weblCanvas").onload = (() => {
  myWebGl.init();
  const animate = function () {
    myWebGl.creatBuffer();
    myWebGl.draw();
    window.requestAnimationFrame(animate);
  };
  animate();
})();
```



我们可以看到，片元着色器shader发生了较大的变化，颜色光照的计算都在这里进行：

```glsl
precision mediump float;
   
varying vec4 v_Normal;
varying vec4 v_position;
uniform vec3 u_PointLightPosition;
uniform vec3 u_DiffuseLight;
uniform vec3 u_AmbientLight;
void main(void){
vec3 normal = normalize(v_Normal.xyz);
vec3 lightDirection = normalize(u_PointLightPosition - vec3(v_position.xyz));
float nDotL = max(dot(lightDirection, normal), 0.0);
vec3 diffuse = u_DiffuseLight * vec3(1.0,0,1.0)* nDotL;
vec3 ambient = u_AmbientLight * vec3(1.0,0,1.0);

  gl_FragColor =vec4(diffuse + ambient, 1);
}
```





# 计算机图形学导论（webGL版）



# 字节跳动WebGL网课

### WebGL实际代码步骤：

1. 创建WebGL上下文

   ```js
   const canvas = document.querySelector('canvas') //找到canvas标签，因为webgl是绘画在canvas上的
   const gl = canvas.getContext('webgl') //指定当前画布内容是webgl类型
   ```

2. 创建shader

   ```js
   //着色器分为顶点着色器和片段着色器（Vertex Shader 和 Fragment Shader）
   ```

3. 利用着色器创建WebGL的program

   ```js
   const vsshader = webgl.createShader(this.webgl.VERTEX_SHADER) //顶点着色器
   const fsshader = webgl.createShader(this.webgl.FRAGMENT_SHADER) //片段着色器
   webgl.shaderSource(vsshader, vertexString) //vertexString就是顶点着色器的代码
   webgl.shaderSource(fsshader, fragmentString) //fragmentString片段着色器的代码
   //webgl编译shader
   webgl.compileShader(vsshader, vertexString)
   webgl.compileShader(fsshader, fragmentString)
   //创建program
   program = webgl.createProgram()
   webgl.attachShader(program, vsshader)
   webgl.attachShader(program, fsshader)
   //绑定并使用program
   webgl.linkProgram(program)
   webgl.useProgram(program)
   ```

4. buffer形式传入数据

   ```js
   const points = new Float32Array([-1,-1, 0,1, 1,-1])
   const bufferId = webgl.createBuffer() //创造一个webgl的buffer
   webgl.bindBuffer(gl.ARRAY_BUFFER, bufferId) //绑定buffer
   webgl.bufferData(gl.ARRAY_BUFFER, ponits, gl.STATIC_DRAW) //填充数据
   ```

5. 将数据送到着色器

   ```
   const Podition = webgl.getAttribLocation(program, 'position') //获得顶点着色器中position变量地址
   webgl.verTexAttribPosition(vPosition, 2, gl.FLOAT, false, 0, 0) //给变量获取长度和类型
   ```

6. 解析变量

   ```js
   const Vposition = webgl.getAttribLocation(program, 'position') //获取顶点着色器中的position变量的地址
   webgl.vertexAttribPosition(vPosition, 2, webgl.FLOAT, false, 0, 0) //设置变量的长度和类型，对应我们之前声明的ponits中的每一个点，这里表明是每2个值作为一个顶点坐标
   webgl.enableVertexAttribArray(vPosition) //激活顶点坐标
   ```

7. 绘画

   ```js
   webgl.drawArray(gl.TRIANGLES, 0, points.length / 2) //绘画什么图形，偏移量和长度
   ```

### 四个齐次矩阵（mat4）

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20220813234412.png)

投影矩阵：处理坐标系，改变大小，方向，左手系右手系等

模型矩阵：对模型进行线性变换，改变大小方向，旋转平移等

视图矩阵：用来控制“摄像机”的位置

法向量矩阵：每个物体的每个表面都有垂直向外的法向量，法向量矩阵来描述法线信息，法线信息可以用来处理光照效果

至于这四个矩阵的更通俗的说法，可以观看：[探秘三维透视投影 - 齐次坐标的妙用_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1LS4y1b7xZ/?spm_id_from=333.999.0.0&vd_source=9f4f5fa0ddf7994dab77edc934f59978)

### 齐次（齐次矩阵，齐次坐标）

齐次是什么意思，它是用来给给坐标加上一个新的维度，来达到更好的向量变换（如平移和透视）的效果，这个新的维度就叫做齐次坐标。而针对新的坐标而来的变换矩阵就是齐次矩阵。参考资料：[无所不能的矩阵 - 三维图形变换_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1b34y1y7nF/?spm_id_from=333.999.0.0&vd_source=9f4f5fa0ddf7994dab77edc934f59978) [探秘三维透视投影 - 齐次坐标的妙用_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1LS4y1b7xZ/?spm_id_from=333.999.0.0&vd_source=9f4f5fa0ddf7994dab77edc934f59978)



参考

[Dev.Opera — An Introduction to WebGL — Part 1](https://dev.opera.com/articles/introduction-to-webgl-part-1/)

[入门 WebGL，看这一篇就够了*大前端*一颗大橄榄\_InfoQ 写作社区](https://xie.infoq.cn/article/511aa64f69530ed3061829351)

[Jsonco/webglTecher (gitee.com)](https://gitee.com/jsonco/webgl-techer)

[WebGL API 中文文档*WebGL 教程*郭隆邦技术博客 (yanhuangxueyuan.com)](http://www.yanhuangxueyuan.com/doc/webgl.html)

[(6 条消息) WebGL 入门-WebGL 常用 API 说明详解\_点燃火柴的博客-CSDN 博客\_webgl 常用函数](https://blog.csdn.net/qw8704149/article/details/115152067)

[2022 年 WebGL 入门教程](https://www.bilibili.com/video/BV1Kb4y1x72q?p=1)

《WebGL 编程指南》

《计算机图形学导论---使用学习指南（WebGL 版）》

# WebGL 相关库

由于 WebGL 本身比较底层的使用方法，通常使用一些库来优化 WebGL 使用过程，如：

1. [Three.js](https://github.com/mrdoob/three.js#readme) ([Github](https://github.com/mrdoob/three.js)) is a lightweight 3D engine with a very low level of complexity — in a good way. The engine can render using ,  and WebGL. This is some info on [how to get started](http://aerotwist.com/tutorials/getting-started-with-three-js/), which has a nice description of the elements in a scene. And here is the Three.js [API documentation](https://github.com/mrdoob/three.js/wiki/API-Reference). Three.js is also the most popular WebGL library in terms of number of users, so you can count on an enthusiastic community ([#three.js on irc.freenode.net](http://webchat.freenode.net/?channels=three.js)) to help you out if you get stuck with something.
2. [PhiloGL](http://senchalabs.github.com/philogl/) ([Github](https://github.com/senchalabs/philogl)) is built with a focus on JavaScript good practices and idioms. Its modules cover a number of categories from program and shader management to XHR, JSONP, effects, web workers and much more. There is an extensive set of [PhiloGL lessons](http://www.senchalabs.org/philogl/demos.html#lessons) that you can go through to get started. And the [PhiloGL documentation](http://senchalabs.github.com/philogl/doc/index.html) is pretty thorough too.
3. [GLGE](http://www.glge.org/) ([Github](https://github.com/supereggbert/GLGE)) has some more complex features, like skeletal animation and animated materials. You can find a list of [GLGE features on their project website](http://www.glge.org/about/). And here is a link to the [GLGE API documentation](http://www.glge.org/api-docs/).
4. [J3D](https://github.com/drojdjou/J3D#readme) ([Github](https://github.com/drojdjou/J3D)) allows you not only to create your own scenes but also to export scenes from [Unity](http://unity3d.com/) to WebGL. The [J3D “Hello cube” tutorial](https://github.com/drojdjou/J3D/wiki/How-to-create-a-cube) can help you get started. Also have a look at this [tutorial on how to export from Unity to J3D](https://github.com/drojdjou/J3D/wiki/Unity-exporter-tutorial).

他们大多都提供了现成的模型，顶层着色器和片段着色器，这可以大大将减轻代码的编辑量。其大多数大多数都是基于 WebGL 创建直观的 3D 环境元素，如场景、摄像机、光源、环境光、现成的形状、材料、纹理和雾、悬浮粒子等效果。

