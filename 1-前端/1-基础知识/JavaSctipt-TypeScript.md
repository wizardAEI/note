# JS汇总

## 基本类型和引用类型

基本类型是一种既非对象也无方法的数据

**基本类型**：string number bigint boolean null undefined symbol

**对象类型** ： 对象(Object)、数组(Array)、函数(Function)，还有两个特殊的对象：正则（RegExp）和日期（Date）。

他们之间的区别在于基本类型按值访问，引用类型按地址访问。这也导致了在用另一个变量等于这个变量时（a = b）的时候，基本类型会直接把值复制一份然后让 a 等于这个值，而引用类型则会让 a 指向 b 指向的地址。

同时，基本类型的是不允许被修改的，只允许赋值。比如`str = 'abc' str[0] = 'd'`这样是没有效果的，同时如果使用`"use strict"`还会报错

## JavaScript 的最大安全整数和最小安全整数

最大安全整数是 2^53 -1，最接近 0 的数是 5e-324，可以用 Number.MAX_VALUE 和 Number.MIN_VALUE 来表示

## 判断是否是数组

- `[] instanceof Array`；
- `Array.isArray()` ；
- 看原型链；
- `Object.prototype.toString.call([])`；
- ` Array.prototype.isPrototypeOf(obj)`

## let 对比 var 的区别

1. ES6 中，let 可以作为块级作用域的变量

ES6 之前，js 只用函数作用域和全局作用域，并没有块级的作用域，所以{}是没办法限定声明变量的范围的

```js
{
  var a = 5
}
console.log(a) >> 5
```

但是 let 则可以定义一个块级作用域

```js
{
    let a  = 5
    }
console.log(a)
>> eroor: a is not defined
```

2. `let`非常适合用于 `for`循环内部的块级作用域。JS 中的 for 循环体比较特殊，每次执行都是一个全新的独立的块作用域，用 let 声明的变量传入到 for 循环体的作用域后，不会受到闭包影响。看一个常见的面试题目：

```js
for (var i = 0; i <10; i++) {
  setTimeout(function() {  // 同步注册回调函数到 异步的 宏任务队列。
    console.log(i);        // 执行此代码时，同步代码for循环已经执行完成
  }, 0);
}
// 输出结果
10   共10个
// 这里面的知识点： JS闭包，setTimeout的机制等

//如果把 var改成 let声明：
// i虽然在全局作用域声明，但是在for循环体局部作用域中使用的时候，变量会被固定，不受外界干扰。
for (let i = 0; i < 10; i++) {
  setTimeout(function() {
    console.log(i);    //  i 是循环体内局部作用域，不受外界影响。
  }, 0);
}
// 输出结果：
0  1  2  3  4  5  6  7  8 9
```

3. let 没有变量提升，即使用某变量只能先定义再使用

   ```{
       b = 4
   
       console.log(b)
   
       let b
   
   }
   
   >>Uncaught ReferenceError: Cannot access 'b' before initialization
   ```

4. let 变量不能重复声明

## Object.keys()

```javascript
let obj = {
  qq: 'sss',
  ww: 'asda',
}
let arr = Object.keys(obj)
//arr ['qq','ww']
```

## 阻止默认事件和阻止事件传播

阻止默认事件

```js
DomEvent.preventDefault()
```

阻止事件传播(包括向上传播和向下传播)

```javascript
DomEvent.stopPropagation()
```

阻止事件冒泡并且阻止该元素上同事件类型的监听器被触发

```js
DomEvent.stopImmediatePropagation()
```

## JS 解构

[解构赋值 - JavaScript | MDN ](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment)

例子：

```
let arr = [1, 'xiaoming', { age: 18, sex: '男' }, { one: 11, two: 22 }]

let [index, theName, detail, phone] = arr
console.log(theName) //xiaoming

let { one } = phone //要与对象里的对应上
console.log(one)

//import {a,b} from 'demo.js'  import这种用法也涉及到了解构赋值
```

## 什么是闭包

闭包的特性在于：**函数可以访问它定义时所在作用域内的变量**。在使用闭包的过程就是找到一个作用域链形成一个闭包，**作用域链是由函数以及声明该函数的词法环境组合而成的**

[闭包 - JavaScript | MDN](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Closures)

