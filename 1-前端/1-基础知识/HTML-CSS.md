[前端汇总 (yuque.com)](https://www.yuque.com/cuggz/interview/famxgp)

# HTML

## Dom 节点的类型

整个文档是一个文档节点，整个元素是一个元素节点，元素里的 dom 是属性节点

## 单选框实现

```html
<!-- input的type属性为rado，同时那么相同 -->
<label for="one">
  <input id="one" type="radio" name="sex" value="male" />男
</label>
<label for="two">
  <input id="two" type="radio" name="sex" value="female" />女
</label>
```

## 语义化标签

我把语义化标签作为增加代码可读性，清晰页面结构的一种对 html 的编写规范

优点：1.css出了问题或者不兼容导致没有成功渲染dom，可以增加网页可阅读性 2.有利于SEO,有利于搜索引擎对网站的爬取 3.便于特殊化设备读取，例如盲人阅读器有利于盲人阅读

`<aside>`可用于侧边栏或者与附近内容相关的内容

`<header>`网页的页眉部分

`<main>`网页的主要部分

`<footer>`网页的页脚部分

`<nav>` 标签定义导航链接的部分。

`<figure>`用于文档中的图像

```html
<figure>
  <p>黄浦江上的的卢浦大桥</p>
  <img src="shanghai_lupu_bridge.jpg" width="350" height="234" />
</figure>
```

### 特殊标签

`<b></b>` 将字体变粗

`<big></big>` 将字体变大一号

`<wbr>` 确定一个长字符串的切换行的位置：

```html
<!--当页面宽度变化时会在wbr标签处换行-->
<p>abcde<wbr />fghigkl<wbr />mnpqrs<wbr />tuvwxyz</p>
```

`<code>和<pre>` code 标签的一个功能是暗示浏览器 code 标签所包围的文本是计算机源代码，浏览器可以做出自己的 样式处理，pre 标签则没有这项功能，但是 pre 标签可以保留文本中的空格和换行符，保留文本中的**空格**和**换行符**是计算机源代码显示 所必须的样式。 一般`code`和`pre`的嵌套使用为`<pre><code>hrllo world</code></pre>`

```html
<!--尝试空格带来的影响（发现只有pre会保留空格）-->
&lt;script type=&quot;text/javascript&quot; src=&quot;loadxmldoc.js&quot;&gt;
<br />
<code>
  &lt;script type=&quot;text/javascript&quot;
  src=&quot;loadxmldoc.js&quot;&gt;</code
>
<pre>
    &lt;script type=&quot;text/javascript&quot; src=&quot;loadxmldoc.js&quot;&gt;</pre
>
```

`<meta>`提供有关页面的元信息(meta-information)

```html
<!--以上代码告诉IE浏览器，IE8/9及以后的版本都会以最高版本IE来渲染页面。 -->
<meta http-equiv="X-UA-Compatible" content="IE=edge" />
<!--页面宽等于屏宽，缩放比等于1.0，防止出现横向滚动条-->
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<!--定义网页编码为gb2312-->
<meta http-equiv="Content-Type" content="text/html; charset=gb2312" />
<meta name="keywords" content="HTML,ASP,PHP,SQL" />
```

`<picture>` 设计多个图像来更好地填充浏览器视口

```html
<!--在650px及以上，采用iamge1.jpg，650px-465px，采用image2.jpg...-->
<picture>
  <source media="(min-width:650px)" srcset="/image1.jpg" />
  <source media="(min-width:465px)" srcset="/image2.jpg" />
  <img src="/image3.jpg" alt="Flowers" style="width:auto;" />
</picture>
```

`<progress>`显示程序的下载进度

```html
<progress value="45" max="100"></progress>
```

## href 和 src 的区别

href 标识**超文本引用**，用在 link 和 a 等元素上，href 是引用和页面关联，是在当前元素和引用资源之间建立联系

src 表示**引用资源**，表示替换当前元素，用在 img，script，iframe 上，src 是页面内容不可缺少的一部分

src 是 source 的缩写，是指向外部资源的位置，指向的内部会迁入到文档中当前标签所在的位置；在请求 src 资源时会将其指向的资源下载并应用到当前文档中，例如 js 脚本，img 图片和 frame 等元素。

```html
<script src="js.js"></script>
```

当浏览器解析到这一句的时候会**暂停**其他资源的下载和处理，直至将该资源加载，编译，执行完毕，图片和框架等元素也是如此，类似于该元素所指向的资源嵌套如当前标签内，这也是为什么要把 js 放再底部而不是头部。

```html
<link href="common.css" rel="stylesheet" />
```

当浏览器解析到这一句的时候会识别该文档为 css 文件，会下载并且**不会停止**对当前文档的处理，这也是为什么建议使用 link 方式来加载 css 而不是使用@import。



## 块级元素，行内元素

常见的块级元素：

`div`,`p`,`h1-h6`,`ol`,`ul`,`dl`,`table`,`form`

常见的内联元素：

`span`,`a`,`strong`,`i`

常见的内联块级元素：

`img`,`input`,`button`

## noscript的作用

noScript在不支持脚本或者支持脚本但是被禁用时会显示出来：

```html
<noscript>
	<p>
    本页面不支持脚本
    </p>
</noscript>
```



# CSS

## background-clip

设置背景颜色或图片，是否延伸，或者只出现在文字部分

[background-clip - CSS（层叠样式表） | MDN (mozilla.org)](https://developer.mozilla.org/zh-CN/docs/Web/CSS/background-clip)

用做渐变颜色字体和字体显示：（利用`background-clip: text`）

[image-clip (codepen.io)](https://codepen.io/wizardaei/pen/bGoYzaz)

## box-shadow

`box-shadow: h-shadow v-shadow blur spread color inset;`

| _h-shadow_ | 必需。水平阴影的位置。允许负值。         |
| ---------- | ---------------------------------------- |
| _v-shadow_ | 必需。垂直阴影的位置。允许负值。         |
| _blur_     | 可选。模糊距离。                         |
| _spread_   | 可选。阴影的尺寸。                       |
| _color_    | 可选。阴影的颜色。请参阅 CSS 颜色值。    |
| inset      | 可选。将外部阴影 (outset) 改为内部阴影。 |

box-shadow 是可以**叠加的**，而且在前面定义的属性会作为最上层阴影。

例如：`box-shadow: 4px 0px 0px 5px black inset, 4px 0px 0px 5px rgb(192, 20, 20), 5px 0px 0px 15px rgb(83, 202, 223);`

## vertical-align

[vertical-align - CSS（层叠样式表） | MDN (mozilla.org)](https://developer.mozilla.org/zh-CN/docs/Web/CSS/vertical-align) 用来指定行内元素（inline）或表格单元格（table-cell）元素的垂直对齐方。

## white-space: nowrap

文本框超出部分用...代替：

```css
span {
  white-space: nowrap;
}
```

## linear-gradient()

线性渐变函数，其参数表达：

```less
/* 100度角，从蓝色开始渐变、到40%位置是绿色渐变开始、最后以红色结束 */
linear-gradient(100deg, blue, green 40%, red);
```

## background-size: 宽 高;

利用 background-size 来定义背景图的长宽

## background-position

可能的值：

| 值                                                           | 描述                                                         |
| :----------------------------------------------------------- | :----------------------------------------------------------- |
| top lefttop centertop rightcenter leftcenter centercenter rightbottom leftbottom centerbottom right | 如果您仅规定了一个关键词，那么第二个值将是"center"。默认值：0% 0%。 |
| x% y%                                                        | 第一个值是水平位置，第二个值是垂直位置。左上角是 0% 0%。右下角是 100% 100%。如果您仅规定了一个值，另一个值将是 50%。 |
| xpos ypos                                                    | 第一个值是水平位置，第二个值是垂直位置。左上角是 0 0。单位是像素 (0px 0px) 或任何其他的 CSS 单位。如果您仅规定了一个值，另一个值将是 50%。您可以混合使用 % 和 position 值。 |

注：必须额外设置 background-attachment:fixed;才能保证该属性在 Firefox 和 Opera 中正常工作。

## clip-path 裁剪

`clip-path` CSS 属性，使用裁剪方式创建元素的可显示区域。区域的部分显示，区域外的隐藏

```css
clip-path:
clip-path: circle()  /*裁剪圆形或几分之一的圆*/
clip-path: ellipse() /*裁剪椭圆或几分之一的椭圆*/
clip-path: polygon() /*裁剪多边形*/
clip-path: url(resources.svg#c1); /*引入外部或内部的svg*/
clip-path: path() /*不太清楚*/
```

例子：

[CSS 中的路径裁剪样式 clip-path 总结 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/52493255)

[clip 和 clip-path inset-秋天爱美丽-专业的技术网站 (qiutianaimeili.com)](http://qiutianaimeili.com/html/page/2019/01/ad0bbbht85.html)

[【Apple 官网特效】iPhone SE 产品网页之颜色切换特效\_哔哩哔哩\_bilibili](https://www.bilibili.com/video/BV1rp4y1X7hT/?spm_id_from=333.788.videocard.4)

[clip 和 clip-path inset-秋天爱美丽-专业的技术网站 (qiutianaimeili.com)](http://qiutianaimeili.com/html/page/2019/01/ad0bbbht85.html)

## 响应式的处理方式：

### media query：

一种媒体查询方式，通过查询页面的宽度，在不同宽度下采用不同的 CSS 样式

```less
// Extra small devices (portrait phones, less than 576px)
// No media query for `xs` since this is the default in Bootstrap

// Small devices (landscape phones, 576px and up)
@media (min-width: 576px) {
  ...;
}

// Medium devices (tablets, 768px and up)
@media (min-width: 768px) {
  ...;
}

// Large devices (desktops, 992px and up)
@media (min-width: 992px) {
  ...;
}

// Extra large devices (large desktops, 1200px and up)
@media (min-width: 1200px) {
  ...;
}
```

### flex：

一种布局方式，伸缩盒模型:[flex - CSS（层叠样式表） | MDN (mozilla.org)](https://developer.mozilla.org/zh-CN/docs/Web/CSS/flex)

### rem

跟随 html 的根单位（font-size）的变化而变化，通常是用来解决文字的响应式问题的

### JS 通过对设备类型的检测转到不同页面

这种方法通常用来解决手机端和电脑端的类型有很大的不同的页面。具体策略：

1.初始进入的页面是 index.html,在 js 文件里加入获取**用户代理头**的方法 navigator.userAgent；其中便包括页面大小信息，使用正则表达式查询是否存在 Android|webOS|iPhone|iPod|BlackBerry 这些标识，标明是移动终端，否则是电脑端

2.采用 window.location.herf = "xx.html" 跳转到对应页面

### 自适应布局

不同的设备采用不同的页面，或采用局部自适应的方法

### 响应式布局

通过对 CSS 的设计，让一套代码可以在多端使用



## CSS 动画

### transition

语法形式：

`transition: property duration timing-function delay;`

最后一个 delay，定义的是过渡效果何时开始

### transform

**旋转 rotate**、**扭曲 skew**、**缩放 scale**和**移动 translate**以及**矩阵变形 matrix**。

### keyframes

```css
//关键帧的使用
@keyframes slidein {
  from {
    transform: translateX(10px);
  }
  to {
    transfrom: translateX(20px);
  }
}

@keyframes slidein {
  0% {
    top: 0;
    left: 0;
  }
  30% {
    ...;
  }
  68%,
  72% {
    ...;
  }
  100% {
    ...;
  }
}
```

```less
#alice {
  animation: aliceTumbling 3s ease-in-out;
  animation-fill-mod: forward; //动画停留在最后一帧
}
@keyframes aliceTumbling {
  0% {
    color: #000;
    transform: rotate(0) translate(-50%, -50%, 0);
  }
  30% {
    color: #431236;
  }
  100% {
    color: #000;
    transform: rotate(360deg) translate3D(-50%, -50%, 0);
  }
}
```

### 逐帧动画

将多张按帧变化的图片，并排排列成一个长图片。接着只露出长图片的第一张，之后按帧将图片向后移动，显示下一帧，从而形成图片。

```less
.sprite {
  position: abolute;
  height: 500px;
  width: 420px;
  animation: 0.9s run-h steps(17) infinite; //0.9s 17帧 重复播放
  backgroud-image: url(cartoon.png);
}
@keyframes run-h {
  to {
    background-position: -5880px 0; //最后的时候会显示最后一张图片
  }
}
//使得正好一帧一张图片
```

### js 动画函数封装

#### requestAnimationFrame(()=>{})

[window.requestAnimationFrame - Web API 接口参考 | MDN (mozilla.org)](https://developer.mozilla.org/zh-CN/docs/Web/API/Window/requestAnimationFrame)

[requestAnimationFrame 详解 - 简书 (jianshu.com)](https://www.jianshu.com/p/fa5512dfb4f5)

### 设计相关（设计网站:dribbble.com 2D: AE 3D: Blender）

![设计相关1](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/设计相关1.png)

### Lottie

一个可用于多端的库

通过 Bodymovin 解析 AE 等制作软件的动画，并导出可渲染动画的 json 文件



## 一个响应式的 banner 图:

```CSS
    .banner {
        height: calc(100vh - 71px);
        background-image: url(../assets/images/hd540/banner.png);
        background-position: center center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-size: cover;
    }
```

## BFC 是什么？如何触发 BFC

BFC 可以看作一个渲染容器，在渲染容器内对元素进行布局，不会影响容器和外面的元素。

常见的，如果不触发 BFC 会出现 margin 重叠，浮动元素高度塌陷，与兄弟元素重合等。

此时就可以使用 BFC 解决上面问题

- `overflow: hidden`（其实不为 visible 就行）
- `display:flex 或 inline-block`等
- `position:absolute 或 fixed`
- 根元素 html 或者浮动元素



## CSS @layer 是什么？

1. 可以重新定义 css 优先级（但是定义在`@layer{}`外的样式优先级更高）

   ```css
   /*
   * special 将生效，因为@layer将其声明在后面，即时special是先写的也会覆盖base
   */
   @layer base, special; 
   
   @layer special {
     .item {
       color: rebeccapurple;
     }
   }
   
   @layer base {
     .item {
       color: green;
     }
   }
   ```

2. 可以在 css 中 import 导入复用

3. 可以嵌套使用

[@layer - CSS（层叠样式表） | MDN (mozilla.org)](https://developer.mozilla.org/zh-CN/docs/Web/CSS/@layer#browser_compatibility)

## 超链接访问过后 hover 样式就不出现的问题是什么？如何解决？

主要是由于 css 样式中的优先级问题，可以采用以下优先级：

```css
a:link {
  ...;
}
a:visited {
  ...;
}
a:hover {
  ...;
}
a:active {
  ...;
}
```

## z-index什么时候生效

**仅适用于定位元素（位置：绝对、位置：相对、位置：固定或位置：粘性）和弹性项目（作为** [display:flex](https://www.w3schools.com/cssref/pr_class_display.asp)`z-index`元素的直接子 元素的元素）。并且父元素不设置`overflow: auto`

## CSS会不会阻塞页面渲染

1. css的解析和dom树的解析是并行的，所以并不会存在阻塞
2. dom树的渲染是需要css解析完才可以进行的，所以dom渲染是会被css阻塞的
3. 此外，如果css后面存在js代码，则css也会阻塞js代码的执行

[CSS到底会不会阻塞页面渲染](https://cloud.tencent.com/developer/article/1819747)

## CSS 引入方式 - link 和 @import 的区别

- link 是 HTML 提供的标签；@import 是 CSS 提供的语法规则。
- 加载页面时，link 标签引入的 CSS 被同时加载；@import 引入的 CSS 将在页面加载完毕后被加载。即动态加载。
- 浏览器对 link 的兼容性更高，@import 只可以在 IE5+ 才能识别。

## CSS 权重

- 引入方式上：行内引入>内嵌>外联

- 选择器：id选择器>伪类选择器>属性选择器>class选择器>标签选择器>通用选择器（*）

- 在同一级别上，对于一个dom的描述越精准的，权重越高，比如上面的属性选择器就是一种体现

- 并且同时还可以使用@layer来进行内部的权重排名，这时@layer外部的css是比内部权重高的
- !important 会打破选择器规则，成为最高优先级

## CSS in JS

在 JS 中维护 CSS 的方案。

[styled-components](https://styled-components.com/)

例子：

```jsx
// Create a Title component that'll render an <h1> tag with some styles
const Title = styled.h1`
  font-size: 1.5em;
  text-align: center;
  color: palevioletred;
`;

// Create a Wrapper component that'll render a <section> tag with some styles
const Wrapper = styled.section`
  padding: 4em;
  background: papayawhip;
`;

// Use Title and Wrapper like any other React component – except they're styled!
render(
  <Wrapper>
    <Title>
      Hello World!
    </Title>
  </Wrapper>
);
```

## css module

CSS Modules 通过自动给 CSS 类名补足类名，保证类名的唯一性，从而避免样式冲突的问题 。

举例（以react为例）：

```css
/* style.module.css */
.title {
	color: red;
}
```

```jsx
import HomeStyle from './Home/style.module.css'

export Home() {
    return (
    	<div className={HomeStyle.title}>
        	title
        </div>
    )
}
```



## 让网站变灰？给网站加滤镜

由于某些特殊原因，或者一些需求的特殊效果，需要我们在原有的页面上加上一层滤镜，那么我们就可以使用[filter - CSS（层叠样式表） | MDN (mozilla.org)](https://developer.mozilla.org/zh-CN/docs/Web/CSS/filter)或者[backdrop-filter - CSS（层叠样式表） | MDN (mozilla.org)](https://developer.mozilla.org/zh-CN/docs/Web/CSS/backdrop-filter)给元素或者元素后的背景加上滤镜。

例如，使得网站变灰，我们可以直接：

```css
body {
	filter: grayscale(1);
}
```



### CSS中括号的使用

标签属性选择器

      span[class='test']    =>匹配所有带有class类名test的span标签
    
      span[class *='test']  =>匹配所有包含了test字符串的class类名的span标签
    
      span[role]               =>匹配所有带有role属性的span标签
    
      [class='all']               =>匹配页面上所有带有class='all'的标签
    
      [class *='as']             =>匹配页面上所有class类且类名带有as字符串的类的标签



### 大小写规范

https://keqingrong.cn/blog/2021-05-29-case-sensitivity/



### CSS命名规范

https://juejin.cn/post/6844903672162304013



### 如何使用CSS保持盒子的横纵比

1. 使用`height: 0; padding:75%`来绘出一个4 : 3的盒子。如果需要在盒子里加内容，则盒子使用相对定位，内容盒子使用绝对定位。
2. 使用新属性`aspect-ratio`

https://juejin.cn/post/6844904070679887886
