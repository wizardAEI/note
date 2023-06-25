## webpack：前端打包工具，万物皆模块



### 为什么使用webpack，他解决了什么问题？

1. 解决不同浏览器对js版本的兼容问题
2. 解决模块化所造成的的文件数量过多，影响请求效率的问题
3. 除了js文件，css文件，html文件或者其他形式的文件未来可能都会面临着模块化的问题

webpack的作用是从入口文件进入，构建一个依赖图，然后将这些模块组合成一个或多个包(bundle)，变成静态资源以供浏览器展示。这里面涉及到了对不同文件的合并打包，对es6的语法兼容(变成es5)，对一些小文件的静态优化(如base64优化图片)，对scss，ts等语言的解析等等。



### 前置概念

1. 树结构：在一个入口文件中引入所有资源，形成所有依赖关系的树状图
2. chunk:打包过程中被操作的模块文件叫作chunk，例如异步加载一个模块就是一个chunk
3. bundle：bundle是最后打包成的文件，可以就是chunk，但大部分情况下是多个chunk的集合



```js
//安装
npm install webpack webpack-cli --save-dev

webpack
```



### webpack.config.js  :  webpack及相关配置文件



```javascript
const path = require('path')
const HtmlWebpackPlugin = require('html-webpack-plugin')
module.exports = {
    mode: 'development', // 设置mode
    entry:path.join(__dirname,'src','index.js'),//导入的入口文件
    output:{
    path:path.join(__dirname,'dist'),//出口文件目录
    filename:'bundle.js'//出口文件的名称
    },
    devServer:{
        port:3333,//webpack-dev-server的配置，这里是端口，注意在用的时候要把webpack-cli的版本降到3.1
        publicPath:'/dist'//服务器启动时要去寻找的出口文件的目录。默认也是/dist
    },
     module: {
        rules: [
          {
            test: /\.js$/i,
            exclude: /node_modules/,//不要去检索这个文件
            use: {
                loader: 'babel-loader',
                options: {         // options选项
                    presets: ['@babel/preset-env'],  // presets设置的就是当前js的版本
                    //plugins: [require('@babel/plugin-transform-object-rest-spread')] // plugin是需要的插件       
                }
            }
            ,
          },
        ],
    }, 
    plugins: [new HtmlWebpackPlugin({
        template:path.join(__dirname,'src/index.html'),  //涉及到的目录
        filename:'index.html' //打包后的名字
    })],
} 
```





### webpack-dev-server:  一个基于express的小型的服务器

```js
webpack-dev-server

安装 
npm install webpack-dev-server  --save-dev

降低webpack-cli版本
npm install webpack-cli@3.x   --save-dev
```





### 文件加载器 loader：使webpack可以实现打包更多类型的文件，例如CSS，PNG



#### css-loader，style-loader

```js
//安装
npm install style-loader css-loader --save-dev

//使用
//js文件中引用css
import('style.css')

//配置好webpcak.config.js后webpack
```



压缩器 webpack-plugin

```js
//安装
npm install uglifyjs-webpack-plugin  --save -dev


//https://blog.csdn.net/weixin_44090040/article/details/107566015  =>使用过程
```



#### babel loader

```js
//安装
npm install babel-loader --save-dev
```





### babel   ---ES6->ES5  让预览器/webpack识别语法



```js
//安装
npm install --save-dev  @babel/core @babel/cli @babel/preset-env   //局部安装
npm install --save-dev @babel/plugin-transform-arrow-functions  //插件

//配置babel-loader
npm install --save-dev  babel-loader

//babel.config.json配置文件
{
  "presets": [
    [
      "@babel/env",
      {
        "targets": {
          "edge": "17",
          "firefox": "60",
          "chrome": "67",
          "safari": "11.1"
        },
        "useBuiltIns": "usage",
        "corejs": "3.6.5"
      }
    ]
  ]
}


//使用
babel src --out-dir lib --presets=@babel/env  //src 是执行目录   lib 是导出目录
```





### html-webpack-plugin  

```js
npm install --save-dev html-webpack-plugin


//config.js
const HtmlWebpackPlugin = require('html-webpack-plugin');
const path = require('path');

module.exports = {
  entry: 'index.js',
  output: {
    path: path.resolve(__dirname, './dist'),
    filename: 'index_bundle.js',
  },
  plugins: [new HtmlWebpackPlugin({
      template:path.join(__dirname,'src/index.html'),  //涉及到的目录
      filename:'index.heml' //打包后的名字
  })],
};
```







### 依赖：package.json：

```json
{
  "name": "responsiveBootStrap",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "devDependencies": {
    "@babel/cli": "^7.14.5",
    "@babel/core": "^7.14.6",
    "@babel/plugin-transform-arrow-functions": "^7.14.5",
    "@babel/preset-env": "^7.14.7",
    "babel-loader": "^8.2.2",
    "css-loader": "^5.2.6",
    "html-webpack-plugin": "^5.3.2",
    "style-loader": "^3.0.0",
    "webpack": "^5.41.1",
    "webpack-dev-server": "^3.11.2",
    "webpack-cli": "^3.3.12"
  },
  "devpendencies": {
  }
}
```



### 配置：webpack.config.js

