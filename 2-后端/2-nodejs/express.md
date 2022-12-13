## Express

### 基本运行

```js
const express = require('express')
const app = express()
app.get('/', function(req, res) {
	res.end('hello express')
})
let port = 3000
app.listen(port)
```

### 与原生http模块混用

express可以和http api昏庸，app作为createSserver的参数

```
const server = http.createServer(app)
server.listen(3000) //和app.listen(3000)一样
```



### 服务器端解决跨域问题

```js
//解决所有的跨域，变为公共的服务器
const allowCors = function(req, res, next) {
    res.header('Access-Control-Allow-Origin', req.headers.origin);
    res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Content-Type');
    res.header('Access-Control-Allow-Credentials','true');
    next();
  };
app.use(allowCors);//使用跨域中间件

//指定某网址跨域
const allowCors = function(req, res, next) {
    res.header('Access-Control-Allow-Origin', "固定ip");
    res.header('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS');
    res.header('Access-Control-Allow-Headers', 'Content-Type');
    res.header('Access-Control-Allow-Credentials','true');
    next();
  };
app.use(allowCors);//使用跨域中间件
```

```js
//cors 解决跨域的包
app.use(require('cors')())//全局跨域或者某些路由允许跨域
```



### get请求解析

```js
//通过req.query来接收
app.get('/axios/get', (req, res) => {
    console.log(req.query)
    res.send(req.query.name)
})
```



### post请求解析

```js
//配置中间件
app.post('/post/axios',express.json(),(req,res)=>{
    console.log(req)
})

//如果请求说明了不是json格式是 URL-encoded 格式（application/x-www-form-urlencoded）的请求体 则需要用express.urlencoded({ extended: false })的中间件
```





### 静态资源托管/虚拟前缀

```js
//虚拟前缀,起到迷惑作用
app.use('/img',express.static(path.join(__dirname,'public')))
//这里真正的文件是放在public目录里，但是访问需要到/img中访问，这样可以迷惑对方，防止被猜到真正的目录-
```



### express的Router

```javascript
const express = require('express');
 
let app = express();
app.listen(8888);
 
//创建路由实例，我们可以在该实例上自由的添加路由
let usersRouter = express.Router();
let orderRouter = express.Router();
 
//添加两个路由到应用上
app.use('/users', usersRouter);
app.use('/order', orderRouter);
 
//注意这时候再加路由，就可以不带前面的/users路径了
usersRouter.get('/', function (req, res) {
    res.send('用户首页');
});
 
usersRouter.get('/:id', function (req, res) {
    res.send(`${req.params.id} 用户信息`);
});
 
//注意这时候再加路由，就可以不带前面的/order路径了
orderRouter.get('/', function (req, res) {
    res.send('订单首页');
});
 
orderRouter.get('/:id', function (req, res) {
    res.send(`${req.params.id} 订单信息`);
});
```



### 链式路由

一个路由可能被多个HTTP方法请求，此时可以使用链式路由

```js
app.route('/book')
	.get((req, res) => {})
	.post((req, res) => {})
```



### 设置cookie

```
res.cookie(name, value, [, options])
```

`name`类型是String

`value`类型为String或者Object，如果Object会在`cookie.serialize()`之前自动调用`JSON.stringify()`

`option`类型为对象，具体属性见官方文档

### 读取cookie

```
request.headers.cookie
```

可以使用express的cookie-parser中间件加载cookie的内容。



### 使用session	

express中可以使用`express-session`中间件来实现session机制

```js
const session = require("express-session")
let sess = {
	secret: "keyboard cat",
	resave: false,
	saveUninitialize: true,
	cookie: {
		maxAge: 5000
	}
}
app.use(session(sess))
```

当客户端的请求经过该中间件的时候会被赋予一个sessionId，并且将器设置为一个客户端cookie。（cookie的名字是connect.sid，指定sess对象的那么属性可以修改。

目前的session除了sessionId之外还没有真正储存信息，再req.session对象上添加属性可以实现自定义的session储存信息

- 定义seesion数据

  ```js
  app.get('/login', (req, res, next) => {
  	req.session.user = 'edge' //储存用户使用设备的信息
  	res.end('xxxx')
  })
  ```

- session的储存

  除了将session的数据直接储存在内存中，即req.sessionStore属性（服务器端）。为了避免session数据太多，可以采用MongoDB或者Redis来储存session，同样可以利用express-session中间件实现。

- 销毁session

  设置的session过了时间会失效，当需要服务器主动服务器主动销毁的时候，可以使用 express-session中间件提供了destroy方法，用来销毁当前请求的session，而其他的session不受影响。

  ```
  app.get('/logout', (req, res, next) => {
  	req.session.destroy(function(err) {
  		next()
  	})
  	console.log(req.sessionStore) //可以发现当前的session已经被删除
  	res.end('logout')
  })
  ```


### OAuth

OAuth是目前服务器开发领域通用的第三方认证的协议，他允许第三方应用在不获得用户密码的情况下获取一些用户在OAuth提供者上的信息。

OAuth提出了一种开放的授权机制。站在OAuth服务提供者的角度看，它可以让用户以外的第三方应用，在没有用户名和密码的情况下请求OAuth服务提供者的某些用户信息。

举例：实现针对Github的OAuth应用

1. Github上打开Setting->Developer Settings->OAuth Apps 注册OAuth应用
2. 打开详情，可以看到具体的Client ID和Client Secret

```js
const express = require('express')
const app = express()
const port = 3000
const clientID = '421ec984e51c26bfeb5a'
const clientSecrets = 'You need a client secret to authenticate as the application to the API.'
const redirect_uri = 'http://localhost:3000/OAuth/github/redirect' //当github授权成功后，github向该页面发送一个get请求(带上一个单独的授权码)来获取令牌

app.get('/', (req, res) => {
  res.send('Hello World!')
})

//通过这个请求转入GitHub的授权页面
app.get('/OAuth', (req, res) => {
    let url = 'https://github.com/login/OAuth/authorize' + '?client_id=' + clientID + 'redirect_uri=' + redirect_uri + '&response_type=code&scope=user'
    res.redirect(url)
})

app.get

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})
```



### 使用mongo

```js
module.exports = app =>{
    const mongoose = require('mongoose')
    mongoose.connect('mongodb://127.0.0.1:27017/集合名',{
        useNewUrlParser:true,
        useUnifiedTopology:true
    })
}
```



## express 5.x

### 安装

```
express@next
```





### 后端命名规则

小写+s是路由，大写单数是模型名

例：

http://localhost:3000/admin/api/categories   是路由   ，其中Category   是模型







### inflection包

用法  require('inflection').classify(resource) 将小写复数转成单数并首字母大写

用处，快速确定后端的路由的小写复数对应的模型





### multer包

向数据库上传图片的中间件





### JWT

```
const jwt = require('jsonwebtoken');
const secretKey = 'aeixhfl'
const Token = {
        encrypt: function(data, time) { //data加密数据，time过期时间
            return jwt.sign(data, secretKey, { expiresIn: time })
        },
        decrypt: function(token) {
            try {
                let data = jwt.verify(token, secretKey);
                return {
                    token: true,
                    data
                };
            } catch (e) {
                return {
                    token: false,
                    data: e
                }
            }
        }
    }
    //加密发给前端
const token = Token.encrypt({ id: 1905010504 }, 60 * 60);
console.log(token)
    //接收请求后解密
console.log(Token.decrypt(token))
```

