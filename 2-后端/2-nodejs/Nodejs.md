 

## process

每个Node进程都有一个独立的`process`对象，它是当前Node进程在代码中的抽象，储存了进程运行时的一些信息。

### process对象上定义的属性和方法（常用）

| 属性名称 | 用途                           |
| -------- | ------------------------------ |
| platform | 判断当前系统平台               |
| argv     | 当前进程的命令行参数数组       |
| execPath | 当前进程的可执行文件的绝对路径 |
| stdout   | 指向标准输出                   |
| stdin    | 指向标准输入                   |
| stderr   | 指向标准错误                   |
| stderr   | 指向标准错误                   |

### 预定义事件

1. beforeExit

   该事件会在exit事件出发前，事件循环队列清空之后触发。

	```js
	process.on('beforeExit', (code) => {
		...
	})
	```

	如果代码手动调用了process.exit或者是触发了uncaughtException时，该事件不会被	触发，但是如果在deforeExit定义了新的任务，如读取一个文件，那么Node进程会重新开始	   事件循环。在这种情况下，Node进程可能永远不会退出。

	```js
	process.on('beforeExit', (code) => {
	setTimeout(() => {
		console.log('xxx')
		},1000)
	})//会不断打印xxx，setTimeout里调用process.exit(),进程才可以顺利退出
	```

2. exit

   进程退出的时候触发的事件(当uncaughtException事件被出发时除外)，用作在进程结束时做一些收尾工作，与beforeExit事件不同，当exit事件被触发后进程一定会退出，因此，在回调中只能定义同步任务，异步任务会被忽略（所以setTimeout在回调中并不会被触发）

3. uncaughtException

   当代码运行出错，而又没有相对应的错误处理时，uncaughtException事件就会被触发。由于Node运行在单进程和单线程环境下，运行时错误会使进程退出。但如果在代码中监听uncaughtException事件，并在回调函数中增加逻辑，则可以维持进程继续运行。

   通常情况下，uncaughtException事件合理的利用方式是在回调函数中做一些错误处理的记录工作，然后让进程退出

## Event

事件/消息机制是由对象A发送消息，对象B注册一个消息侦听方法，当收到消息时再执行相相应的操作。从这个角度看，事件机制的目的时将对象之间的通信解耦。

Node原生的Events模块提供了事件监听和触发机制，Node中的很多原生模块都继承了该模块，从而获得处理事件的能力。

### 使用

Event模块的使用分为如下两步：
(1) 使用on方法注册一个事件和对应的回调 (2)使用emit方法触发事件

```js
const eventEmitter = require('events')

const myEvent = new eventEmitter()

myEvent.on('topic', function(opt) {
	console.log(opt)
})

myEvent.emit('topic', 'hello') //hello
```

事件监听的实现原理在于，Node会在内存中维护一个类似字典的结构。当代码中使用on方法监听以一个事件的时候，就把对应的事件名和回调方法加入字典。当程序调用emit方法时，就取出相应的回调方法调用，这个过程是完全同步的。

### 继承Event模块

Node中凡是提供事件处理功能的原生模块或者对象，都是通过继承Event模块实现的。如果想给自定义的对象增加事件处理能力，也可以通过同样的方式来实现。

```js
class Player extends eventEmitter {
}
const player = new Player()

player.on('pause', function() {
	console.log('暂停')
}) 
player.emit('pause') //暂停
```

在es6之前，我们可以这样写：

```js
const util = require('util')
const eventEmitter = require('events')

function Player() {
	eventEmitter.call(this)
}
util.inherits(Player, eventEmitter)

const player = new Player()

player.on('pause', function() {
	console.log('暂停')
}) 

player.emit('pause')
```



## 文件系统

Node在I/O方面对JavaScript的扩展，主要在于两个原生模块FileSystem和Stream上。

### FileSystem

在FileSystem模块中大部分API都有三个版本，他们的功能是一样的

- 基于回调函数的异步API，如`fs.readFile(path[,options],callback)`
- 函数名为Sync结尾的同步API，如`fs.readFlieSync(path[,options])`
- Promise版本的API,如`fsPromise.readFile(path[,options])`