[JavaScript 关于作用域、作用域链和闭包的理解\_Hello World-CSDN 博客\_js 作用域和作用域链 闭包](https://blog.csdn.net/whd526/article/details/70990994)

举例：

```javascript
let a = 1
function fn(num) {
  return num + a
}
fn(1) //2
//虽然fn内并没有a变量，但是在它所处的作用域内有a
```

## 原型链

以下是原型对象和原型链的解析视频，要注意的是，当我们在对象里找一个属性不存在的时候，会去 `对象`.\_\_proto\_\_里去找。

[JavaScript 原型对象 - Web 前端工程师面试题讲解\_哔哩哔哩\_bilibili](https://www.bilibili.com/video/BV117411v76o?t=491)

[JavaScript 原型链 - Web 前端工程师面试题讲解\_哔哩哔哩\_bilibili](https://www.bilibili.com/video/BV1N7411k7D2/?spm_id_from=333.788.videocard.0)

## `__proto__`和 prototype

```js
a
>>{name: 'xiaoming'}
a.__proto__.name = 'x'
a.name
>>'xiaoming'
a.__proto__.q = 'x'
a.q
>>'x'  //说明添加原型不会影响对象，但是找不到的属性会去原型上找



f
>>ƒ f() {
    console.log('x')}
f.prototype.name = 'x'
f.prototype.name
>>'x'    //函数使用prototype

//原型链
function a(){}
a.prototype.name = 'a'
function b(){}
b.prototype = a.prototype
let c = new s()
c.name
>> 'a'
```

## new

当我们执行 new 方法时，经历了如下步骤

`a = new A('xx')`

1. 创建一个空的简单 JavaScript 对象（即`{}`）；
2. 为步骤 1 新创建的对象添加属性`__proto__`，将构造函数的 prototype 放在对象的原型链上；
3. 将步骤 1 新创建的对象作为`this`的上下文 ，并执行构造函数；
4. 如果 **constructor** 函数没有返回对象，则返回 this。

## 变量提升

字面意思上说，即函数和变量的**声明**都可以移到代码最前面。

常见的变量提升：

```js
//函数提升
fun(2)
function fun(w) {
	console.log(w)
}
>> 2

//变量提升
num = 6;//初始化
console.log(num);
>> 6
var num;//声明
```

变量提升也适用于其他数据类型和变量。变量可以在声明之前进行初始化和使用。但是如果没有初始化，就不能使用它们。

可以看出，JavaScript 其实是**把声明提升了**，函数和变量相比，会被优先提升。这意味着函数会被提升到更靠前的位置。且函数中也会有嵌套的变量提升。

例：

```js
console.log(v1);
var v1 = 100;
function foo() {
    console.log(v1);
    var v1 = 200;
    console.log(v1);
}
foo();
console.log(v1);
>>
undefined
undefined
200
100
```

变量提升后可以写成这样：

```js
function foo() {
  var v1
  console.log(v1)
  v1 = 200
  console.log(v1)
}
var v1
console.log(v1)
v1 = 100
foo()
console.log(v1)
```

## 立即执行函数

[js 立即执行函数\_CSDN 博客](https://blog.csdn.net/y_silence_/article/details/82988477)

## 如何遍历对象

1. 使用 `for(key in obj)` 这种方法会把自身的和**原型链上**的所有可枚举属性都遍历出来
2. 使用 Object.keys() 返回属性数组，这种方法会返回对象自身所有可枚举的属性
3. Object.getOwnPropertyNames() 返回对象自身所有属性（**包括不可枚举**）
4. Reflect.ownKeys 返回所有自身属性（**包括 Symble**）
5. Object.entries()

[(1 条消息) 遍历对象*陌上浮屠的博客-CSDN 博客*遍历对象](https://blog.csdn.net/weixin_38788947/article/details/81840087)

使用`for in`如何避免使用到原型链上的属性呢? 可以使用 `myObj.hasOwnProperty(key)`来判断一个属性是否是自身的属性而不是继承来的。

## 单线程的 Javascript 为什么可以异步

[单线程的 Javascript 为什么可以异步 | F2E 前端技术论坛 (learnku.com)](https://learnku.com/articles/50935)

浏览器中的渲染进程分为主线程(JavaScript 线程引擎)和其他线程(GUI 渲染，定时触发器，事件触发，异步 HTTP 请求  定时器和HTTP请求都是多线程)

浏览器先去执行主线程，其他线程执行的回调加入到任务队列。主线程执行完后，去任务队列拿回调继续执行，从而实现异步处理

## ES6 新增的高级函数

```js
let goods = [5,7,10,40,20,15]

//返回一个新的数组，包含从 start 到 end （不包括该元素）的 arrayObject 中的元素。
arrayObject.slice(start,end)

//数组循环
for(let n of goods)
{
	console.log(n)
}//10 20

for(i in goods) console.log(i)
//0 1 2 3 4 5

//数组过滤函数
let goods1 = goods.filter(function(n){
    return n > 10
})//goods  [40,20,15]

//map映射
let goods1 = goods.map(function(n){
    return n * 0.5
})//goods1  [2.5,3.5,5,20,10,7.5]

//reduce汇总
let goods1 = goods.reduce(function(s,n) {
	return s + n
}))//goods1 = 97  （经过多次赋值后）
//其中s第一次为0，以后每次都为上次的函数返回值；n是数组遍历的值
//https://www.runoob.com/jsref/jsref-reduce.html


//some() every()等高级函数略

```

## 数组相关函数

[(1 条消息) Js 数组中的 concat(),join(),reverse(),sort()方法\_倾心\*的博客-CSDN 博客](https://blog.csdn.net/weixin_53056046/article/details/122930430)

## 任务队列（宏任务，微任务，Event-Loop）

在 JS 引擎中，我们可以按性质把任务分为两类，macrotask（宏任务）和 microtask（微任务）。

浏览器 JS 引擎中：

macrotask（按优先级顺序排列）: script(你的全部 JS 代码，“同步代码”）, **setTimeout**, **setInterval**, setImmediate(在一次 Event-Loop 后调用), I/O,UI rendering
microtask（按优先级顺序排列）: **Promises（这里指浏览器原生实现的 Promise）**, MutationObserver, window.queueMicrotask
JS 引擎首先从 macrotask queue 中取出第一个任务，执行完毕后，将 microtask queue 中的所有任务取出，按顺序全部执行；
然后再从 macrotask queue（宏任务队列）中取下一个，执行完毕后，再次将 microtask queue（微任务队列）中的全部取出；
循环往复，直到两个 queue 中的任务都取完。

而这个循环往复的过程就称作 EventLoop（当然实际情况会更复杂一些）

Tips：

NodeJS 引擎中：

先执行 script 中的所有同步代码，过程中把所有异步任务压进它们各自的队列（假设维护有 process.nextTick 队列、promise.then 队列、setTimeout 队列、setImmediate 队列等 4 个队列）
按照优先级（process.nextTick > promise.then > setTimeout > setImmediate），选定一个 不为空 的任务队列，按先进先出的顺序，依次执行所有任务，执行过程中新产生的异步任务继续压进各自的队列尾，直到被选定的任务队列清空。
重复 2...
也就是说，NodeJS 引擎中，每清空一个任务队列后，都会重新按照优先级来选择一个任务队列来清空，直到所有任务队列被清空。

## ES6 Set 和 Map

`Set`对象是值的集合，你可以按照插入的顺序迭代它的元素。 Set 中的元素只会**出现一次**，即 Set 中的元素是唯一的。

```js
//常用方法：
let obj = new Set() //创建Set对象
obj.add(10) //添加10  可以添加数，数组，字符串，对象等
obj.has(10) //判断是否有10
obj.clear() //清除
obj.delete(10) //清除set中的10这个元素
obj.forEach(value => {
  console.log(value)
}) //通过回调函数，来按顺序传回set的值
obj.size() //返回长度
let iterator1 = obj.values() //返回从头开始（并不是第一个元素，第一次的iterator1.next().value才是第一个元素）的一个迭代器 通过iterator1.next().value不断向后
```

`map` 键值对的集合

```js
//常用方法
let obj = new Map() //创建一个Map对象
obj.set('zero', 1)
obj.set('one', 'sss')
obj.set('two', [1, 2])
obj.set('three', {
  name: 'xiaowang',
}) //set   添加一组键值对，其形式多样，注意键值对是可以覆盖的
console.log(obj.get('zero')) //1
obj.delete('zero') //根据键删除对
obj.forEach(value => {
  cosole.log(value)
}) //按添加顺序输出值（不输出键）
obj.entries() //返回键值对形式的数组的迭代器用法类似于 obj.values()  ['zero',1]
```

## ES6 字符串相关

```js
//函数部分
s.starsWith('aa') //判断是否以aa开头并返回false或true
s.endsWith('aa') //判断是否以aa结尾

//...待更新

//模板字符串使用` `
let s = `
这个字符串可以换行
并且可以嵌入变量${n}
`
```

## ES6 扩展运算符

```js
//...
let arr = [1, 2, 3]
let arr2 = [...arr, 6, 7, 8]
console.log(arr2) //[ 1, 2, 3, 6, 7, 8 ]

function add(a, b, c) {
  return a + b + c
}
console.log(add(...arr)) //6

function f(...a) {
  console.log(a)
}
f(1, 2, 5) //[1,2,5] 参数可以自由设置多个，最终湖形成一个数组
```

## ES6 里新增了类的概念

[ES6 Class 类总结 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/55779174)

## 静态类型和动态类型

静态类型在初始化的时候就要有一个类型，动态类型只会在最后运行的时候才可以确定其类型

## ES6 模块化

1. 在 html 引用 js 的过程中，我们可以使用 type="module"来让某一个 js 链接独立形成闭包，可以让他的变量和其他 js 文件不冲突
2. 导出有 export 和 export default（只能在一个 module 里设置一个）

## import 和 require 的用法区别

#### 导入方法不同

import 只能用于静态导入，就是必须在文件开始的时候，在最上层就写好。而 require 就可以实现动态加载，可以写在任何地方。

例如：

```js
  data() {
    return  {
      imgSrc:require('assets/computer/办公本1.jpg')//可以
      //imgSrc:import('assets/computer/办公本1.jpg')//不行
    }
  }
```

## 引用的效果不同

ES6 模块

1. 不管是基础还是复杂的数据类型，都是对该变量的动态只读引用。动态在于一个模块中的变量变化会影响到另一个模块；只读在于某个模块引入一个变量的时候，不允许修改该变量的值。对于复杂数据类型，可以添加属性和方法，但是不允许指向另一个内存空间即指针不能改。

   ```js
   //a.js
   let number = 1
   setTimeout(()=>{
       number++
   },2000)
   export {number}
   //b.js
   import { number } from './a.js'
   console.log(number)
   //number += 1 会报错TypeError: Assignment to constant variable.
   setTimeout(()=>{console.log(number)},3000)
   
   >> 1
   >> 2
   说明是动态引用，但是是只读引用
   ```

2. 出现模块之间的循环引用时，只要模块存在某个引用，代码就可以执行。

CommonJS

1. 通过 require 引入基础数据类型时，属于复制该变量。

```js
// a.js
let count = 1
let setCount = () => {
  count = 2
}
setTimeout(() => {
  console.log('a', count)
}, 1000)
module.exports = {
  count,
  setCount,
}
// b.js
const obj = require('./a.js')
obj.setCount()
console.log('b', obj.count)

//node b.js
// b 1
// a 2
//count在b.js中复制了一份，setCount只改变了a.js中的count
```

2. 通过 require 引入复杂数据类型时，数据浅拷贝该对象。

```js
// a.js
let count = {
  num: 1,
}
let setCount = () => {
  count.num = 2
}
setTimeout(() => {
  console.log('a', count.num)
}, 1000)
module.exports = {
  count,
  setCount,
}
// b.js
const obj = require('./a.js')
obj.setCount()
console.log('b', obj.count.num)

//node b.js
// b 2
// a 2
//a.js和b.js中的值都发生了变化，说明是浅拷贝
```

3. 当使用 require 命令加载同一个模块时，不会再执行该模块，而是取到缓存之中的值。也就是说，CommonJS 模块无论加载多少次，都只会在第一次加载时运行一次，以后再加载，就返回第一次运行的结果，除非手动清除系统缓存。
4. 出现模块之间的循环引用时，会输出已经执行的模块，而未执行的模块不输出（比较复杂）
5. CommonJS 模块默认 export 的是一个对象，即使导出的是基础数据类型

## 异步中 async 和 await 的用法

在 Promise 前写上 await，整体函数是 async。这样函数返回就是一个 Promise，并且 `let f = new Promise(fn)`后，f 就是 then 或 catch 的返回值（前提是 Promise 不会抛错）。如果 Promise 会抛错，例如 catch 的就是一个 error，那么就需要用`try{}catch(err){}`

例如：

```js
try{
       	await f = new Promise(fn)
    	console.log(f)//如果没抛错，则打印Promise的返回值
      }
	  catch(err) {
       	console.log('抛错了')
      }
```

## apply()和 call()的用法

[快速理解 JavaScript 中 apply()和 call()的用法和用途 - SegmentFault 思否](https://segmentfault.com/a/1190000004581945)

个人的理解：apply()和 call()常用在改变对象的指向来实现方法的继承。或者一些对象通用的方法在不同的对象间进行调用。

举例：

```js
function animal(name, food) {
  ;(this.name = name),
    (this.food = food),
    (this.say = function () {
      console.log(name + ' likes ' + this.food + '.')
    })
}

function rabbit(name, food, other) {
  this.other = other
  animal.call(this, name, food)
}

let Judy = new rabbit('Judy', 'carrot', 'lala')

Judy.other // lala
Judy.say() // >>> Judy likes carrot.
```

在上述代码中，通过 call 函数，我们增加了 this 的参数；从而实现了类似于继承的效果。注意，如果我们在 call()函数之前在函数中定义了 call 的函数中会出现的参数，那么 call()函数会将 this 的参数进行覆盖。

而`apply()`和`call()`功能几乎一样，唯一的区别就是`apply()`第二个参数只能是数组，这个数组将作为参数传给原函数的参数列表`arguments`。

除了 this,我们当然也可以让某个对象继承另一个对象

例子

```js
let a = {
  name: 'a',
  like: '',
  f: function (x) {
    this.like = x
  },
}
a.f('apple')

let b = { name: 'b' }
a.f.call(b, 'banana')
console.log(a) //{name: 'a', like: 'apple', f: ƒ}
console.log(b) //{name: 'b', like: 'banana'}
```

相关教程 [【JS】两分钟说完 call, apply 和 bind\_哔哩哔哩\_bilibili](https://www.bilibili.com/video/BV1Ug411F7fZ?spm_id_from=333.999.0.0)

## this

由于 js 是运行时的，所以 JS 的 this 一般指的是在运行环境下（并非编译期）的当前对象。

**this 的指向和声明环境无关，完全取决于 this 运行时出现在哪个执行环境下。**

例：

```js
var name = '罗恩'
var aaa = {
  name: '哈利',
  say: function () {
    console.log(this.name)
  },
}

var bbb = {
  name: '赫敏',
  say: aaa.say,
}

var ccc = aaa.say

aaa.say() //哈利
bbb.say() //赫敏，由于执行时this所处环境在bbb
ccc() //罗恩，由于执行时this所处环境在全局
```

特殊的 this 情况（异步等情况）

例：

```js
var aaa = {
  name: '哈利',
  getName: function () {
    setTimeout(function () {
      console.log(this.name) //罗恩
    }, 100)
  },
}
```

由于异步执行，这里的 this 都是指向的 window 对象（回调时 this 丢失所以指向了 window）

为了放置折中问题，我们可以这样写：

```js
getName: function () {
        //在setTimeout外存储this指代的对象
        var that = this;
        setTimeout(function(){
            //this.name变成了that.name
            console.log(that.name);
        },100)
}
```

### 函数中的 this

this 是 js 的一个关键字，随着函数使用场合不同，this 的值会发生变化。但是总有一个原则，那就是 this 指的是调用函数的那个对象。即函数的 this 是由运行时的上下文确定的。

### 箭头函数的 this

箭头函数的 this 是声明时就确定的，而不是由运行环境决定，同时也不可以使用 call，apply 修改 this。与此同时，不用担心 settimeout，setinternal 的 this 丢失。

### 比较函数和箭头函数的区别

例子：

```js
let obj = {
  name: '哈利',
  getName: function () {
    setTimeout(() => {
      console.log(this.name)
    }, 0)
    setTimeout(function () {
      console.log(this)
    }, 0)
  },
}
obj.getName() // 箭头函数打印出了哈利 普通函数打印了一个Timeout对象
```

这个题目中，`getName`本身就是一个普通函数，又因为是使用 obj 调用的`getName`，所以这个函数的内的 this，指向的就是`obj`，又因为箭头函数使用的是声明时的 this，所以即时是延时打印也会打印出`哈利`

但是对于第二个`setTimeout`来说，其回调是一个普通函数，而这个函数在运行的时候，其运行时环境已经不再是 obj 的上下文了(因为其异步了)。所以他输出了一个 Timeout 对象。（由此也可知，此时的上下文为一个 Timeout 对象）

### js 最外层函数 this 的指向

在没有嵌套的函数里，this 指向是当前环境下表示全局的对象，在 node 环境下是 global，浏览器环境下是 window

## 函数柯里化（currying）

是把接受多个参数的函数变换成接受一个单一参数（最初函数的 第一个参数）的函数，并且返回接受余下的参数而且返回结果的新函数的技术。

```jsx
// 普通的add函数
function add(x, y) {
  return x + y
}

// Currying后
function curryingAdd(x) {
  return function (y) {
    return x + y
  }
}
add(1, 2) // 3
curryingAdd(1)(2) // 3
```

柯里化的作用:

1. 参数复用

```js
// 正常正则验证字符串 reg.test(txt)
// 函数封装后
function check(reg, txt) {
  return reg.test(txt)
}
check(/\d+/g, 'test') //false
check(/[a-z]+/g, 'test') //true
// Currying后
function curryingCheck(reg) {
  return function (txt) {
    return reg.test(txt)
  }
}
var hasNumber = curryingCheck(/\d+/g) //定义一个可以被复用的判断出现数字的正则表达式判别函数
var hasLetter = curryingCheck(/[a-z]+/g)
hasNumber('test1') // true
hasNumber('testtest') // false
hasLetter('21212') // false
```

2. 延迟执行：由于返回值是一个函数，那么这个函数可以放到后面延迟去执行

## addEventListener 和 attachEvent

创建监听的方法，不同的是 addEventListener 比较通用，IE 要使用 attachEvent

[JS addEventListener()和 attachEvent()方法：注册事件 (biancheng.net)](http://c.biancheng.net/view/5940.html)

## 事件捕获和事件冒泡

事件捕获是从外到内，先开始，然后事件冒泡，从里到外。

在 HTML 中处理事件是通过冒泡处理的。

.onclick 是冒泡处理的。

.addEventListener('click', fn) 默认是冒泡处理的

.addEventListener('click', fn, true) 第三个参数传入 true 时是捕获处理。

[JavaScript 事件捕获和事件冒泡 - Web 前端工程师面试题讲解\_哔哩哔哩\_bilibili](https://www.bilibili.com/video/BV1m7411L7YW?from=search&seid=6584018010257713198&spm_id_from=333.337.0.0)

## 原始类型和包装对象

由问题出发：

let s = 'xxxx'

为什么 s.length 会返回 4？

因为原始类型调用方法的时候会自动创建一个包装对象，而这个包装对象就是 String(),在调用后便会自动销毁

所以`s.length`实际是：

```
s.length -> new String('xxxx').length
```

## 浅拷贝和深拷贝

js 里的基本类型像`Number`,`String`,`Boolean`这些，他们在按值传递时，是直接传递值：

```js
let a = 5
b = a
b = 3
console.log(b,a)
>>3 5
```

而对象或数组之间的传值，则只是复制对象或数组的指针：

```js
let obj = {
  name: 'xxx',
  sex: 1,
}
let obj1 = obj
obj1.name = 'abc'
console.log(obj.name) >> abc
```

像这种传值，被称为浅拷贝。

如何实现对象的深拷贝呢？

1. `Object.assign(target, ...sources)`

   `Object.assign()`对多个源对象的**可枚举属性**进行**浅拷贝**。这样的特性可以让其实现深拷贝一层，而无法递归的深拷贝

   ```js
   var obj = { a: { a: 'hello', b: 21 }, b: 'xx' }
   var initalObj = Object.assign({}, obj)
   
   initalObj.a.a = 'changed'
   initalObj.b = 'ab'
   console.log(obj.b) //"xx" 实现了深拷贝
   console.log(obj.a.a) // "changed" 内层的还是浅拷贝
   ```

2. `JSON.stringify()和JSON.parse()`将对象转为字符串再转回来

   ```js
   var obj1 = { body: { a: 10 } }
   var obj2 = JSON.parse(JSON.stringify(obj1))
   obj2.body.a = 20
   console.log(obj1.body.a) // 10
   console.log(obj1 === obj2) // false 表明已经不是一个了
   ```

   这种办法比较简单，但是会抛弃对象的 constructor。也就是深拷贝之后，不管这个对象原来的构造函数是什么，在深拷贝之后都会变成 Object。

   这种方法能正确处理的对象只有 `Number, String, Boolean, Array, 扁平对象`，即那些能够被 json 直接表示的数据结构。RegExp 对象是无法通过这种方式深拷贝。

   也就是说，只有可以转成`JSON`格式的对象才可以这样用，像`function`没办法转成`JSON。`

   ```js
   var obj1 = {
     fun: function () {
       console.log(123)
     },
   }
   var obj2 = JSON.parse(JSON.stringify(obj1))
   console.log(typeof obj1.fun)
   // 'function'
   console.log(typeof obj2.fun)
   // 'undefined' <-- 没复制
   ```

3. 递归拷贝 （最终解决方案）

```js
//initalObj为被复制的对象
function deepClone(initalObj, finalObj) {
  var obj = finalObj || {}
  for (var i in initalObj) {
    if (typeof initalObj[i] === 'object') {
      //判断构造函数是不是Array即initalObj[i]是不是数组，注意判断数组不能用typeof，因为typeof [1,2,3] === 'object'
      obj[i] = initalObj[i].constructor === Array ? [] : {}
      arguments.callee(initalObj[i], obj[i]) //arguments.callee为自身这个function
    } else {
      obj[i] = initalObj[i]
    }
  }
  return obj
}
```

## 前端页面的三层结构

html 结构层 css 样式层 js 行为层

## Web worker

允许主线程创建 worker 线程，主线程运行的同时，worker 线程在后台运行，两者互不干扰。

[Web Worker 使用教程 - 阮一峰的网络日志 (ruanyifeng.com)](http://www.ruanyifeng.com/blog/2018/07/web-worker.html)

## [Mix-ins / 混入](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Classes#mix-ins_混入)

抽象子类或者 mix-ins 是类的模板。 一个 ECMAScript（JavaScript） 类只能有一个单超类，所以想要从工具类来多重继承的行为是不可能的。子类继承的只能是父类提供的功能性。因此，例如，从工具类的多重继承是不可能的。该功能必须由超类提供。

一个以超类作为输入的函数和一个继承该超类的子类作为输出可以用于在 ECMAScript 中实现混合：

```js
var calculatorMixin = Base =>
  class extends Base {
    calc() {}
  }

var randomizerMixin = Base =>
  class extends Base {
    randomize() {}
  }
```

使用 mix-ins 的类可以像下面这样写：

```js
class Foo {}
class Bar extends calculatorMixin(randomizerMixin(Foo)) {}
```

其实就是封装了一个方法，参数为要继承的类，返回一个继承了该类的衍生类

## generator **生成器**对象

```js
function* fn() {
  yield 1
  yield 2
}

let a = fn()

console.log(a.next())
console.log(a.next())
console.log(a.next())

// { value: 1, done: false }
// { value: 2, done: false }
// { value: undefined, done: true }  done的意思是是否迭代完了
```

同时，yield 也可以指向另一个生成器对象，从而实现递归的效果：

```js
let delegatedIterator = (function* () {
  yield 'Hello!'
  yield 'Bye!'
})()

let delegatingIterator = (function* () {
  yield 'Greetings!'
  yield* delegatedIterator
  yield 'Ok, bye.'
})()

// Prints "Greetings!", "Hello!", "Bye!", "Ok, bye."
for (let value of delegatingIterator) {
  console.log(value)
}
```

## `ScreenY`，`PageY`和，`clientY`的区别

一句话总结：pageY 是距文件，screenY 是获取显示器屏幕位置的坐标，clientY 是页面视口。

没有滚动条时，(pageY=clientY)+**浏览器菜单栏高度**=screenY；

有滚动条时，pageY>screenY>clientY，

因为 clientY 是页面视图距离，有无滚动条时你点屏幕的同一位置不会变化，screenY 也是。

但是 pageY 会随着滚动条的下拉而变大，因为它是距文件顶端的距离

## 事件监听，自定义事件，事件派遣

```js
// add an appropriate event listener
dom.addEventListener('cat', function (e) {
  process(e.detail)
})

// create and dispatch the event
let event = new CustomEvent('cat', {
  bubbles: true, //是否支持冒泡
  cancelable: true, //是否支持取消事件
  detail: {
    say: 'hello world',
  },
})
dom.dispatchEvent(event) // 执行事件
```

## JS 算数优先级

注意 `*` `/` `%` 算数优先级都是高于`+` `-`的。位运算的算术优先级都是更低的

## Object.defineProperty

`Object.defineProperty()`方法会直接在一个象上定义一个新属性或者修改一个属性的现有属性，并且返回此对象。他是实现观察者模式的一种工具

语法：`Object.defineProperty(obj, prop, descriptor)`

- `obj` 要定义属性的对象
- prop 要定义或修改的属性的名称或`Symbol`
- descriptor 要定义或修改的属性描述符

发挥至为被传递函数的对象

```
const object1 = {};

Object.defineProperty(object1, 'property1', {
  value: 42,
  writable: false
});

object1.property1 = 77;
// throws an error in strict mode

console.log(object1.property1);
// expected output: 42

```

**利用`Object.defineProperty()`实现对数据的监听**

```js
const prop = 'name'
const val = 'xiaowang'

obj = {
  name: val,
}

Object.defineProperty(obj, prop, {
  configurable: true, //默认是false，默认时属性值不可修改
  enumerable: true, //默认为false，默认时属性不会出现在枚举属性中
  get: () => val, //切记这里不能返回obj[prop]，不然会出现无限套娃
  set: newVal => {
    //执行fn
    console.log(newVal)
    val = newVal
  },
})
```

这样我们就实现了对 obj[prop]的监听，一旦 obj[prop]发生变化，set 中的 fn 就可以采取相应的操作，而如果我们想监听所有属性，则可以使用`Object.keys()`遍历

## arguments 和剩余运算符

**`arguments`** 是一个对应于传递给函数的参数的类数组对象。 （来源于 MDN）

举例：

```js
const fn = function () {
  console.log(arguments)
}
fn(2, 3, 5) //[Arguments] { '0': 2, '1': 3, '2': 5 }
```

我们可以用这种方法动态的获取参数。

但是**箭头函数**是没有 arguments 的，但是可以通过剩余运算符来替代：

```js
const fn = (...arr) => {
  console.log(arr)
}
fn(2, 3, 5) // [ 2, 3, 5 ]
```

## TypedArray 类型

TypedArray 并不是一个类名，他仅仅代表着一个类型集合的总称。

TypedArray 可以是以下类型：

- Int8Array
- Unit8Array
- Unit8ClampedArray
- Int16Array
- Unit16Array
- Int32Array
- Unit32Array
- Float32Array
- Float64Array
- BigInt64Array
- BigUint64Array

上述类型中的数字表示了 TypedArray 中每个元素的所占的比特位数，如 Int8Array，每个元素占 8 个 bit，即一个字节。

[TypedArray - JavaScript | MDN (mozilla.org)](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/TypedArray)

## js 对象键值的特点

```js
let obj = {}
obj[1] = 'ac'
console.log(obj['1']) //'ac'
```

这说明使用这种键值对的命名时，即使是`obj[1]=...`，但是在内部使用其实还是字符串

## 对象遍历器

js 之所以可以遍历数组，Map，Set 等数据结构，是由于这些对象统一实现了`Symbol.iterator`接口，该接口是一个定义在 Symbol 原型上的属性，其对应的值通常为一个函数。

我们可以利用这一个特点，给普通的对象自定义一个 iterator 接口，从而让该对象可以被遍历：

```js
var obj = {
  0: 'a',
  1: 'b',
  2: 'c',
  length: 3,
  [Symbol.iterator]: Array.prototype[Symbol.iterator],
}
```

我们复用了 Array 的 iterator 接口，并且使对象的键名从 0 开始的连续数字，同时设置了 length 属性，从而可以使用 Array 的 iterator 接口：

```js
for (let item of obj) {
  console.log(item)
}
// a b c
```

## use strict

严格模式，可以用来限制没有声明就使用变量

## WeakMap

WeakMap 是为了解决传统 map 的 get 和 set 操作都是 On 的复杂度(比较大)和不可被垃圾机制回收的两个缺点而诞生的
WeakMap 的键是对象，值随意。为 WeakMap 是弱引用，所以他保证了当没有其他引用的时候键值对会被垃圾回收。
WeakMap 的基本用法：

```js
const wm1 = new WeakMap(),
const o1 = {}, o2 = function() {}, o3 = window;
wm1.set(o1, 37);
wm1.set(o2, 'azerty');
wm1.get(o2); // "azerty"
wm1.has(o2); // true
wm1.has(o1); // true
wm1.delete(o1);
wm1.has(o1); // false
```

## 搞清 CommonJS、AMD、CMD、ES6 的联系与区别

[记笔记：搞清 CommonJS、AMD、CMD、ES6 的联系与区别\_寒烟说的博客-CSDN 博客](https://blog.csdn.net/hanyanshuo/article/details/110134788)

### export.\_\_esModule

简单来说就是由于历史包袱，如果模块中既出现了 Commonjs 又出现 es6 模块，打包会出现兼容问题。为了避免这个问题，一般会使用声明`export.__esModule`表示导出对象为一个 ES 模块来避免这个问题

[\_\_esModule 的作用 | Toyo (toyobayashi.github.io)](https://toyobayashi.github.io/2020/06/29/ESModule/)

## ES6 函数

1. 参数默认值

   ```js
   function fn(a = 2, b = 1) {
     return a + b
   }
   ```

   默认参数只有在为传递参数或者参数为 undefined 的时候，才会使用默认参数，null 值被认为是有效的值传递。

2. rest 参数(...变量名)代替 arguments 去处理多余参数

   ```js
   function fn() {
     return arguments
   }
   function fn2(...numbers) {
     return numbers
   }
   ```

   rest 参数只能作为最后一个参数，类似`fn(a, ...b, c)`是不可以的

3. name 参数

   ```js
   function foo() {}
   foo.name // es5和es6都会返回"foo"
   const fn = function() {}
   fn.name // "fn" 由于是匿名函数，es5的name会返回'fn'
   function foo() {}
   bind返回的函数，name会加上bound前缀
   foo.bind({}).name // "bound foo"
   (function() {}).bind({}) // "bound "
   ```

4. 箭头函数

   ```js
   //提示一些可能出错的地方
   //当箭头函数只有一个返回时，不用加{}，如果要返回一个对象，为了区分于代码块，需要加括号
   let f = (id, name) => ({ id, name })
   ```

   箭头函数中没有`this`，`super`，`arguments`和`new.target`，箭头函数中的 this 是定义函数时的对象，区别于普通函数，普通函数的 this 取决于使用函数时的对象。

## ES6函数使用技巧

### Array.prototype.filter()

`filter`方法返回一个新数组，包含通过**测试函数**的元素

例如，返回arr数组中所有大于2的元素，组成新数组：

```js
[1,2,3,4,11,-2,1].filter(item => item > 2)
// [3, 4, 11]
```



### Array.prototype.some()

`some()` 方法测试数组中是不是至少有 1 个元素通过了被提供的函数测试。它返回的是一个 Boolean 类型的值。

```js
const array = [1, 2, 3, 4, 5];
const even = (element) => element % 2 === 0;
array.some(even) //true
```



### &&和||的使用技巧

`&&`和`||`会在执行时有不同的效果：

```js
(代码段1) && (代码段2) // 这里如果第一个代码段为真，才会执行下一个代码段
(代码段1) || (代码段2) // 这里如果第一个代码段为假，也会执行下一个代码段
```

`&&`和`||`会在返回时有不同的效果：

```js
(代码段1) && (代码段2) // 这里如果第一个代码段为真，则返回第二个代码段，否则返回第一个代码段
(代码段1) || (代码段2) // 这里如果第一个代码段为假，则返回第二个代码段，否则返回第一个代码段

如：
true && "" // 返回""
false && true //返回false
"" || undefined // 返回undefined
```





## js 判断触底

当滚动条在 Y 轴的滚动距离+浏览器视口的高度 = 文档的总高度 的时候

```js
//滚动条在Y轴上的滚动距离
function getScrollTop() {
  var scrollTop = 0,
    bodyScrollTop = 0,
    documentScrollTop = 0
  if (document.body) {
    bodyScrollTop = document.body.scrollTop
  }
  if (document.documentElement) {
    documentScrollTop = document.documentElement.scrollTop
  }
  scrollTop =
    bodyScrollTop - documentScrollTop > 0 ? bodyScrollTop : documentScrollTop
  return scrollTop
}

//文档的总高度
function getScrollHeight() {
  var scrollHeight = 0,
    bodyScrollHeight = 0,
    documentScrollHeight = 0
  if (document.body) {
    bodyScrollHeight = document.body.scrollHeight
  }
  if (document.documentElement) {
    documentScrollHeight = document.documentElement.scrollHeight
  }
  scrollHeight =
    bodyScrollHeight - documentScrollHeight > 0
      ? bodyScrollHeight
      : documentScrollHeight
  return scrollHeight
}

//浏览器视口的高度
function getWindowHeight() {
  var windowHeight = 0
  if (document.compatMode == 'CSS1Compat') {
    windowHeight = document.documentElement.clientHeight
  } else {
    windowHeight = document.body.clientHeight
  }
  return windowHeight
}

window.onscroll = function () {
  if (getScrollTop() + getWindowHeight() == getScrollHeight()) {
    var more = document.getElementById('more')
    more.style.display = 'none'
  } else {
    var more = document.getElementById('more')
    more.style.display = 'block'
  }
}
```

## video 的播放暂停和定位

```javascript
const video = documen const vedio = document.getElementById('bannerVideo')
vedio.currentTime = 0 //定位
vedio.pause() //暂停
vedio.play() //播放
```



# 22 年笔试题/面试题总结（基础篇）

## 作用域

```js
var b = 3
(function () {
  b = 5
  var b = 2
})()
console.log(b)
```

输出值为 3，考点在于 function 是个函数作用域

## 闭包

```js
function f() {
  var num = 1
  return () => {
    num++
    return num
  }
}
var a = f(),
  b = f()
a(), b()
```

输出都为 2，因为相当于创建了两个闭包，也可以尝试一下`a === b`，其结果为 false。

## 变量提升和 let

```js
function fn() {
  console.log(name)
  console.log(age)
  var name = 'sss'
  let age = 24
}
fn()
```

结果为`undefined，ReferenceError`，其变量提升后相当于：

```js
function fn() {
  var name //var进行了变量提升，但只是初始化，赋值还是在后面
  console.log(name)
  console.log(age)
  name = 'sss'
  let age = 24 //let没有变量提升
}
fn()
```

注意 let 是没有变量提升的，所以会出现`ReferenceError`

## 重写 promise.all

写一个数组来存储 resovle，当 resolve 长度等于 promise 的数组时说明全部 resolve 了；否则出现一个 reject 就 reject

```js
Promise.mayAll = function (arr) {
  let resArr = []
  return new Promise((resolve, reject) => {
    arr.forEach(item => {
      item.then(res => {
        resArr.push(res)
        if (resArr.length == arr.length) {
          resolve(resArr)
        }
      })
      item.catch(err => {
        reject(err)
      })
    })
  })
}

const a = new Promise((res, rej) => {
  setTimeout(() => {
    console.log(1)
    rej('a')
  }, 100)
})

const b = new Promise((res, rej) => {
  setTimeout(() => {
    console.log(2)
    res('b')
  }, 50)
})

Promise.mayAll([a, b])
  .then(res => {
    console.log('final res: ', res)
  })
  .catch(err => {
    console.log('final err: ', err)
  })
```

## js call，apply，bind 方法的区别

共同点：

1. 都用来改变 this 的指向
2. 第一个参数都是 this 要指向的对象
3. 都可以利用后续参数传参。

不同点：

1. 调用返回不同，传参形式不同，例如使用`myAdd`方法：

   ```js
   const body = {
   	sum: 1
   }
   myAdd = function(a, b ,c) {
   	this.sum += (a + b + c)
   }
   myAdd.call(body, 1, 2, 3)  //call会直接调用myAdd方法，后续参数对应函数参数
   
   myAdd.apply(body, [1, 2, 3]) //apply也会直接调用myAdd方法，后续的数组对应函数参数
   
   const bodyAdd = myAdd.bind(body, 1, 2, 3) //bind方法不会直接执行myAdd方法，而是返回更改this后的新函数，参数形式同call
   bodyAdd()
   
   三种方法执行后body都会变成 7
   ```

## 重写 js call 方法和 js bind 方法

重写 call 方法：

```js
//首先验证传入的obj是不是function或者object，然后为obj名命一个属性赋值当前this，即函数本身；然后使用obj执行
Function.prototype.myCall = function (obj, ...params) {
  if (/^function|object$/.test(typeof obj)) {
    const key = Symbol('key')
    obj[key] = this
    obj[key](...params)
    delete obj[key] //删除属性
  } else {
    //错误处理
  }
}
```

重写 bind 方法：

```js
//直接套娃，使用箭头函数，this还是指的当前函数
Function.prototype.myBind = function (obj, ...params) {
  if (/^function|object$/.test(typeof obj)) {
    return () => {
      this.myCall(obj, ...params)
    }
  }
}
```

## setTimeout 和 Promise

### 如题：

```js
setTimeout(() => {
  console.log('1')
  new Promise(() => {
    console.log('2')
    Promise.resolve().then(res => {
      console.log('2.5')
    })
  })
}, 0)

setTimeout(() => {
  console.log('3')
}, 0)
```

应该如何输出？

答案：1 2 2.5 3

关键在于宏任务和微任务。setTimeout 是典型的宏任务，而 promise 则是一个微任务。

### 如题：

```js
setTimeout(function () {
  console.log(1)
}, 0)
new Promise(function execulor(resolve) {
  console.log(2)
  for (var i = 0; i < 10000; i += 1) {
    i == 9999 && resolve()
  }
  console.log(3)
}).then(function () {
  console.log(4)
})
console.log(5)
```

输出： 2 3 5 4 1 先把异步放到后面，又因为异步中先执行 promise（微任务）后执行 setTimeout（宏任务）



## setTimeout Promise async

如题：

```js
async function fn() {
    console.log(1)
    await fn2()
    console.log(3)
}
async function fn2() {
    console.log(2)
}

fn()

console.log(4)

;(new Promise((res, rej) => {
    console.log(5)
    res(6)
})).then(res => {
    console.log(res)
})

setTimeout(() => {
    console.log(7)
}, 0)
```

答案：

```
1
2
4
5
3
6
7
```

## DNS 的具体流程

通过域名会由 DNS 服务器(其地址在网络设置里已经配置好了)首先找到根域名，然后找到顶级域名服务器的地址，再通过顶级域名服务器找到域名的地址

## js 的 CurrentTarget 和 target 的区别

当事件处理程序注册的元素**等于**事件的实际目标元素的时候，e.target 和 e.currentTarget 以及 this 三者相同。 当事件处理程序注册的元素**不等于**事件的实际目标元素的时候，e.currentTarget 和 this 两者相同，但 e.target 不与这两者相同。

currentTarget / this：事件处理程序注册的元素。
target：事件的实际目标元素。

## 事件委托

事件委托就是让父节点监听事件(比如 onclick 之类的)，然后当子节点触发事件的时候，由于冒泡的机制，父组件也会触发，那么此时可以利用`e.target`来找到真正触发事件的 dom 对象，从而实现将事件委托给父节点，触发事件后再去找子节点。这种用法可以保证在 list 里不用每个子节点都写一个事件。

## 如何判断 dom 节点的类型

使用`el.nodeType`可以，他会返回数字来区分 dom 类型

使用`el.nodeName`也可以返回 string 来区分 dom 类型

## 如何判断一个字符(或字符串)是否为数字？

- `isNaN`: 判断是否为**非数字**

```js
isNaN(1) //false
isNaN('121') //false
isNaN('123aa') //true
```

isNaN()的缺点就在于 null、空格以及空串会被按照 0 来处理

- **使用正则表达式** /^[0-9]+.?[0-9]\*$/
- 使用`parseFloat`

```js
parseFloat('a1') //NaN
parseFloat('123.22aas') //12.22
parseFloat('12a3.22aas') //12
//然后和原变量比一下是否相等
```

`parseFloat`缺点在于，只要首位是数字，不管后面是什么都会保留是数字的部分。

## `typeof`和`instanceof`的区别

`typeof`返回字符串，表明其后跟的表达式的类型。它可以返回 6 种基本类型，但是`typeof null`会返回 `object`,这属于一个历史遗留问题。其他的引用类型，除了 function 可以判断出，其他的都返回`object`

`instanceof` 用来检验构造函数(类)的 prototype 是否出现在变量的原型链上

instanceof 可以判断出 typeof 判断不明确的类型，例如：

```js
typeof [] //object
[] instanceof Array //true
```

并且，利用`toString`也可以实现对类型的判断：

```js
Object.prototype.toString.call([])
//[object Array]
```

## JavaScript 变量在内存中的具体存储形式

- 基本数据类型：栈内存
- 引用数据类型：指针在栈内存，内容在堆内存

## js 中的基础类型如字符串为什么可以使用 charAt()等方法呢？

是因为基础类型 string，number，boolean 是有对应的 String Number Boolean 的**包装类型**的，当对一个字符串使用`str.charAt(1)`,其实隐式地执行了一个装箱的操作：

```js
const temp = new String(str)
temp.charAt(1)
temp = null
```

所以基础变量才可以使用方法

对应的，将通过 String 等类型 new 出来的变量，也可以通过`toString`和`valueOf`方法变成基础类型。这一操作成为拆箱。

## 为什么 undefined >= undefined 为 false，而 null >=null 为 true

因为这里发生了隐式转换，其中 undefined 转换为了`NaN`，`NaN`既不等也不大于`NaN`；而 null 隐式转换成了 0

## 0.1 + 0.2 == 0.3 错误的原因？

由于 JavaScript 会有精度问题，所以 0.1 + 0.2 = 0.30000000000000004。防止精度出现问题可以通过保留小数点的形式，例如保留五位小数 `parseFloat((0.1 + 0.2).tofixed(5))`

## 在浏览器种的弹出框类型：

alert，confirm，prompt

## 创建一个对象的几种方式

1. new Object

   ```js
   const obj = new Object()
   obj.val = 1
   ```

2. 字面量

   ```js
   const obj = { val: 1 }
   ```

3. 工厂函数

   ```js
   function createObj(val) {
     const obj = new Object()
     obj.val = 1
     return obj
   }
   ```

4. 构造函数

   ```js
   function Obj(val) {
     this.val = val
   }
   const obj = new Obj(1)
   ```

## 什么是 BOM？和 DOM 的关系？

BOM 是浏览器对象模型，提供了很多操作浏览器和查看浏览器信息的功能，最上层是 window 对象，提供了 window.history(用来操纵浏览器的历史记录)，window.location(操作文档和 URL)等

BOM 可以通过 API 访问到 DOM 对象并对其进行操作（可以说是包含关系）

拓展： 文档对象模型 (DOM) 是 HTML 和 XML 文档的编程接口。它提供了对文档的结构化的表述，并定义了一种方式可以使从程序中对该结构进行访问，从而改变文档的结构，样式和内容。DOM 将文档解析为一个由节点和对象（包含属性和方法的对象）组成的结构集合。简言之，它会将 web 页面和脚本或程序语言连接起来。 一个 web 页面是一个文档。这个文档可以在浏览器窗口或作为 HTML 源码显示出来。但上述两个情况中都是同一份文档。文档对象模型（DOM）提供了对同一份文档的另一种表现，存储和操作的方式。 DOM 是 web 页面的完全的面向对象表述，它能够使用如 JavaScript 等脚本语言进行修改。

## 暂时性死区？

我认为暂时性死区是指在一个代码块中（函数作用域或者块作用域中），如果使用 const 或者 let 声明了变量，那么就会形成一个封闭的作用域，在这个作用域内，引用的变量必须是作用域内声明的(或即将声明的)变量，即使外部已经有声明的变量。
暂时性死区可能会导致报错，如：

```js
let a = 2
function fn() {
  console.log(a)
  let a = 1
}
fn()
//Cannot access 'a' before initialization 报错
```

## script, script async, script defer 的区别

主要区别在于 html 解析过程

script：html 解析中遇到 script 标签就会暂停解析，转而去**解析**和**执行**script 中的 js 代码

script async：js 文件**异步解析**，当解析完成后，hml 暂停解析去**执行**js 代码

script defer：js 文件**异步解析**，当 html 解析完成后，再去**执行**js 代码

## 什么是 compose？如何实现一个 compose？

compose 函数是为了应对多重的函数嵌套而出现的, 例如：

```
const fn1 = (x) => { return x + 1 }
const fn2 = (x) => { return x * 2 }
const fn3 = (x) => { return x - 1 }
fn3(fn2(fn1(2))) //5
```

像这种嵌套，使用 compose 就可以变成这样：`composeFn(fn1, fn2, fn3)(2)`

那么如何实现一个 compose 函数呢？可以利用 reduce

```js
function composeFn(...fns) {
  return function (initVal) {
    return fns.reduce((ret, fn) => {
      return fn(ret)
    }, initVal)
  }
}
composeFn(fn1, fn2, fn3)(2) //5
```

注意，compose和高阶函数并不同。



## function.length？

`function.length`是指到最后一个必须要传入的参数位置，一共要传递几个参数。例如：

```js
const fn = function (a, b, c) {
  return 1
}
fn.length //3
const fn2 = function (...a) {
  return 1
}
fn2.length //0
const fn3 = function (a = 1, b = 2, c) {
  return 1
}
fn2.length //0
const fn4 = function (a, b = 2, c) {
  return 1
}
fn2.length //1
const fn5 = function (a, b, c = 2) {
  return 1
}
fn2.length //2
```

## forEach 想个办法跳出循环，并传递参数

答：使用 try...catch 包裹，需要跳出的时候`throw Error(data)`

## window.location.replace("https://baidu.com")和window.location.href = "https://baidu.com"的区别

都可以在当前页面跳转到百度，但是一种无法返回到上一次跳转。即没有将上一页存放在 history 中

## 发布订阅者模式

```js
// 消息中心
const topic = {
  eventList: {},
  /**
   * @description 订阅
   * @param {string} event 事件名词
   * @param {function} callback 订阅触发的回调，也就是订阅者
   */
  on(event, callback) {
    //这个事件的回调push到事件数组里(事件数组不存在就初始一个空数组)
    ;(this.eventList[event] || (this.eventList[event] = [])).push(callback)
  },
  /**
   * @description 发布
   * @param {string} event 事件名词
   * @param  {...any} arr 携带的参数
   */
  emit(event, ...arr) {
    this.eventList[event] &&
      this.eventList[event].forEach(fn => {
        fn(...arr)
      })
  },
}

//分别对a事件订阅三次
topic.on('a', data => {
  console.log('1', data)
})
topic.on('a', data => {
  console.log('2', data)
})
topic.on('a', data => {
  console.log('3', data)
})
//发布
topic.emit('a', '订阅到了')
//1 订阅到了 2 订阅到了 3 订阅到了
```

## 手写 AJAX

ajax 是用的 xhr(XMLHttpRequest)封装的，所以需要使用到 xhr 相关方法

```js
const ajax = {
  get(url, callback) {
    const xhr = new XMLHttpRequest()
    xhr.open('GET', url) //建立连接
    //onreadystatechange相当于一个钩子函数，监听readstate的变化
    xhr.onreadystatechange = () => {
      xhr.readyState === 4 && callback(xhr.responseText) // 当readyState是4的时候表明数据传输完成且有回调了
    }
    //发送请求
    xhr.send()
  },
  post(url, data, callback) {
    const xhr = new XMLHttpRequest()
    xhr.open('POST', url)
    xhr.onreadystatechange = () => {
      xhr.readyState === 4 && callback(xhr.responseText)
    }
    xhr.send(data)
  },
}
```

## 最全的垂直居中方法

- padding 设置上下内边距
- line-height 设置行距 = 盒子高度
- flex，grid 布局
- position:absolute 并且 top:50% transform:translateY(-50%)
- 将需要对齐的元素设置 block-align 再设置一个高度为外边盒子的高度，宽度为 0 的对照 block-align 元素，之后设置 vertical-align:middle

[CSS 垂直居中 - Web 前端工程师面试题讲解\_哔哩哔哩\_bilibili](https://www.bilibili.com/video/BV167411y7m5?spm_id_from=333.337.search-card.all.click)

## 手写 Promise

```js
class MyPromise {
  static PENDING = '待定'
  static FULLFILLED = '成功'
  static REJECT = '拒绝'
  resolveCallbacks = []
  rejectCallbacks = []
  constructor(func) {
    this.status = MyPromise.PENDING //promise状态
    this.result = null //resolve或者reject的返回
    try {
      func(this.resolve, this.reject)
    } catch (err) {
      this.reject(err)
    }
  }
  resolve = res => {
    this.status === MyPromise.PENDING && (this.status = MyPromise.FULLFILLED)
    this.result = res
    this.resolveCallbacks.forEach(callback => {
      callback(res)
    })
  }
  reject = res => {
    this.status === MyPromise.PENDING && (this.status = MyPromise.REJECT)
    this.result = res
    this.rejectCallbacks.forEach(callback => {
      callback(res)
    })
  }
  then = (onFULFLILED, onREJECTED) => {
    if (this.status == MyPromise.PENDING) {
      //当发生异步的时候先把then回调存起来
      onFULFLILED && this.resolveCallbacks.push(onFULFLILED)
      onREJECTED && this.rejectCallbacks.push(onREJECTED)
    }
    if (this.status === MyPromise.FULLFILLED) {
      setTimeout(onFULFLILED(this.result)) //模拟异步，但是这个是宏任务，真正的promise是微任务
    }
    if (this.status === MyPromise.REJECT) {
      setTimeout(onREJECTED(this.result))
    }
  }
}

let promise = new MyPromise((res, rej) => {
  setTimeout(() => {
    res('x')
  }, 1000)
}).then(res => {
  console.log(res)
})
```

## Object.entries 和 Object.fromEntries 的用法

`Object.entries`：返回对象的键值对二维数组

`Object.fromEntries`：根据键值对二维数组生成对象（注意此时对象必须是迭代的）

## Array.prototype.flat()怎么用

扁平化数组到一维数组，当不传入参数的时候默认是一层，传入`infinity`表述任一层

[Array.prototype.flat() - JavaScript | MDN (mozilla.org)](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Array/flat)

```js
var arr3 = [1, 2, [3, 4, [5, 6, [7, 8, [9, 10]]]]]
console.log(arr3.flat(2)) //[ 1, 2, 3, 4, 5, 6, [ 7, 8, [ 9, 10 ] ] ]
```

## 在浏览器中 let，const，class 声明后可以在 window 对象上找到吗？

不可以，只有 var 声明的对象才可以在 window 对象上看到，而 let，const，class 会被放在 Script 对象上，它和 global 对象同级，而 global 包含了 window。

[let 和 const 声明的变量到底去哪里了？ - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/114128108)

## 什么是词法环境，用来做什么的

词法环境，可以说是进行参数分析，登记参数声明，变量声明，函数形参声明的地方。 词法环境是在代码定义的时候决定的，跟代码在哪里调用没有关系。所以说 JavaScript 采用的是词法作用域（静态作用域）。

词法环境由两个部分组成：

- 对外部词法环境的引用（作用域链可以连起来的关键）
- 环境记录（用于记录词法环境中的标识符与变量的映射）

对于**全局词法环境**来说，它的对外部词法环境的引用为 null，环境记录可以分为**声明式环境记录**和**对象式环境记录**：

- 声明式环境记录：let const class 等（包括除了全局函数和 var 的其他声明）
- 对象式环境记录：包括 var 声明和全局函数声明，其特点在于**绑定**，绑定的对象是当前对象

对于函数词法环境来说，他的对外部词法环境的引用主要看声明的情况。其环境记录为对象环境记录
举个例子：

```js
var a = 2
let x = 1
const y = 5

function foo() {
  console.log(a)

  function bar() {
    var b = 3
    console.log(a * b)
  }

  bar()
}
function baz() {
  var a = 10
  foo()
}
baz()
```

其语法环境为：

```js
// 全局词法环境
GlobalEnvironment = {
    outer: null, //全局环境的外部环境引用为null
    GlobalEnvironmentRecord: {
        //全局this绑定指向全局对象
        [[GlobalThisValue]]: ObjectEnvironmentRecord[[BindingObject]],
        //声明式环境记录，除了全局函数和var，其他声明都绑定在这里
        DeclarativeEnvironmentRecord: {
            x: 1,
            y: 5
        },
        //对象式环境记录，绑定对象为全局对象
        ObjectEnvironmentRecord: {
            a: 2,
            foo:<< function>>,
            baz:<< function>>,
            isNaNl:<< function>>,
            isFinite: << function>>,
            parseInt: << function>>,
            parseFloat: << function>>,
            Array: << construct function>>,
            Object: << construct function>>
            ...
            ...
        }
    }
}
//foo函数词法环境
fooFunctionEnviroment = {
    outer: GlobalEnvironment,//外部词法环境引用指向全局环境
    FunctionEnvironmentRecord: {
        [[ThisValue]]: GlobalEnvironment,//this绑定指向全局环境
        bar:<< function>>
    }
}
//bar函数词法环境
barFunctionEnviroment = {
    outer: fooFunctionEnviroment,//外部词法环境引用指向foo函数词法环境
    FunctionEnvironmentRecord: {
        [[ThisValue]]: GlobalEnvironment,//this绑定指向全局环境
        b: 3
    }
}

//baz函数词法环境
bazFunctionEnviroment = {
    outer: GlobalEnvironment,//外部词法环境引用指向全局环境
    FunctionEnvironmentRecord: {
        [[ThisValue]]: GlobalEnvironment,//this绑定指向全局环境
        a: 10
    }
}

```

[JS：深入理解 JavaScript-词法环境 (limeii.github.io)](https://limeii.github.io/2019/05/js-lexical-environment/)

[深入 JavaScript 系列（一）：词法环境 - 掘金 (juejin.cn)](https://juejin.cn/post/6844903733495595016)

## 为什么 let 和 const 不可以变量提升

mdn 里说明过：let 是**声明一个块级作用域的本地变量**，并且存在一个暂时死区，通过 `let` 声明的变量直到它们的定义被执行时才初始化。

从执行角度来说，执行步骤为：

1. 创建一个**新的执行上下文（Execution Context）生成一个**新的词法环境（Lexical Environment）

2. 将该执行上下文的 **变量环境组件（VariableEnvironment）如 var 声明的变量**和 **词法环境组件（LexicalEnvironment）如 let 声明的组件** 都指向新创建的词法环境

3. 将该执行上下文 **推入执行上下文栈** 并成为 **正在运行的执行上下文**

4. 对代码块内的**标识符进行实例化及初始化**

5. **运行代码**

6. 运行完毕后**执行上下文出栈**

在第四步中同时出现了变量提升和暂时死区，即变量环境组件(var)会被初始化，从而发生了变量提升。而词法环境组件则仅被实例化，但不会被初始化，运行到声明代码处才被初始化。

## 滚动视差是什么？

滚动视差是指让多层背景以不同的速度移动，形成立体的运动效果 。可以通过`background-attachment:fixed`或者`transform:translate3D`实现

[滚动视差？CSS 不在话下 - ChokCoco - 博客园 (cnblogs.com)](https://www.cnblogs.com/coco1s/p/9453938.html)

## es6 如何异步加载模块

使用`import().then`来异步加载

```js
//a.js
export const fn = val => val + 1
```

```js
//b.js
import('./a').then(module => {
  console.log(module.fn(2)) //3
})
```

## 如何做一个卡片翻转效果（3D 效果）

主使用`transform: rotate(deg)`来进行翻转

## 做一个随机排序

1. 从一个 array 中随机取出一个元素，并从原 array 中去除。一直到 array 取尽。

2. 假设 array 一共有 n 个元素。第一次将第 n 个元素和前 n-1 个元素中的随机一个元素交换，第二次将第 n-1 个元素和前 n-2 个元素中的随机一个元素交换...知道最后全部交换完成，得到新数组。

## 类私有变量怎么写

_a 或者闭包 或者使用symbol 或者 #：

[js私有变量的实现](https://segmentfault.com/a/1190000017081250)

## 大文件上传实现和断点续传怎么实现

**大文件上传：**核心是利用`Blob.prototype.slice`方法，将文件切成更小的切片，记录好每个切片的顺序发送给后端，并在发送完成后发出合并请求通知后端合并；后端根据顺序将文件还原（这里可以使用 Nodejs 的 读写流（readStream/writeStream），将所有切片的流传输到最终文件的流里）

**断点续传：**主要思路是要前端/后端记住已经上传的切片，从而跳过已经上传的部分

- 前端使用 localStorage 记录已上传的切片 hash
- 服务端保存已上传的切片 hash，前端每次上传前向服务端获取已上传的切片

这里的hash值，可以通过文件内容进行计算，常见的npm包是spark-md5

[实现一个大文件上传和断点续传](https://juejin.cn/post/6844904046436843527)



## fori forEach forin 的效率差距

结论: forin明显慢于另外两者，fori和foreach看浏览器的处理（firfox中forEach更快一点，chrome中fori更快一点）

并且理论上 while是会比for更快的，虽然在浏览器上看差距不大

其他的像`map`和`reduce`等方法，由于需要有返回值的缘故，时间效率更差一点



## 手机端如何实现细边框(0.5px)和网页端如何实现小字体(12px以内)

**手机端如何实现细边框:**

1. 直接设置 border-width: 0.5px；使用方便，但兼容性很差，不推荐使用。
2. 用阴影代替边框，设置阴影box-shadow: 0 0 0 .5px #000; 使用方便，能正常展示圆角，兼容性一般。
3. 给容器设置伪元素，设置绝对定位，高度为1px，背景图为线性渐变，一半有颜色，一半透明。视觉上宽度只有0.5px。这种方法适合设置一条边框，没法展示圆角。
4. 给容器内设置伪元素，设置绝对定位，宽、高是200%，边框是1px，然后使用transform: scale(0.5) 让伪元素缩小原来的一半，这时候伪元素的边框和容器的边缘重合，视觉上宽度只有0.5px。这种方法兼容性最好，4个边框都能一次性设置，能正常展示圆角，**推荐使用**。

[手机上如何实现细/1px/0.5px边框](https://zhuanlan.zhihu.com/p/340711204)

**网页端如何实现小字体: **

手机端的浏览器会根据浏览器本身的设计限制最小字体号(比如1px)，但网页版的浏览器一般都会限制最小字体12px，为了显示更小的字体，我们可以采用以下方法：使用缩放 如`transform: scale(0.5)`，但是如果这个属性影响到了整个元素的高宽，那么我们可以加上display:inline-block;使得当前元素没有宽高。并使用transform-origin设置缩放原点。

还有一个问题：浏览器如何浏览手机端可以设置的12px以下的字体





## 如何实现长度是100元素都为0的数组

1. `(new Array(100)).fill(0)` 

   相关语法：

   ```js
   // Array的构造函数用法
   new Array(element0, element1, /* … ,*/ elementN)
   new Array(arrayLength)
   //fill() 方法用一个固定值填充一个数组中从起始索引到终止索引内的全部元素。不包括终止索引。
   fill(value) //全部元素
   fill(value, start)
   fill(value, start, end)
   ```

2. `Array.from({ length: 100 }, (x) => 0);`

   form语法：

   > [Array.from() - JavaScript | MDN (mozilla.org)](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Array/from)

3. map函数。



## 使用setinterval做轮询有什么问题？

setinterval函数作为一个用来定时循环执行的函数，他有一个特点就是只有当计算机空闲时，才会执行.而下一次触发时间则是在setInterval回调函数执行完毕之后才开始计时,所以如果setInterval内执行的计算过于耗时,或者有其他耗时任务在执行,setInterval的计时会越来越不准,延迟很厉害.

```js
let startTime = new Date().getTime();
let count = 0;
//耗时任务
setInterval(function(){
    let i = 0;
    while(i++ < 100000000);
}, 0);
setInterval(function(){
    count++;
    console.log(new Date().getTime() - (startTime + count * 1000));
}, 1000);
// 尝试该段代码可以发现延迟越来越厉害
```

为了在js里可以使用相对准确的计时功能,我们可以在代码里,通过1000(也就是周期时间)减去当前时间和准确时间的差距,来算出下次触发的时间,从而修正了当前触发的延迟.

```js
let startTime = new Date().getTime();
let count = 0;
setInterval(function(){
    let i = 0;
    while(i++ < 100000000);
}, 0);
function fixed() {
    count++;
    let offset = new Date().getTime() - (startTime + count * 1000);
    let nextTime = 1000 - offset;
    if (nextTime < 0) nextTime = 0; 
    setTimeout(fixed, nextTime);
     
    console.log(new Date().getTime() - (startTime + count * 1000));
}
setTimeout(fixed, 1000);
```

但是当耗时函数太耗时了，超过生命周期了，这个偏移函数就会出问题，我们此时也只能使用`if (nextTime < 0) nextTime = 0; `来尽量避免延迟了。



## for in 如何只遍历自身

我们可以在遍历的时候通过`Object.prototype.hasOwnProperty()`来判断这个元素是不是自己的

```js
for(let item in obj) {
	if(obj.hasOwnProperty(item)) {
		...
	}
}
```





## Reflect的receiver的作用

[Reflect.get() - JavaScript | MDN (mozilla.org)](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Reflect/get)

例子：

```js
const parent = {
  name: "parent",
  get value() {
    return this.name;
  },
};

const handler = {
  get(target, key, receiver) {
    return Reflect.get(target, key); // 或者直接target[key]
  },
};

const proxy = new Proxy(parent, handler);

const obj = {
  name: "son",
};

// 设置obj继承与parent的代理对象proxy
Object.setPrototypeOf(obj, proxy);

console.log(obj.value);
```

此时返回的是`parent`

如果我们传入`receiver`的话，相当于更改了this值：

```js
const handler = {
  get(target, key, receiver) {
    return Reflect.get(target, key, receiver); // 或者直接target[key]
  },
};
```

此时返回`son`



## 柯里化和compose函数的区别	



柯里化的作用在于，当参数不能一起传入或者参数不确定的时候，柯里化可以使一个函数返回函数并继续传参，例如add(1, 2)(3)

compose则是对高阶函数的扁平化处理，即`ans(mul3(add1(add1(0))))` => `compose(ans, mul3, add1, add1)`



## 如何终止XMLHttpRequest和Fetch

XMLHttpRequest:

**方法一：xhr.abort() 调用中止api**

xhr 就是 XMLHttpRequest 的实例，该实例调用对应的xhr.abort() 会终止当前的请求。

```
var xhr = new XMLHttpRequest();
xhr.open('get', 'https://jianshu.com', true);
xhr.send();
xhr.onreadystatechange= function (){
console.log(xhr.responseText, '-- respone')
}
setTimeout(() => {xhr.abort()}, 20);
```

fetch:

[Fetch：中止（Abort） (javascript.info)](https://zh.javascript.info/fetch-abort)



## 隐式转换

javascript隐式转换规则
隐式类型转换是在一定场景下，js 运行环境自动调用这几个方法，尝试转换成期望的数据类型：

- ToString
- ToNumber
- ToBoolean
- ToPrimitive

### ToString

这里所说的 ToString 可不是对象的 toString 方法，而是指其他类型的值转换为字符串类型的操作

- null：转为 "null"
- undefined：转为 "undefined"
- 布尔类型：true 和 false 分别被转为 "true" 和 "false"
- 数字类型：转为数字的字符串形式，如 10 转为 "10" ， 1e10 转为 "10000000000"
- 数组：相当于调用数组的 Array.prototype.join() 方法，如 [1, 2, 3] 转为 "1,2,3"，空数组 [] 转为 '' 空字符串，数组中的 null 或 undefined ，会被当做 '' 空字符串处理
- 普通对象：相当于直接使用 `Object.prototype.toString()`，返回 "[object Object]"

### ToNumber

ToNumber 指其他类型转换为数字类型的操作

null： 转为 0

undefined：转为 NaN

字符串：如果是纯数字形式，则转为对应的数字，空字符转为 0 , 否则一律按转换失败处理，转为 NaN

布尔型：true 和 false 被转为 1 和 0

### ToBoolean

`ToBoolean` 指其他类型转换为布尔类型的操作

js 中的假值只有 `false`、`null`、`undefined`、`''空字符`、`0` 和 `NaN`，其它值转为布尔型都为 `true`

### ToPrimitive

ToPrimitive 指对象类型（如：对象、数组）转换为原始类型的操作。

当对象类型需要被转为原始类型时，它会先查找对象的 `valueOf` 方法，如果 `valueOf` 方法返回**原始类型**的值，则 ToPrimitive 的结果就是这个值
如果 `valueOf` 不存在或者 `valueOf` 方法返回的不是原始类型的值，就会尝试调用对象的 toString 方法，也就是会遵循对象的 ToString 规则，然后使用 toString 的返回值作为 ToPrimitive 的结果。

### 运算符中的隐式类型转换

下面只介绍常用的几种：

#### 一元 +

```js
+1  // 1

+‘1’ // 1

+‘-1’ // -1

+{} // NaN

+[] // 0;

+[1] // 1;

+[1, 2] // NaN
```

#### 二元 +

二元加法运算符 + 可以对两个数字做加法，也可以做字符串连接操作，如果其中一个操作数是字符串或者隐式转换为字符串的对象，另外一个操作数将会转换为字符串，加法将进行字符串的连接操作；否则会尝试转换成数字进行相加。 这里只说明加法是因为只有加法

```js
1 + 2 //  3: 加法

"1" + "2" //  "12": 字符串连接

"1" + 2 //  "12": 数字转换为字符串后进行字符串连接

1 + +'1' // 2 : 第二个+相当于数学中的正号

1 + {} //  "1[object Object]": 对象转换为字符串后进行字符串连接

{} + 1 // 1 浏览器解析成了 {}; + 1

a = {} + 1 // "1[object Object]"

'1' + true //  "1true": 布尔值转换为字符串后进行字符串连接

true + true //  2: 布尔值转换为数字后做加法

2 + null //  2: null转换为0后做加法

2 + undefined //  NaN: undefined转换为NaN后做加法

1 + 2 + " blind mice"; //  "3 blind mice"

1 +（2 + " blind mice"）; //  "12 blind mice"
//需要注意的是，“++”运算符从不进行字符串连接操作，它总是会将操作数转换为数字并增1。表达式++x并不总和x=x+1完全一样
let x = '1'
++x //  2: 
```

#### 关系运算符 ==

规则：

null == undefined为true 除此之位 null 和 undefined 和其他相 == 都是false

对于数字和字符串的抽象比较，将字符串进行 ToNumber 操作后再进行比较
对于布尔值和其他类型的比较，将其布尔类型进行 ToNumber 操作后再进行比较
对于对象和基础类型的比较，将对象进行 ToPrimitive 操作后在进行比较
**当类型相同时，直接去比较。当类型都是引用类型时，例如两个数组相比，则看其引用地址是否相等**
下面来看几个例子：

```js
true == '1'       // true
/**
  * 布尔类型和其他类型比较适用规则2，true通过ToNumber操作转换为1
  * 这时候1 == '1'，这时候适用规则1，将'1'通过ToNumber操作转换为1
  * 1 == 1 所以输出为true
  **/
let obj = {
    valueOf: function() { return '1' }
}
true == obj      // true
/**
  * 首先适用规则2，将true转换为1，此时1 == obj
  * 此时适用规则3，将obj转换为'1'，此时1 == '1'
  * 此时适用规则1，将'1'转换为1，此时1 == 1，所以输出true
  **/
[] == ![]      // true
/**
  * 一般直觉这明细是false，但我们仔细看一下
  * ![]先对[]进行强制boolean转换，所以实际上应该是[] == false
  * 这样就又回到我们刚刚的规则上了，适用规则2所以[] == 0
  * 接着适用规则3，所以 '' == 0
  * 最后 ToNumber('')  == 0
    **/
// 特例
NaN == NaN        // false
null == undefined // true，属于ecma规范
```



## 在react组件中一个元素绑定onClick事件，点击后总会向上传播，如何阻止冒泡？

React 为提高性能，有自己的一套事件处理机制（合成事件），相当于将事件代理到全局进行处理，也就是说监听函数并未绑定到DOM元素上。因此，如果你禁止react事件冒泡`e.stopPropagation()`，你就无法阻止原生事件冒泡（但可以阻止react的组合事件冒泡）；你禁用原生事件冒泡`e.nativeEvent.stopPropagation()`，React的监听函数就调用不到了。

解决方案：

判断`event.target`对象，是否是目标对象、或包含的对象、或被包含的对象，来决定是否触发事件。

例如：

```js
handleClick (e) {
    if(e.target.nodeName === 'li'){
        // do something
    }
    if(contains(this.root, e.target)){
        // do something
    }
}
```

当然，对于一般的合成事件来说，我们阻止其冒泡，使用`e.stopPropagation()`就可以解决问题。



## 如何捕获异步错误？

```js
window.addEventListener('unhandledrejection', (e) => {
    console.log('unhandledrejection', e.reason)  // 注意这里不打印
}, false)

window.addEventListener('rejectionhandled', (e) =>  {
    console.log('rejectionhandled', e.reason)
})

window.addEventListener('error', (e) => {
    console.log('error', e)
})

const p  = new Promise((res, rej) => {
    // throw new Error()
    rej('xxxx')
})
setTimeout(() => {
    p.catch(e => {
        console.log(e)
    })
}, 1000)
```

## window.onerror 和window.addEventListener('error')的区别

首先对于所有的`onxxx`和`addEventListener('xxx')`，都是onxxx绑定的函数先被触发。

同时`onxxx`绑定的事件，如果重新赋值函数，则会只执行最新的函数；对于`addEventListener('xxx')`来说，绑定了多个事件的触发函数，则最终都会执行

具体的，window.onerror绑定的触发函数接收多个参数，`addEventListener('error')`只有一个参数：

```js
window.onerror = (...e) => { //多个参数可以使用剩余参数语法
    console.log('onError', e)
}

window.addEventListener('error', (e) => {
    console.log('error', e)
})

throw new Error('xxx')

```



## bind可以修改箭头函数this参数吗？为什么

不可以，因为bind是用来修改运行时的this指向的，而箭头函数的this是在编译期间就被定义好是谁的，所以不会被修改。相反，普通函数的this是在运行时才会确定的，所以可以被修改。



## bind之后的函数还可以在被call或者apply修改吗

bind之后无法改变this的指向，当执行绑定函数时，this指向与形参在bind方法执行时已经确定了。

```js
const objA = {
    val: 'a'
}

const objB = {
    val: 'b'
}

const testFuncBind = (function(arg) {
    console.log(this)
    console.log(arg)
}).bind(objA, 1)

testFuncBind() // { val: 'a' }  1
testFuncBind.apply(objB, [2]) // { val: 'a' }  1
```

和上面的题联系起来，能否改变this其实就是看在改变this时当前的this指向有没有被确定下来。



##  Promise.all 和 Promise.race 传入空数组

```js
Promise.all([]).then((res) => {
    console.log('all');
});
Promise.race([]).then((res) => {
    console.log('race');
});
// all会立刻输出， race则不会输出（说明Promise.race([])一直处于pending状态）
```



## WebRTC

[WebRTC网页即时通信_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1nb4y1i7bR/?spm_id_from=333.788&vd_source=9f4f5fa0ddf7994dab77edc934f59978)

WebRTC 即时网络通信 （web Real-Time Communicate）

WebRTC 是一个支持浏览器进行实时语音对话或者视频对话的API

允许浏览器之间**直接连接** （与websocket的不同点）

### WebRTC连接过程：

在建立连接之前，浏览器之前显然没有办法传递数据。所以我们需要先通过服务器（信令服务器）的中转传递一些信令信息（如通信开启或关闭的的连接控制信息，建立安全连接的关键数据等），然后建立浏览器的点对点连接。

### 如何建立WebRTC

由于NAT（网络地址转换）的影响，我们没办法直接获取一个客户端的公网ip，所以此时，我们可以使用Stun服务器来获取客户端自身公网ip来建立点对点或端对端连接（即P2P  Peer to Peer）。

当个P2P失败时，我们就通过TURN服务器进行中间转发（此时的方式就类似于websocket了）

对应流程图：

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20221107164949.png)

（注意，当我们使用Stun服务器获取到公网ip，并且p2p连接成功时就不需要Turn服务器去转发了）

### 多对多通讯方案：

Mesh方案:两两之间进行连接，形成网状结构 （流量消耗大）

MCU方案：由一个服务器将音视频进行混流并进行转发，多个用户和该服务器进行通信（服务器压力大）

SFU方案：与MCU不同，SFU是直接将音视频转发。（带宽大）

### 相关的库

`socket.io`



## js调用栈的执行方法

- js函数执行时回将函数加入调用栈，当执行函数体时，遇到另一个函数的执行或者递归时，则将该函数继续加入调用栈（压入栈，在其父函数上边），进入函数继续执行。

- 知道一个函数执行结束后，将该函数从调用栈中取出。



## 柯里化

function` ` add(x) {________}; alert(add(2)(3)(4)); //填空，使结果为9

```js
function add(a) {
  if (!isFinite(add.i)) {
    add.i = a
  } else {
    add.i += a;
  }
  // 重写函数方法
  add.valueOf = add.toString = function () {
    return add.i
  }
  return add;
}
alert(add(2)(3)(4))
```



# Typescript

## 类型注解

```typescript
//这里的str表明必须传递string类型的变量，否则会报错
function fun(str: string) {
  console.log(str)
}
```

## 基础类型

#### Ts 的基础类型：

```
boolean  //布尔 true false

number   //数字

string   //字符串

undefined null //默认情况下null和undefined是所有类型的子类型，但是如果想把其赋值给某个类型的变量，想要不报错首先要关闭严格模式

number[] string[] 等 数据类型[]  或  Array<number> Array<string> 等 Array<数据类型>   //数组

let a:[string,number,boolean] = ['xxx',12,true]  //元组  与数组不同的是可以存在不同类型,但是数据类型的位置和个数要一一对应

enum //枚举

any //任何类型

unknown //任何类型的安全形式

void //没有类型,如 function f:void () { ... } 无返回值

never //函数无法返回的类型，例如一个会抛出异常的函数 就可以写 function f(msg:string):never {throw new Error(msg)}

any[] //不确定个数，不确定类型的数组，但是不好的地方是就没有实时的编译提示了

object //对象

类型一|类型二	  //联合类型，同时接受多种类型

(<string>str).length  或  (str as string).length //类型断言，断言某个变量是某种类型，以防止报错。 这个为例，断言str是string类型，所以在提前不知道str的类型的情况下，使用.length方法也不会报错

//例子：
let str:string = 'abc'
```

#### 枚举

`enum`类型是对 JavaScript 标准数据类型的一个补充。 像 C#等其它语言一样，使用枚举类型可以为一组数值赋予友好的名字。

```
enum Color {Red, Green, Blue}
let c: Color = Color.Green;
```

默认情况下，从`0`开始为元素编号。 你也可以手动的指定成员的数值。 例如，我们将上面的例子改成从`1`开始编号：

```
enum Color {Red = 1, Green, Blue}
let c: Color = Color.Green;
```

或者，全部都采用手动赋值：

```
enum Color {Red = 1, Green = 2, Blue = 4}
let c: Color = Color.Green;
```

枚举类型提供的一个便利是你可以由枚举的值得到它的名字。 例如，我们知道数值为 2，但是不确定它映射到 Color 里的哪个名字，我们可以查找相应的名字：

```
enum Color {Red = 1, Green, Blue}
let colorName: string = Color[2];
alert(colorName);  // 显示'Green'因为上面代码里它的值是2
```

#### Tips:

- TS 是支持不同类型的变量进行拼接的

## 接口

一种类似于类型注解的约束

#### 基本使用

```typescript
interface Iperson {
  firstName: string
  lastName: string
}
function showFullName(person: Iperson) {
  return person.firstName + person.lastName
} //这里的函数传入的参数，必须同时具备firstName,lastName两种属性，但是多具备其他属性则不做要求
let q = {
  firstName: 'xx',
  lastName: 'x',
  qq: 'aa',
}
showFullName(q)
```

#### 详细使用

```typescript
//例子：person对象的约束：
//id是number，必须有，只读；name是string，必须有；age是number类型，必须有；sex是string类型，可以没有;

//定义一个接口类型
interface Person {
	readonly id: number
	name: string
	age: number
	sex?: string
    [propName: string]: number //索引，表明新增的string类型的属性值可以为number
}

//约束person对象
const person:Person = {
id:1,
name:'xxx',
age:18,
sex:'fmale'
abcd: 1234 //利用索引新创建的值
}
```

#### 接口的函数类型

```typescript
interface SearchFunc {
  (source: string, subString: string): boolean
}

let mySearch: SearchFunc
mySearch = function (source: string, subString: string) {
  let result = source.search(subString)
  return result > -1
}
```

#### 类类型

```typescript
interface ClockInterface {
  currentTime: Date
  setTime(d: Date)
}

interface Name {
  name: string
  setname(pname: string)
}

class Clock implements ClockInterface, Name {
  name: 'xxx'
  currentTime: Date
  setTime(d: Date) {
    this.currentTime = d
  }
  setname(pname: string) {
    this.name = pname
  }
  constructor(h: number, m: number) {} //构造函数类是接口不约束的
}
```

#### 继承

```typescript
interface nameAndClock extends ClockInterface,Name {...} //{ }加上新增的内容
```

类和构造器

```typescript
class Greeter {
  greeting: string
  constructor(message: string) {
    this.greeting = message
  }
  greet() {
    return 'Hello, ' + this.greeting
  }
}

let greeter = new Greeter('world')
```

## 

## 类型推断

TS 会在没有明确的说明类型时，根据声明或者在第一次使用的时候，根据赋值的类型来自行推断数据类型

## 类

typescript 中的类的定义：

```typescript
class Greeter {
  greeting: string
  constructor(message: string) {
    this.greeting = message
  }
  greet() {
    return 'Hello, ' + this.greeting
  }
}

let greeter = new Greeter('world')
```

#### 继承:

```
class Animal {
    move(distanceInMeters: number = 0) {
        console.log(`Animal moved ${distanceInMeters}m.`);
    }
}

class Dog extends Animal {
    bark() {
        console.log('Woof! Woof!');
    }
}

const dog = new Dog();
dog.bark();
dog.move(10);
dog.bark();
```

#### 共有和私有

```js
//默认成员为共有，但是也可以在成员前加上public表示公用
//private表示私有，不可在外部直接访问，也不能在派生类中访问
//protected修饰符，不可以在外部直接访问，但是可以在派生类中访问

class Animal {
    private name: string;
    constructor(theName: string) { this.name = theName; }
}

new Animal("Cat").name; // 错误: 'name' 是私有的.
```

#### readonly 修饰符

- 对类中的属性成员的修饰符，此时成员可以在外部被查看但不能被更改，但是内部额可以进行更改
- 特殊用法：在构造函数的参数中，对参数用 readonly 修饰，可以看作在类中有同样名字的 readonly 的公共成员，可直接在构造函数中用 this 调用
- Tips:构造函数参数也可以使用 public，private,protected 修饰，也会默认新增一个公共属性，同时带有相应的特性

```typescript
class Person {
  name: 'xiaoming'
  constructor(readonly age: number = 18) {
    this.age = age
  }
}

let person = new Person(19)

console.log(person.age) //虽然没有定义属性但依旧可以调用，且值为19
```

#### 存取器

通过特殊的函数 get，set，对公共对象快速访问

```typescript
class Person {
  firstName: string = 'xx'
  lastNmae: string = 'x'

  constructor(firstName: string, lastname: string) {
    this.firstName = firstName
    this.lastName = lastname
  }

  //读取器
  get fullname() {
    console.log('执行了get')
    return this.firstName + ' ' + this.lastName
  }

  //设置器
  set fullanme() {
    console.log('执行了set')
  }
}

const person = new Person('dejiang', 'wang')

console.log(person.fullname) //直接执行fullname
```

#### 静态成员

类中的属性通过 static 修饰，那么相关的变量或者方法就变成了静态成员。

他们不能从实例中访问，同时也不能从内部函数中访问，但是可以直接调用类来访问

```typescript
class Zoo {
  static theName: string = 'luluZoo'
  constructor() {
    console.log('xx')
  }
}

console.log(Zoo.theName) //输出luluZoo  Tip:注意class类中都会内置一个name变量，所以 static name是不行的

let zoo = new Zoo()

zoo.theName //报错，提示找不到该成员
```

#### 抽象类

抽象类做为其它派生类的基类使用。 它们不会直接被实例化。 不同于接口，抽象类可以包含成员的实现细节。 `abstract`关键字是用于定义抽象类和在抽象类内部定义抽象方法。

```typescript
//抽象类不可以被实例化
abstract class Animal {
  abstract makeSound(): void //抽象类不可以写方法体
  move(): void {
    console.log('roaming the earch...')
  }
}

//定义派生类,派生类可以被实例化
class Dog extends Animal {
  makeSound() {
    console.log('wangwang')
  }
}
```

抽象类中的抽象方法不包含具体实现并且必须在派生类中实现。 抽象方法的语法与接口方法相似。 两者都是定义方法签名但不包含方法体。 然而，抽象方法必须包含`abstract`关键字并且可以包含访问修饰符。

## 函数

#### 函数声明

```typescript
const add = function (x: number = 1, y?: number): number {
  if (y) return x + y
  else return x
}
//add函数参数必须是数字类型，返回值必须是数字类型,x默认是1，y可选
```

#### 函数重载

根据传入不同的参数而返回不同的类型

```typescript
function add(x: string, y: string): string

function add(x: number, y: number): number

function add(x, y) {
  if (typeof x === 'string') return 'the String' + x + y //字符串拼接
  else return x + y //相加
}

add(1, 2) //可以，符合第二种重载

add('hello', 'world') //符合第一种重载

add(1, 'ss') //报错，不符合重载类型
```

## 泛型

`泛型`用来创建可重用的组件，一个组件可以支持多种类型的数据。 这样用户就可以以自己的数据类型来使用组件。

```typescript
function fun<T>(x: T, y: number): T {
  return x
} //将类型设置成类似于变量的形式，这样以后再用的时候就可以根据不同的数据类型，使用不同的参数

fun<string>('xx', 12) //可以
fun<string>(123, 12) //可以
fun<number>('ss', 12) //报错
```

更加多样的用法：

```typescript
function fun2<T, U, V>(x: T, y: U, z: V): [T, U, V] {
  return [x, y, z]
} //函数的第一个参数类型是T，第二个是U，第三个是V，返回的是一个元组类型

let arr = fun2<string, number, object>('x', 12, { theName: 'xiaom' })

console.log(arr) //[ 'x', 12, { theName: 'xiaom' } ]
```

## keyof

keyof(索引类型查询操作符)用来获取类型上所有已知，public 的建对应的联合类型

## 类型别名 type

type 作用就是给类型起一个新名字，支持基本类型、联合类型、元祖及其它任何你需要的手写类型

例子：

```
type test = number; //基本类型
let num: test = 10;
type userOjb = {name:string} // 对象
type getName = ()=>string  // 函数
type data = [number,string] // 元组
type numOrFun = Second | getName  // 联合类型
```

## 高级类型

常见的高级类型有如下：

- 交叉类型 &
- 联合类型 |
- 类型别名 type
- 类型索引 keyof
- 类型约束 extend(并不同于类的 extend)
- 映射类型 in
- 条件类型 ? : (并不同于三元表达式)

## [装饰器](https://www.tslang.cn/docs/handbook/decorators.html)

一句话概括：装饰器是用来在类的各个部分添加和设置各种东西的。

装饰器分为类装饰器，成员装饰器，方法装饰器，参数装饰器；分别放在一个类的前面，类的某个成员前面，方法的前面，方法的某个参数的前面。

### 一个栗子

我们先看一个 nest 框架的实例（nest 是一个以 express 为基础的 typescript**服务器**框架）

```typescript
@Controller('cats') //类装饰器
export class CatsController {
  @Get('/hello')
  @HttpCode(200) //方法装饰器
  recall(@Req() /*参数装饰器*/ request: Request): string {
    console.log(request) //将会输出网络请求的内容
    return 'hello nestjs'
  }
}
```

看不懂没关系，我们一步步的来解释每一句：

首先`@Controller('cats')`，它是一个类装饰器，要放在 class 的前面，他的作用是定义一个基本的控制器，即添加了一个路由。也就是说现在，这个类成为了一个控制器，**具有了一个`/cats`的路由**。

`@Get('/hello')`和`@HttpCode(200)`都是方法装饰器，它们放在类的方法前面，他们让这个类具有了更多的功能，分别是**增加了一个`/hello`的子路由**和一个**返回 200 的状态码**

`@Req()`是一个参数装饰器，他放在类中函数的参数前面，在这个实例中，他让这个参数具有了**请求的参数**的意义。

最终运行的结果是这样的：

![屏幕截图 2021-10-03 110506](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/屏幕截图 2021-10-03 110506.png)

可以看到，在加这些装饰器之前，这个类其实仅有一个方法：

```typescript
class CatsController {
  recall(request: Request): string {
    console.log(request)
    return 'hello nestjs'
  }
}
```

而这些装饰器，则**给这个类增加了很多功能**，从而达到了一个控制器（ 处理传入的请求和向客户端返回响应）的作用。这就是装饰器在实际开发中的用法，通过高度的封装，更加快速的实现功能。同时也具备了 OOP(面向对象开发)的特点。

### 基本使用

那么装饰器，是如何实现这些事情的呢？

首先，我们通过实现一个具有**提示功能**的类来了解类的用法

初始化：

```typescript
class Toast {
  type: string
  tell(text: string): void {}
}
```

#### 类装饰器

现在这个类是什么功能都没有的。我们先添加一个**类装饰器**，使这个类具有一个 tiltle

```typescript
const Description: ClassDecorator = target => {
  //注1
  target.prototype.title = '我是一个Toast' //注2
}

@Description //装饰类Toast
class Toast {
  type: string
  tell(text: string): void {}
}

let toast = new Toast()
interface NewToast extends Toast {
  title: string
} //注3

console.log((toast as NewToast).title) >> '我是一个Toast'
```

- 注 1：我们定义了一个 Description 装饰器，他的类型是`ClassDecorator`（类装饰器型）。注意，**装饰器是一类函数**，**不同的装饰器接收的参数不同**，这里的**类装饰器接收的参数 target 即为它装饰的类本身**。我们在类装饰器中，通过给类本身的 prototype 上添加属性，从而达到操作类的目的。
- 注 2：`target.prototype.title = '我是一个Toast'`操纵原型，相当于在 class 中添加了一个`title = '我是一个Toast'`的成员，对原型不太了解的童鞋可以评论区评论，我会单独出一期关于原型的文章
- 注 3：这里我们定义了一个 interface 接口，并且继承了 Toast 和增添了 title 属性。为的就是通过**断言**让 ts 知道 toast 是有 title 的。不然会报错,因为这个类本来是没有 title 成员的。（另外也可以直接使用 toast['title']，这样将不进行检查）

通过类装饰器，我们让一个类有了 title。但是现在这个 title 是固定的，如果我们需要传进一个参数来设置 title，这时就可以利用装饰器工厂来实现这件事情。

#### 装饰器工厂

装饰器工厂说起来好像比较高大上，我个人理解就是在各种的**装饰器外套上一个函数**，以达到接收参数的作用 🤣。

例如我们将上面的类装饰器改成一个装饰器工厂：

```typescript
const Description = (title: string): ClassDecorator => {
  //注1
  return target => {
    target.prototype.title = title
  }
}

@Description('装饰器鸭装饰器📢') //注2
class Toast {
  type: string
  tell(text: string): void {}
}

let toast = new Toast()
interface NewToast extends Toast {
  title: string
}

console.log((toast as NewToast).title) >> '装饰器鸭装饰器📢'
```

- 注 1：装饰器工厂将类装饰器套在了一个函数中，并返回了它。所以这里函数的返回是一个类装饰器型。它像是一个普通函数一样使用，只不过返回了一个类装饰器。并没有那么神秘
- 注 2：由于装饰器工厂是一个函数调用后返回装饰器，所以这里我们在使用时就直接调用，并且写入参数。

通过类装饰器，我们完成了**自定义类的 title 的功能**

#### 成员装饰器

接下来，我们添加一个成员装饰器，来装饰类的 type，表示这个提示功能是个警告(warning)。

```typescript
const initType: PropertyDecorator = (target, propertyKey) => {
  //注1
  target[propertyKey] = 'warning' //注2
}

@Description('装饰器鸭装饰器📢')
class Toast {
  @initType //注3
  type: string
  tell(text: string): void {}
}

let toast = new Toast()
console.log(toast.type) >> 'warning'
```

- 注 1：成员装饰器同样是函数，它接收的参数分别为当前类(target)和它装饰的成员的名字(propertyKey)
- 注 2：这里的写法就相当于`toast.type = warning`
- 注 3：成员装饰器装饰谁哪个成员把谁放到哪个成员上面

这里自定义 type 也可以使用装饰器工厂，只不过返回的类型成了方法装饰器。写法大同小异，有兴趣的童鞋可以试一下。

#### 方法装饰器

最后我们加上一个方法装饰器来装饰方法，让他打印出**提示信息**：

```typescript
const initTell: MethodDecorator = (target, propertyKey, descriptor) => {
  //注1
  ;(descriptor.value as unknown) = (text: string): void => {
    //注2
    console.log('warning！这里出了写问题：', text)
  }
  descriptor.writable = false
  // 这种写法ES5之后是没作用的
  // target[propertyKey] = (text: string):void => {
  //     console.log('warning！这里出了写问题：',text)
  // }
}
@Description('装饰器鸭装饰器📢')
class Toast {
  @initType
  type: string
  @initTell
  tell(text: string): void {}
}

let toast = new Toast()
toast.tell('按钮') >> 'warning！这里出了写问题： 按钮'
```

- 注 1：方法装饰器的参数分别是：接收类原型对象，对于静态方法来说是类的构造函数（target）；方法名；方法的属性描述符 ，这里的属性描述符我们经常用到 `descriptor.value`和`descriptor.writable`

- 注 2：descriptor.value 指向函数，我们可以利用它来重写函数
- 注 3：descriptor.writable = false 时，实例就没办法用`toast.tell = ...`来改写函数了

#### 参数装饰器

参数装饰器的样例如下：

```
//参数装饰器
const initText:ParameterDecorator = (target, key, index) => {

}
```

- 注：掺入的参数分别是原型(target)，方法名(key)，和参数在参数集合中的位置(index,0 开始)

它常常和其他的装饰器一同使用。

#### 不看也无所谓的 Tips:

类中不同声明上的装饰器将按以下规定的顺序应用：

1. 参数装饰器，然后依次是方法装饰器，属性装饰器应用到每个实例成员。

2. 参数装饰器，然后依次是方法装饰器，属性装饰器应用到每个静态成员。

3. 参数装饰器应用到构造函数。

4. 类装饰器应用到类。

#### 可以看看的 Tips：

相同级别装饰器是**从上往下加载**，但是是**从下往上调用**。即若有几个功能重复的同级别装饰器，**最上面的装饰器功能会覆盖掉下面的装饰器**



## 模块

TypeScript任何包含顶级`import`或者`export`的文件都被当成一个模块。相反地，如果一个文件不带有顶级的`import`或者`export`声明，那么它的内容被视为**全局可见**的（因此对模块也是可见的）。

举个例子，我们同时具有`a.ts`，`b.ts`

```typescript
//a.ts
let obj = {}
```

```typescript
//b.ts
let obj = {}
```

那么此时，编译器就会报错，因为我们在全局上具有两个同名的变量obj

我们可以利用模块的特性，更改一下`a.ts`：

```typescript
//a.ts
export let obj = {}
```

此时全局上就只有一个obj了。

我们如果想使用`a.ts`的obj对象，则可以通过export来引用对象

```typescript
//b.ts
import {obj as obj2} from './a' // 重新命名使得不会和当前变量冲突
let obj = {}
```

注意当前的`b.ts`由于在顶层也具有了import，所以此时该文件也成为了一个模块，其变量在全局都不可见。



## 命名空间

命名空间现在更推荐使用`namespace`关键字（替换掉ts1.5之前的module官架子）。

拿上面的问题来解释命名空间，同样有两个文件：

```typescript
//a.ts
let obj = {}
```

```typescript
//b.ts
let obj = {}
```

那么此时，编译器就会报错，因为我们在全局上具有两个同名的变量obj

使用命名空间，我们可以这样做：

```typescript
//a.ts
namespace A {
  export let obj = {}  
}
```

那么此时我们可以在`b.ts`文件中这样使用：

```typescript
let obj = {}
A.obj
```

此时就不会出现命名冲突的情况了。

同时命名空间支持代码分分离到多个文件，及同一个命名空间可以写在不同的文件中。但是我们必须保证所有代码都被加载了。一般有两种方式：

第一种方式，把所有的输入文件编译为一个输出文件，需要使用`--outFile`标记：

```Shell
tsc --outFile sample.js Test.ts
```

编译器会根据源码里的引用标签自动地对输出进行排序。你也可以单独地指定每个文件。

```Shell
tsc --outFile sample.js Validation.ts LettersOnlyValidator.ts ZipCodeValidator.ts Test.ts
```

第二种方式，我们可以编译每一个文件（默认方式），那么每个源文件都会对应生成一个JavaScript文件。 然后，在页面上通过 `<script>`标签把所有生成的JavaScript文件按正确的顺序引进来，比如：

`MyTestPage.html (excerpt)`

```html
    <script src="Validation.js" type="text/javascript" />
    <script src="LettersOnlyValidator.js" type="text/javascript" />
    <script src="ZipCodeValidator.js" type="text/javascript" />
    <script src="Test.js" type="text/javascript" />
```

由于命名空间很难去识别组件之间的依赖关系，对于新项目来说推荐使用模块做为组织代码的方式。





## 非空断言

typescript可以使用！进行非空断言。

例如，我们可以这么写：

```ts
let a !: string
```

这表明a是一个string类型的，而且一定不是null或者undefined

使用这样的非空断言时一定要注意赋值，否则可能会在运行时报错。

同时，对于一个不确定的变量，我们也可以使用非空断言告诉ide该变量一定有值：

```ts
nus!.trim()  //避免提示undefined无trim方法
```