```js
const path = require('path')
const HtmlWebpackPlugin = require('html-webpack-plugin')
module.exports = {
    mode: 'development', // 设置mode
    entry:{
       index: path.join(__dirname,'src/index.js')
    },//入口文件,若要打包多个文件就配置多个
    output:{
    path:path.join(__dirname,'dist'),//出口文件目录
    filename: '[name].js'
    },
    devServer:{
        port:3333,//webpack-dev-server的配置，这里是端口，注意在用的时候要把webpack-cli的版本降到3.1
        contentBase: path.join(__dirname, 'dist'),//服务器启动时要去寻找的出口文件的目录。默认也是/dist
        compress: true,
    },
     module: {
        rules: [
          {
            test: /\.js$/i,
            exclude: /node_modules/,//不去检索node_modules，节省时间
            use: {
                loader: 'babel-loader',
                options: {         // options选项
                    presets: ['@babel/preset-env'],  // presets设置的就是当前js的版本
                    plugins: [] // plugin是需要的插件       
                }
            }
            ,
          },
          {
            test: /\.css$/i,
            use: ["style-loader", "css-loader"],//倒叙放置，因为loader加载时倒叙加载的
          },
        ],
    }, 
    plugins: [
        //打包html，多个包就new多次
        new HtmlWebpackPlugin({
        template:path.join(__dirname,'src/index.html'),  //涉及到的目录
        filename:'index.html' //打包后的名字
    })],
} 
```



### babel.config.json

```json
{
    "presets":[
      [
        "@babel/env",
        {
          "targets": {
            "edge": "17",
            "firefox": "60",
            "chrome": "67",
            "safari": "11.1"
          },
          "useBuiltIns": "usage",
          "corejs": "3.6.5"
        }
      ]
    ]
  }
```

## webpack提高构建的方法

### 优化loader配置

1. 写明exclude，include，test，表明不去检索哪些文件，在什目录下检索，以及匹配规则

2. `extension`数组为缺省后缀名的快速匹配

   ```js
   resolve: {
       extensions: ['.tsx', '.ts', '.js'],
     }, //配置模块化引入文件的缺省类型，即如果没有后缀名，则从上面数组中依次查找
   ```

3. 加上alias别名，减少·`./../../`这种情况的出现

   ```js
   resolve:{
           alias:{
               "@":path.resolve(__dirname,'./src')
           }
       }
   ```

4. 使用 cache-loader，有些加载速度比较慢的loader可以尝试存在缓存里提高二次构建速度

   ```js
   module.exports = {
       module: {
           rules: [
               {
                   test: /\.js$/,
                   use: ['cache-loader', ...loaders], //注意将cache-loader放到最开始
                   include: path.resolve('src'),
               },
           ],
       },
   };
   ```

   



## webpack loader和plugin的区别

loader的作用可以看成转换器，操作的是文件。例如将less文件转换成css文件。在打包文件之前运行。

plugin的作用是监听webpack事件，并且在某个事件下对打包进行优化，资源管理，环境注册等。运行在整个webpack打包周期中。例如`HtmlWebpackPlugin`就是在js等文件打包好后将其合适的注入在指定的或生成的html文件里。



## webpack 原理

webpack从入口文件出发，寻找文件间的依赖图并构建成一个个的模块(chunk)，通过loader对不同模块进行翻译(如less->css)，语法兼容(es6->es5)，静态资源优化（如base64），最终完成对模块的“翻译”，同时将同类型的模块打包成一个或多个bundle。在这个过程中，每个生命周期都有相应的钩子函数，可以注入plugins，从而对打包的每个阶段进行操作，例如生成html文件并插入js，css链接等操作。



## webpack热更新是什么

即模块热更换。在webpack5里可以通过`webpack serve`来打开一个8080本地服务器的形式启动一个服务。当有文件更改时webpack后自动热替换相应的模块



## 如何写一个 webpack plugin

`webpack` 插件的具体实现以下组成：

- 声明一个一个 JavaScript 构造函数。
- 在插件函数的 prototype 上定义一个 `apply` 方法。
- 指定一个绑定到 webpack 自身的[事件钩子](https://www.webpackjs.com/api/compiler-hooks/)。
- 处理 webpack 内部实例的特定数据。
- 功能完成后调用 webpack 提供的回调。

```js
function MyExampleWebpackPlugin() {

};
// 在插件函数的 prototype 上定义一个 `apply` 方法。
MyExampleWebpackPlugin.prototype.apply = function(compiler /*webpack环境配置*/) {
  // 指定一个挂载到 webpack 自身的事件钩子。
  compiler.plugin('webpacksEventHook', function(compilation /*webpack内部实例的特定数据*/, callback) {
    console.log("This is an example plugin!!!");
    // 功能完成后调用 webpack 提供的回调。
    callback();
  });
};
```

## css-loader做了什么

css-loader

解析css文件，将其中的@import，url等转换成`require`来动态加载引用的css文件。（因为webpack认识require）

`style-loader`来将css存放在新建的`style`的标签中

(注意这里只是简化，正常流程时包含了webpack的pich操作的)

```javascript
module.exports = function (source) {
  return `let style = document.createElement('style')
    style.innerHTML = ${JSON.stringify(source)} // 注意格式化代码，换行符保留
    document.head.appendChild(style)`
}
```



[Webpack的loader原理和实现 - 掘金 (juejin.cn)](https://juejin.cn/post/6916919296098566157#heading-8)https://www.jianshu.com/p/d2470f719fee)



## babel干什么用的？实现思路？

babel可以称之为一个JavaScript转译器，用来将现有的JavaScript代码转换成指定的向后兼容版本的JavaScript代码。

 Babel 的三个主要处理步骤分别是： **解析（parse）**，**转换（transform）**，**生成（generate）**。

解析阶段包括词法分析（将代码段转换成扁平的语法片段数组：令牌流）和语法分析（ 把一个令牌流转换成 AST 的形式。 ） 。

转换阶段接收AST语法树并对其进行遍历，在这个过程中按照兼容版本要求对语法树进行替换更新操作。

生成阶段就是将AST抽象语法树转换成JavaScript代码并创建源码映射（source maps）