相关的文件系统API可以参考 [fs 文件系统 | Node.js API 文档 (nodejs.cn)](http://nodejs.cn/api/fs.html) 

### 关于文件路径

在使用文件系统API的时候，我们访问的路径并不是绝对路径，而是相对基点（在Node被调用的时的路径）的路径

解决路径不明确的问题，我么可以使用`__dirname`，并且搭配path.resolve方法解决路径问题

```js
const fs = require('fs')
const path = require('path')
fs.writeFileSync(path.resolve(__dirname, './data.txt'))
```





## Stream

前面内容的文件系统API的回调函数通常都是如下形式：

```js
(err, data) => {}
```

这种情况下，整个文件的内容都被一次性读入内存，这也表示对文件内容的操作要等到整个文件都读取完毕后才能开始。如果使用流，就可以每次先处理一部分的数据，直到所有的数据被处理完毕为止。

### 流操作

流和I/O是紧密相关的，一个流有如下基本操作。

- 打开 
- 关闭
- 定向

流的定向是数据被督导缓冲区后使用重定向符输出到文件

### 使用可读流读取文件

首先使用`fs.writeFileSync`写一个文件

```js
const fs = require('fs')
let mbData = Buffer.alloc(20*1024*1024)
fs.writeFileSync('mb.bat', mbData)
```

之后，我们就拥有了一个20mb的文件

然后我们使用`fs.createReadStream`创建一个可读流来读取文件

```js
const fs = require('fs')
const readable = fs.createReadStream('./mb.bat', {
    highWaterMark: 1024 * 1024 //规定一次最多读1mb数据
})

readable.on('readable', () => {
    console.log('begin to read')
    readable.read()
})

readable.on('data', (data) => {
    console.log('get data')
})

readable.on('end', (data) => {
    console.log('end')
})

readable.on('error', (err) => {
    console.error(err)
})

//循环（20次）打印 begin to read get data 最终打印一次 end
```

其中的

```js
readable.on('readable', () => {
    console.log('begin to read')
    readable.read()
})
```

整体去掉，可读流会自动去读取文件

### 文件复制

(1) 使用可读流从原文件中读取数据(read方法)，(2) 使用可写流将数据写入目标位置的文件(write方法)

细节处理：例如我们读取a.txt的数据复制到b.txt的数据中，由于通常读数据是比写数据快的，此时可能会造成write的处理能力不够迅速而缓冲区积压超出其大小，此时再调用write方法会返回false。因此代码需要对write方法的返回值进行判断和处理，即当write方法返回false的时候，停止可读流的读取。当可写流将缓冲区的数据处理完，就会触发drain事件，此时可读流就可以继续读取数据。（drain事件指写入流清空了缓冲了）

```js
const fs = require('fs')
let readable = fs.createReadStream('./a.dat')
let writeable = fs.createWriteStream('./b.dat')
readable.on('data', (data) => {
	if(!writeable.write(data)) {
		readable.pause()
	}
})
writeable.on('drain', () => {
	readable.resume()
})
```

#### pipe方法

文件复制的例子中，除了同时监控两个流的状态，Stream模块提供了pipe方法用来简化这一流程，该方法可以想象成将两个管道连接在一起，开发者不必要考虑数据如何流动

```js
const fs = require('fs')
let readable = fs.createReadStream('./a.dat')
let writeable = fs.createWriteStream('./b.dat')
readable.pipe(writeable)
```

当有多个流需要处理时，也可以使用nodejs提供的pipeline方法

#### Stream和文件系统API作比较

Stream处理文件更快，并且使用到内存更少





## Child Process

child_process模块，用来提供多进程并行的支持。

### spawn( )

使用spawn执行外部命令：`child_process.spawn(command[, args][, options])`

command:需要执行的外部命令

args:可选，表示外部命令运行的参数列表

options：可选，spawn其他配置选项

spawn()会使用指定的命令生成一个新进程，执行完对应的命令后该进程会自动退出。spawn方法返回一个child_process对象，开发者可以通过监听对应的事件来获得命令执行结果

```js
const spawn = require('child_process').spawn

const command = spawn('node', ['./child.js']) //使用node命令执行js文件

command.stdout.on('data', (data) => {
    console.log("stdout:", data.toString())
})
command.on('close', () => {
    console.log('close')
})


//child.js
console.log('>>>>')
```

执行后会输出：

```
stdout: >>>>

close
```



### spawn原理

spawn方法的原理是在系统环境变量的路径下查找对应的可执行文件，然后执行该可执行文件，相当于在控制台中输入命令。但由于操作系统的差异，在使用中可能会造成预期之外的结果。

如以dir命令，linux可以直接在command参数下，而在windows中，则需要cmd.exe或者powershell.exe来执行：

```js
const spawn = require('child_process').spawn
//linux
const ls = spawn('dir')
//windows
const ls = spwan('powershell', ['dir'])

ls.stdout.on('data', (data) => {
	console.log('stdout', data)
})
```



### fork()

在**Linux**系统下，使用fork方法创建一个新（Node）进程，本质是复制一个当前的进程。当用户调用fork方法后，操作系统会为新进程分配空间，然后将父进程的数据复制一份过去，父进程和子进程只有少数数值不同，如进程标识符（PID）、

`child_process.fork(modulePath[, args][, optons])`,如果只需要以当前的源文件创建新进程，则参数是__filename作为参数调用即可

Tips：1. 当主进程退出的时候，子进程也会随之退出。 2. 要防止“fork bomb”，即不断创造子进程，通常做法是判断出是否是最初启动的进程(主进程)来决定的那个是否需要fork子进程

对于计算型任务，进程/线程的数量并不是越多越好，如6核12线程，创建12个线程就可以达到充分利用多核的目的



## 处理CPU密集型任务

Node由于是单线程环境，会出现单线程阻塞，所以被认为不适合处理I/O密集型任务，而不适合CPU计算任务。

要解决阻塞问题，最直接的办法是创建一个子进程，并且把任务交给子进程来完成，但是对于创建进程和进程之间切换的开销，使用线程更加轻

Node在10.5.0版本中增加了Worker Threads模块，该模块允许开发者为计算任务创建新的worker线程来避免事件循环被阻塞，类似与HTML5中的Web worker [HTML5 Web Workers | 菜鸟教程 (runoob.com)](https://www.runoob.com/html/html5-webworkers.html) ，每个worker线程都有自己的事件循环。

例如新开一个线程来执行计算斐波那契：

```js
//main.js
const { Worker } = require('worker_threads')

let count = 0
setInterval(() => {
    count++
    console.log(`${count}s passed`)
    if(count === 3) {
        const worker = new Worker('./thread.js', {
            workerData: 44
        })
        worker.on('message', (data) => {
            console.log(data)
        })
    }
}, 1000)


//thread.js
const { parentPort, workerData }  = require('worker_threads')


function fib(n) {
    if(n <= 0) return 0
    if(n == 2 || n == 1) return 1
    return fib(n - 1) + fib(n - 2)
}

const data = fib(workerData)
parentPort.postMessage(data)
```

主要涉及 主线程判断，新建线程，线程间通信





## 异步

### 多线程和回调函数

常见的编程语言，如Java，C#等提供了多线程编程模式，面对一个I/O任务，由开发者自行创建一个新的线程。由于数据还没有就绪，因此该线程在原地等待，CPU继续执行主线程的任务，等待I/O任务就绪之后，线程被唤醒执行完之后加ing结果告诉主线程。而Node采用单线程事件循环模型，通过回调函数来使用I/O返回的数据。此时回调函数作为Node处理异步的方式，异步调用完成时，回调函数被调用。

### Promise

为了更好的解决回调函数的嵌套和返回值问题，社区提出了Promise规范，什么是Promise： [Promise - JavaScript | MDN (mozilla.org)](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Promise) 。

### until.promisify()

Promisify方法可以将一个异步调用封装成Promise对象

```js
//转换setTmeout
const setTimeout_promise = require('util').promisify(setTimeout)
//转换readFile
const readFile_promise = require('util').promisify(require('fs').readFile)
```

跟多情况下，也可以用Promise将有回调的函数手动封装成一个Promise类型函数

### 运行多个Promise

Promise提供了一些API用于同时运行多个Promise对象，首先是Promise.all()和Promise.race()两个静态方法。这两个方法都接受一个Promise对象数组作为参数，并返回一个新的Promise对象，新的Promise对象的状态由传入的Promise对象的数组决定。

1. `all()`

   假设；有一个数组[a, b, c]，其中每个元素都是一个包裹了异步操作的Promise对象。

   ```js
   const p = Promise.all([a, b, c])
   p.then( (result) => {
   	//result是个数组，包含了是所有异步操作最终的结果
   })
   .catch( (err) => {...} )
   ```

   其中如果全部resolve才会then，否则catch

   

2. `race()`

   race的调用格式和all方法相同，区别在于race方法返回的是一个Promise对象，它的状态和最终结果(res和err)由参数数组中状态最先改变的那个Promise决定，可以助记成比赛race，谁先到终点了，是什么状态，整体就是什么状态。

   

3. `allSettled()`（Node12.9.0后支持）

   参数同all(),但是即使某个Promise对象状态变成了rejected，也会将这个rejected作为结果集的一部分在then中返回

### async/await

解决了Promise.then的繁琐： [async函数 - JavaScript | MDN (mozilla.org)](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Statements/async_function)  [await - JavaScript | MDN (mozilla.org)](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Operators/await) 



## Web应用

Node有关Web服务的模块

- HTTP, HTTP/2, HTTPS. Net

```js
//最基本的使用
const http = require('http')

const server = http.createServer((request, response) => {
    response.writeHead(200, {'Content-Type': 'text/plain'})
    response.end('hello web')
})

server.listen(8080, () => {
    console.log('Listening on 8080')
})
```

首先调用了一个createServer方法新建了一个Web服务器，该方法返回一个server对象，然后调用其listening方法监听8080端口，从而启动Web服务器

其中涉及的server，request和response，他们分别是http.Server, http.InCommingMessage及http.ServerResponse类的实例： [http 超文本传输协议 | Node.js API 文档 (nodejs.cn)](http://nodejs.cn/api/http.html#class-httpserver)  



### 路由和request.url

| 在浏览器中访问的URL            | request.url      |
| ------------------------------ | ---------------- |
| http://localhost:8080          | /   称为跟路由   |
| localhost:8080/login           | /login           |
| localhost:8080/login?name=lear | /login?name=lear |

request.url对应的字符串称为路由。



### 处理get

手写解析路由方法可能有遗漏，node提供了原生的URL模块解决这类问题，其中url.parse方法可以处理路由信息

```js
const url = require('url')
const query = url.parse(request.url, true)
console.log(query) //输出一个Url对象，包括protocol，search，query，path等属性
```



### 处理POST

HTML中POST方法的四种编码方式

- application/x-www-form-urlencoded：默认方式
- multipart/form-data：上传文件的编码方式
- text/plain：纯文本
- application/JSON：使用Ajax方式提交表单的编码方式

Node实现的服务器要处理POST请求，请求头部分可以直接通过request.headers获取，但body数据流的处理需要开发者自行实现，否则会被Node程序丢弃。实际项目中也可以通过第三方模块如formidable处理表单



### 模板引擎与页面渲染

前端页面有两种渲染方式：

- 服务器渲染，服务器返回完整的HTML字符串，前端只负责展示
- 客户端渲染，借助前端框架，服务器只返回JSON字符串，HTML由前端动态生成。

#### 模板引擎

模板引擎是一个字符串处理程序，它可以接收数据来生成特殊的字符串。是一种服务器渲染方式。

JSP就是一种经典的JAVA WEB开发常用的模板引擎。

目前以Spring为代表的Java Web开发中已经很少使用JSP，如Spring Boot默认的模板引擎是Thymeleaf。尽管编写方式不同，其核心思想不变。

```html
<!-- Thymeleaf 文件实例 -->
<!-- th:text表示该标签的内容由Thymeleaf生成-->
<html>
   	<head>
        <meta charset="UTF-8" />
        <title>Thymeleaf3 + Servlet3 实例</title>
    </head>
    <body>
        <h1>
            Thymeleaf3 + Servlet3 实例
        </h1>
        <p>
            Hello <span th:text="${recipient}"></span> !
        </p>
    </body>
</html>
```

#### 在node中使用模板引擎

Node中有很多流行的模板引擎，如EJS,Jade,Mustache等。EJS语法可以参考官网 [EJS -- 嵌入式 JavaScript 模板引擎 | EJS 中文文档 (bootcss.com)](https://ejs.bootcss.com/) 



#### 在node中使用数据库

由于node没有类似于JDBC的统一数据库编程接口，所以一般都是通过第三方包来连接数据库，常见的由mysql和mongoose



#### 使用Express

这部分内容统一归类在，前端(多端)，应用层md文件中



## node的高并发和高并行的区别

为了处理大量的请求，node/浏览器逐渐实现了高并发，即具有了处理大量请求的能力而不发生崩溃的能力。区分于高并行将多个线程运行在多个CPU核心上，node/浏览器采用了任务队列的方式，多个请求同样需要在队列中排队，本质还是单线程。但总比服务器进程崩溃好。

为了解决单线程的弱点，浏览器在HTML5实现了`web worker`来创建多线程，而node也实现了worker_threads来实现多线程。

同时node还可以借助集群来实现多进程 [cluster 集群 | Node.js API 文档 (nodejs.cn)](http://nodejs.cn/api/cluster.html) 



## Node 的生产环境配置

```js
//package.json文件:
  "scripts": {
    "env_de": "SET NODE_ENV=production",//切换为生产环境
    "env_dev": "SET NODE_ENV=developement"//切换为开发环境
  }
```



## 如何发布 npm 包

1. 初始化文件（npm init -y）；
2. 修改`package.json`, 表明引用文件位置（main 字段），执行文件字段（bin 字段），如果有 d.ts 声明文件也表明（ types 字段）
3. npm login 后 npm publish 发包



## node 中的全局 this 指向的什么

全局中的 this 默认是一个空对象。并且在全局中 this 与 global 对象没有任何的关系。它指向`module.exports`

在普通函数中 this 指向的是 global 对象，因为 js 运行时全局的 this 对象是 global，而普通函数的 this 又是动态绑定的，所以会造成这样的结果。而如果函数是箭头函数的时候，由于箭头函数的 this 是声明时定义的，所以还是指向`module.exports`

```js
const fn = () => {
  this.a = 'a'
}
const fn2 = function () {
  this.b = 'b'
}
fn()
fn2()
this.c = 'c'

console.log(global.b) //b
console.log(module.exports) //{a:'a', c:'c'}
```

## npm和pnpm，yarn的区别

### npm

> [https://www.npmjs.com/](https://links.jianshu.com/go?to=https%3A%2F%2Fwww.npmjs.com%2F)

npm 是 Node Package Manager 的缩写，是一个 NodeJS 包管理和分发工具，我们可以使用它发布、安装和卸载 NodeJS 包。npm 是 JavaScript 运行时环境 Node.js 的默认包管理器。

### yarn

> [https://yarnpkg.com/](https://links.jianshu.com/go?to=https%3A%2F%2Fyarnpkg.com%2F)

yarn 是 facebook 等公司在 npm v3 时推出的一个新的开源的 Node Package Manager，它的出现是为了弥补 npm 当时安装速度慢、依赖包版本不一致等问题。

yarn 有以下优点：

- 安装速度快

  - 并行安装：npm 是按照队列依次安装每个 package，当前一个 package 安装完成之后，才能继续后面的安装。而 Yarn 是同步执行所有任务。
  - 缓存：如果一个 package 之前已经安装过，yarn 会直接从缓存中获取，而不是重新下载。

- 版本统一

  yarn 创新性的新增了 yarn.lock 文件，它是 yarn 在安装依赖包时，自动生成的一个文件，作用是记录 yarn 安装的每个 package 的版本，保证之后 install 时的版本一致。不过随着后来 npm 也新增了作用相同的 package-lock.json，这个优势已经不太明显。

### pnpm

> [https://pnpm.io/](https://links.jianshu.com/go?to=https%3A%2F%2Fpnpm.io%2F)

2017 年 pnpm 推出。全称 Performance NPM，即高性能的 npm。相比较于 yarn，pnpm 在性能上又有了极大的提升。

pnpm 的出现解决了 npm、yarn 重复文件过多、复用率低等问题。我们知道，不管是 npm 还是 yarn，它们的安装方法都是将项目依赖包的原封不动的从服务器上下载到本地，写入到 node_modules 文件夹，而每个 package 又都有自己的 node_modules，所以当一个 package 在不同的依赖项中需要时，它会被多次复制粘贴并生成多份文件，形成一个很深的依赖树。

另外，如果同一个 package 在我们本地的多个项目中使用，每次安装的时候它都会被重新下载一次。比如我们本地有 100 个项目，都依赖 lodash，那么使用 npm 或 yarn 进行安装， lodash 很可能就被下载、安装了 100 次，也就是说我们的磁盘中有 100 个地方写入了 lodash 的代码，这种方式是极其低效的。

pnpm 内部使用基于内容寻址的文件系统来存储磁盘上所有的文件，这个文件系统出色的地方在于:

同一个包 pnpm 只会安装一次，磁盘中只有一个地方写入，后面再次使用都会直接使 hardlink。即使一个包的不同版本，pnpm 也会极大程度地复用之前版本的代码。举个例子，比如 lodash 有 100 个文件，更新版本之后多了一个文件，那么磁盘当中并不会重新写入 101 个文件，而是保留原来的 100 个文件的 hardlink，仅仅写入那一个新增的文件。

链接：https://www.jianshu.com/p/e02ffa9effe6

## monorepo

把公用的文件，模块提取成公共模块，重复使用。pnpm的就是这个思想，从而大大增加了包的安装速度，同时节约了磁盘体积。
