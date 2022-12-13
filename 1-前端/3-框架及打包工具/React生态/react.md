## 概述

React 是一个用于**构建用户界面**的**JavaScript 库**

## 特点

1. 声明式。可以在 js 中通过 jsx 直接渲染 UI，声明 HTML 即可。
2. 基于组件

## 基本使用

### 创建 react 元素

```js
/**
 *接收三个参数，分别是元素名称，元素属性，元素的子节点或元素的文本
 */
React.createElement(
  'p',
  {
    title: '标题',
    id: 'title1',
  },
  React.createElement('span', null, '我是一个span节点')
)
```

### 渲染元素

```js
/**
*接收两个参数，分别是要渲染的react元素和挂载点，挂载点一般是某个dom
*/
const el = React.createElement(...)
reactDOM.render(el, document.getElementById('root'))
```

### 安装脚手架

```
安装
npx  create-react-app react-app
```

## JSX 基本使用

```jsx
const title = <h1>Hello JSX</h1>
ReactDOM.render(title, document.getElementById('root'))
```

### jsx 注意点：

1. React 元素使用驼峰命名法
2. 特殊属性名：`class`->`className`，`for`->`htmlFor`，`tabindex`->`tabIndex`
3. 没有子元素的 React 元素可以直接使用/>结束
4. 推荐使用`()`包裹 jsx 语句，避免出现`;`陷阱

### jsx 在 javascript 中的使用

```jsx
const age = 19
const title = <h1>his age is {age}</h1>
ReactDOM.render(title, document.getElementById('root'))
```

## jsx 条件渲染

```jsx
const loading = true
const dataLoading = () => {
  if (loading === true) return <div> loading... </div>
  return <div> 数据加载完成 </div>
}
const title = dataLoading()

ReactDOM.render(title, document.getElementById('root'))
```

## jsx 列表渲染

jsx 是可以返回数组的，我们可以这样返回一个列表

```jsx
const songs = [
  { id: 'a', name: 'x' },
  { id: 'b', name: 'y' },
  { id: 'c', name: 'z' },
]
const list = (
  <ul>
    {songs.map(item => (
      <li key={item.id}>{item.name}</li>
    ))}
  </ul>
)
ReactDOM.render(list, document.getElementById('root'))
```

## jsx 样式处理

```jsx
//行内style样式
const title = (
  <h1 style={{ color: 'red', backgroundColor: 'skyblue' }}>h1样式处理</h1>
)

//class添加
import './index.css'
const title = <h1 className="title">h1样式处理</h1>
```

## jsx 语法的转换

jsx 语法会被转化为`React.createElement()`方法，可以被看做一个语法糖。

![屏幕截图 2021-11-11 231526](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/屏幕截图 2021-11-11 231526.png)

在 react 的 cli 中内置了 babel 来转化 jsx 语法成 createElement()方法。而且可以识别 js 中的 jsx 语法并转换。

## React 组件

```jsx
//函数组件
//函数名称以大写字母开头，函数组件必须有返回值，表示该组件的结构，如果返回null，表示不渲染任何内容
function Hello() {
  return <div>这是我的一个函数组件！</div>
}
ReactDOM.render(<Hello />, document.getElementById('root'))
```

```jsx
//class组件
//必须大写字母开头，要继承React.Component,必须提供render方法比且必须有返回值
class ComOne extends React.Component {
  render() {
    return <div>Hello Class Component</div>
  }
}
```

```jsx
//抽离为单独的js文件(Hello.js)
import React from 'react'
import './Hello.css'

class Hello extends React.Component {
  render() {
    return <h1>这个是一个独立组件内的h1</h1>
  }
}

export default Hello
```

## 事件绑定

```jsx
//使用class
class Hello extends React.Component {
  handleClick() {
    console.log('点击事件')
  }
  render() {
    return <h1 onClick={this.handleClick}>这个是一个独立组件内的h1</h1>
  }
}
//使用函数
export default function Hello() {
  function handleClick() {
    console.log('点击')
  }
  return <button onClick={handleClick}>一个按钮</button>
}
```

## 事件对象

```js
export default function Hello() {
  function handleClick(e) {
    e.preventDefault()
    console.log('不会跳转')
  }
  return (
    <a href="http://baidu.com" onClick={handleClick}>
      这个是链接
    </a>
  )
}
```

## 有状态组件(类组件)和无状态组件(函数组件)

函数组件没有自己的状态，只负责数据的展示；而类组件有自己的状态，负责更新 UI，让页面“动”起来

## 状态：state 和 setState

状态（state）即数据，是组件内部的私有数据，只能在组件内部使用。state 的值是对象，表示一个组件可以有多个数据

使用方法：

```jsx
class Hello extends React.Component {
  // constructor() {
  //     super()
  //     this.state ={
  //         count: 0
  //     }
  // }
  state = {
    count: 0,
  }
  handleClick = () => {
    //注意这里使用的是箭头函数，因为直使用函数的话this会出问题
    this.setState({
      count: this.state.count + 1,
    })
  }
  render() {
    return (
      <>
        <h1> 计数器：{this.state.count}</h1>
        <button onClick={this.handleClick}>+</button>
      </>
    )
  }
}
```

### setState 详解

- setState 是异步的，看下面的代码：

  ```jsx
  {
      ...
  	 this.setState({
          num: this.state.num + 1
        })
        console.log(this.state.num)
        this.setState({
          num: this.state.num + 1
        })
  	}
  //最终console打印出来的结果是 1 因为是setState异步的，所以此时还没有更新
  //更新渲染后，num的值是2 因为第二次的setState中num还是1，所以这个setState仍是让num变成了2
  ```

- 多次调用 setState 最终只会执行一次 render 函数，所以（为性能优化做考虑）

- setState 推荐语法

  ```jsx
  this.setState((state, props) => {
  	return {
  		count: state.count + 1
      }
  }})
  ```

  这种语法更推荐使用，同时在这种语法下，我们每次的回调函数的参数是最新的 state。即可以避免重复调用 setState 修改一个值只生效一次的情况

  ```jsx
  {
      ...
  	 this.setState((state, props) => {
          num: state.num + 1
        })
        this.setState((state, props) => {
          num: state.num + 1
        })
  	}
  //最后的num为 3。因为每次的state是最新的，所以第二次使用setState的时候state.num是 2 (即使现在的this.state.num还没有更新仍为 1)
  ```

- setState 第二个参数（类似于 vue 的 nextTick）

  ```jsx
  this.setState(
    (state, props) => {
      num: state.num + 1
    },
    () => {
      console.log(this.state.num)
    }
  ) //this.state.num初始为1
  //此时打印出来的是2，因为第二个参数是在状态更新后并且重新渲染了之后触发的一个回调
  ```

## 表单处理---受控组件

### input

```jsx
changeHandle = (e) => {
     this.setState({
         txt:e.target.value
     })
 }

...
<input type="text" value={this.state.txt} onChange={this.changeHandle}></input>
```

### textarea

```jsx
<textarea value={this.state.txt} onChange={this.changeHandle}></textarea>
```

### select

```jsx
handleCity = e => {
  this.setState({
    city: e.target.value,
  })
}

;<select value={this.state.city} onChange={this.handleCity}>
  <option value="sh">上海</option>
  <option value="bj">北京</option>
  <option value="cs">长沙</option>
</select>
```

### checkbox

```jsx
handleCheck = e => {
  this.setState({
    isChecked: e.target.checked,
  })
}

;<input
  type="checkbox"
  checked={this.state.isChecked}
  onChange={this.handleCheck}
/>
```

## 表单处理---非受控组件

```jsx
constructor() {
    super()
    this.txtRef = React.createRef()
}

<input type="text" ref={this.txtRef}></input>
<button onClick={() => {console.log(this.txtRef.current.value)}}> 点击 </button>
```

注意，这是直接操作 dom 的方式，不太推荐

## 组件通信

### props

特点：

1. 可以给组件传递任意类型的数据
2. props 是只读的对象，只能读取属性的值，无法修改对象
3. 注意：使用类组件的时候，如果写了构造函数，应该将 props 传递给 super(), 否则，无法在构造函数中获取到 props！

```jsx
<Hello name="jack" age=(19) />

function Hello(props) {
    return (<div>{props.name}</div>)
}
```

```jsx
class Hello eximport './App.css';
import React from 'react'

class App extends React.Component {
  constructor(props) {
    super(props) //必须要传递参数
    this.props = props
  }
  render() {
    return (
      <>
      {this.props.name}
      </>
    )
  }
}

export default App
```

### 父子组件传值

利用 props 很容易实现父组件像子组件传值。

子向父组件传值：利用回调函数，父组件提供回调，子组件调用，将要传递的数据作为回调函数的参数并执行，那么此时父组件就会执行回调函数并且得到子组件的参数

```jsx
import './App.css'
import React from 'react'

class Child extends React.Component {
  clickHandle = () => {
    //子组件调用父组件的函数
    this.props.getMsg('这是子组件的数据')
  }
  render() {
    return (
      <>
        <button onClick={this.clickHandle}>点击按钮将数据传递给父组件</button>
      </>
    )
  }
}

class Parent extends React.Component {
  getChildMsg = data => {
    console.log('接收到子组件传递的数据', data)
  }
  render() {
    return (
      <>
        子组件：
        <Child getMsg={this.getChildMsg} />
      </>
    )
  }
}

export default Parent
```

### 兄弟组件传值

- 将兄弟组件传递的值状态提升到最近的公共父组件中，由公共父组件管理这个状态

```jsx
import './App.css'
import React from 'react'

class BrotherOne extends React.Component {
  clickHandle = () => {
    //子组件调用父组件的函数
    this.props.getNum(321)
  }
  render() {
    return (
      <>
        <button onClick={this.clickHandle}>按钮</button>
      </>
    )
  }
}

class BrotherTwo extends React.Component {
  render() {
    return <>使用兄弟组件更改：{this.props.data}</>
  }
}

class Parent extends React.Component {
  state = {
    num: 123,
  }
  getChildMsg = num => {
    this.setState({ num })
  }
  render() {
    return (
      <>
        <BrotherOne getNum={this.getChildMsg} />
        <BrotherTwo data={this.state.num} />
      </>
    )
  }
}

export default Parent
```

### props children 属性

组件中内嵌子节点（文本，标签，组件，函数），props 的 children 属性会得到相应子节点

```jsx
import './App.css'
import React from 'react'
class Node extends React.Component {
  constructor(props) {
    super(props)
    console.log(props.children)
  }
  render() {
    return (
      <>
        子组件
        <br />
        从父组件传来的子节点：
        {this.props.children}
      </>
    )
  }
}

class Parent extends React.Component {
  render() {
    return (
      <Node>
        <span>一个span子节点</span>
      </Node>
    )
  }
}

export default Parent
```

### props 检验

对于组件来说，由于 props 是外来的，无法保证组件传入的数据的格式，所以需要对 props 进行校验。

校验方式：在创建组件的时候，指定 props 的类型，格式等，捕获使用组件时因为 props 导致的错误，给出明确的错误提示，增加组件的健壮性

使用方式

```bash
yarn add prop-types
```

```jsx
import './App.css'
import React from 'react'
import PropTypes from 'prop-types'

class NodeOne extends React.Component {
  constructor(props) {
    super()
  }
  render() {
    return <>{this.props.name}</>
  }
}
NodeOne.propTypes = {
  name: PropTypes.string,
}

class Parent extends React.Component {
  render() {
    return <NodeOne name={123} />
  }
}
export default Parent
```

此时打开控制台，就可以看到相关的错误提示：

```
Warning: Failed prop type: Invalid prop `name` of type `number` supplied to `NodeOne`, expected `string`.
```

更多使用方式：

```jsx
//属性a number
//属性 fn 函数且必填
//属性 tag react元素
//属性 filter 对象({area: '上海', price: 1999})
App.propTypes = {
  a: PropTypes.number,
  fn: PropTypes.func.isRequired,
  tag: PropTypes.element,
  filter: PropTypes.shape({
    area: PropTypes.string,
    price: PropTypes.number,
  }),
}
```

### props 默认值 defaultProps

如果没有传入 props 值，会有一个默认的值

```jsx
App.defaultProps = {
  name: 'abc',
}
```

## Context

通过`React.createContext()`结构出来的`Provider`和`Consumer`跨组件传递数据

使用方法：

```jsx
import './App.css'
import React from 'react'

const { Provider, Consumer } = React.createContext()

class SubNode extends React.Component {
  render() {
    return (
      <>
        我是subnode组件,上层组件传来的信息：
        <Consumer>{data => <span>{data}</span>}</Consumer>
      </>
    )
  }
}

class Node extends React.Component {
  render() {
    return (
      <>
        <SubNode />
      </>
    )
  }
}

class Parent extends React.Component {
  render() {
    return (
      <Provider value="hello imapp">
        <Node />
      </Provider>
    )
  }
}

export default Parent
```

## 生命周期

注意 react 的生命周期只有在类组件中才可以使用

组件创建过程：

**constructor()** -> getDerivedStateFromProps() -> **render()** -> **componentDidMount**

组件更新过程：

getDerivedStateFromProps() -> shouldComponentUpdate() -> **render()** -> getSnapshotBeforeUpdate() -> **componentDidUpdate()**

注意调用 componentDidUpdate()的时候如果要在其中写 setState，必须使用 if 语句判断，不然会嵌套调用 componentDidUpdate()，导致无限循环错误。正确用法：

```jsx
//判断更新前后的props是否相同来决定是否重新渲染组件
componentDidUpdate(preProps) {
    if(preProps.count !== this.props.count) {
		this.setState({
            ...
        })
    }
}
```

装卸时:

componentWillUnmount()

## 组件复用

### render-props 模式

例如：`<Mouse render = { {mouse} => {} }>`在使用组件的时候，添加一个值作为函数的 prop，通过函数**参数**来获取；同时通过该函数的返回值来作为要渲染的 UI 内容。（需要组件内部实现）。实则是子父传值的一种用法。

例如（实现一个通用的获取鼠标位置的组件）：

```jsx
import './App.css'
import React, { Component } from 'react'

class Mouse extends Component {
  // 鼠标位置state
  state = {
    x: 0,
    y: 0,
  }
  //一个通用组件，用来获取鼠标坐标并返回，最终通过调用props.render函数，让使用该组件的组件产生回调，从而在参数中实现组件信息的传递。并且利用函数回调及进行复用组件的自定义渲染
  handleMouseMove = e => {
    this.setState({
      x: e.clientX,
      y: e.clientY,
    })
  }

  componentDidMount() {
    window.addEventListener('mousemove', this.handleMouseMove)
  }

  //注意需要在最后取消监听，以优化项目
  componnetWillUnmount() {
    window.removeEventListener('mousemove', this.handleMouseMove)
  }

  render() {
    return this.props.render(this.state)
  }
}

Mouse.defaultProps = {
  state: null,
}
//使用组件的一个组件，在其中使用组件并传递一个函数
class App extends Component {
  render() {
    return (
      <div>
        <Mouse
          render={mouse => {
            return (
              <p>
                鼠标位置：{mouse.x} {mouse.y}
              </p>
            )
          }}
        />
      </div>
    )
  }
}

export default App
```

举一反三，我们也可以用 props children 代替：

```jsx
import './App.css'
import React, { Component } from 'react'

class Mouse extends Component {
  // 鼠标位置state
  state = {
    x: 0,
    y: 0,
  }

  handleMouseMove = e => {
    this.setState({
      x: e.clientX,
      y: e.clientY,
    })
  }

  componentDidMount() {
    window.addEventListener('mousemove', this.handleMouseMove)
  }

  //注意需要在最后取消监听，以优化项目
  componnetWillUnmount() {
    window.removeEventListener('mousemove', this.handleMouseMove)
  }

  render() {
    return this.props.children(this.state)
  }
}

Mouse.defaultProps = {
  state: null,
}

class App extends Component {
  render() {
    return (
      <div>
        <Mouse>
          {mouse => {
            return (
              <p>
                鼠标位置：{mouse.x} {mouse.y}
              </p>
            )
          }}
        </Mouse>
      </div>
    )
  }
}

export default App
```

### 高阶组件（ 包装模式）

高阶组件(HOC)其实是一个函数，这个函数接收要包装的组件，返回增强后的组件。高阶组件内部创建一个类组件，在这个类组件中提供复用的状态逻辑代码，通过 prop 将复用的状态传递给被包装的包装组件：

```jsx
//高阶组件的使用方法
const EnhancedComponent = withHOC(WrappedComponent) //高阶组件我们约定以with开头

//高阶组件内部创建的类组件
function withHoc() {
  class Mouse extends React.Component {
    render() {
      return <WrappedComponent {...this.state} />
    }
  }
  return Mouse
}
```

例子（同 render props 的例子）

```jsx
//获取位置的公用组件
function withMouse(WrappedComopnent) {
  class Mouse extends Component {
    state = {
      x: 0,
      y: 0,
    }
    handleMouseMove = e => {
      this.setState({
        x: e.clientX,
        y: e.clientY,
      })
    }
    componentDidMount() {
      window.addEventListener('mousemove', this.handleMouseMove)
    }
    componentWillUnmount() {
      window.removeEventListener('mousemove', this.handleMouseMove)
    }

    render() {
      //注意这里需要同时传递props，因为如果包装后的组件传递属性，那么会被包装函数的组件中props接收，最终需要添加到返回值中，不然会使得props传递中断
      return <WrappedComopnent {...this.props} {...this.state} />
    }
  }
  return Mouse
}

//一个需要被包装的组件
class Posision extends Component {
  render() {
    return (
      <p>
        当前鼠标位置：{this.props.x} {this.props.y}
      </p>
    )
  }
}

//包装好的组件
const WithMousePosition = withMouse(Posision)

//最终呈现
class App extends Component {
  render() {
    return (
      <>
        <WithMousePosition />
      </>
    )
  }
}
export default App
```

但是在这种情况下，当打开 react 调试组件的时候，会发现被包装的组件名称叫作 Mouse 而不是 WithMousePosition。这是因为我们返回的 Mouse 其 displayName 是"Mouse"。

所以我们需要通过改变组件 displayName 的方式来更改返回组件的组件名，从而根据传入的组件来改变返回的组件名字（组件的 displayName 属性）

```jsx
function Mouse(WrappedComponent) {
  Mouse.displayName = `withMouse${
    WrappedComopnent.displayName || WrappedComopnent.name || 'Component'
  }`
  return Mouse
}
```

## React 组件优化

### 减轻 state

在 state 中仅存储和组件渲染以及状态管理相关的数据

### shouldComponentUpdate

`shouldComponentUpdate(nextProps, nextState)`函数返回 true 时，会允许 render 渲染，否则当返回 false 的时候则 render 不会触发。

由于一轮的状态更新，就会触发一次的 render 进行渲染，所以我们可以利用`shouldComponentUpdate`和`setState`的标准写法，来控制状态根据一定的条件判断是否渲染，从而避免没必要的组件渲染。

```jsx
increaseNum() {
	setState((state, props) => {
		num: state.num + 1
		})
	}
shouldComponentUpdate() {
      while(this.state.num < 3) return false
      return true //只有当state的num达到3的时候才会render渲染
    }
```

同时，由于当父组件改变时，整个父组件在的树都会被重新渲染，即其子组件也会被渲染。但是，有时的子组件是没有必要重新渲染的，这时就可以用`shouldComponentUpdate`来控制渲染

## 纯组件 PureComponent

`PureComponent` 可以减少不必要的更新，进而提升性能，每次更新会自动帮你对更新前后的 props 和 state 进行一个简单对比，来决定是否进行更新。 但是这里的比较是浅层比较，即基础类型的值改变了就是可以比较出来的，但是引用类型类如 object 就会出问题。

```jsx
class App extends PureComponent {
  state = {
    obj: {
      num: 1,
    },
  }
  clickHandle = () => {
    const newObj = this.state.obj
    //这里的num值虽然变化了，但是newObj的引用不变所以没有变化
    newObj.num += 1
    this.setState(state => {
      return {
        obj: newObj,
      }
    })
  }
  render() {
    return (
      <>
        {this.state.obj.num}
        <button onClick={this.clickHandle}>按钮</button>
      </>
    )
  }
}
```

这种情况下页面就不会重新渲染。因为引用没有变化。

所以此时就需要改变引用来实现渲染。

```jsx
class App extends PureComponent {
  state = {
    obj: {
      num: 1,
    },
  }
  clickHandle = () => {
    const newObj = {}
    Object.assign(newObj, this.state.obj)
    newObj.num++
    this.setState(state => {
      return {
        obj: newObj,
      }
    })
  }
  render() {
    return (
      <>
        {this.state.obj.num}
        <button onClick={this.clickHandle}>按钮</button>
      </>
    )
  }
}
export default App
```

或者这样：

```jsx
...
clickHandle = () => {
      const newObj = {...this.state.obj, num:this.state.obj.num + 1}
      this.setState((state) => {
        return {
          obj: newObj
        }
      })
    }
...
```

## React 路由

### 基本使用

前端路由是一套映射规则，在 React 中，是 URL 路径与组件的对应关系。

安装：

```bash
yarn add react-router-dom@5.30
```

由于版本更新缘故，v6 出现了很多新的特性，详情可以看这里：

[(6 条消息) React-Router v6 新特性解读及迁移指南\_前端劝退师-CSDN 博客](https://blog.csdn.net/weixin_40906515/article/details/104957712)

这里我们使用 5.30 版本的 react。

```jsx
//Pages.jsx
import React from 'react'
import { HashRouter as Router, Route, Link, Switch } from 'react-router-dom'
import App from './App'

const Pages = () => (
  <Router>
    <h1>这是路由</h1>
    <Link to="/app">页面一</Link>
    <Switch>
      <Route path="/app" component={App} />
    </Switch>
  </Router>
)

export default Pages
```

### 编程式导航（路由操作）

#### 跳转路由

使用`this.props.history.push('/xxx')`来转换路由

注意使用这个方法的组件必须是存在于路由系统中（在 route 中被记录过的）

#### 返回上一级

```jsx
handleOnclick = () => {
  this.props.history.go(-1) //返回上一个页面
}
```

### 默认路由

```jsx
const Pages = () => (
  <Router>
    <h1>这是路由</h1>
    <Link to="/app">页面一</Link>
    <Switch>
      {/*默认路由*/}
      <Route path="/" component={DefaultPage} />
      <Route path="/app" component={App} />
    </Switch>
  </Router>
)
```

### 模糊匹配

上面的默认路由的情况，当切换到`/app`路由的时候，默认路由对应的页面也会存在。这是由于 react 的路由匹配采用的是模糊匹配的方式（默认情况下）。

也就是说当 path 是'/'的时候，他可以匹配到所有路由。

当路由是`/first`的时候，它可以匹配到`/first`,`/first/a`,`first/a/b...`等路由。

### 精确匹配

为了避免匹配时的模糊匹配的请款，可以给路由加上`exact`属性

```jsx
const Pages = () => (
  <Router>
    <h1>这是路由</h1>
    <Link to="/app">页面一</Link>
    <Switch>
      {/*默认路由*/}
      <Route exact path="/" component={DefaultPage} />
      <Route path="/app" component={App} />
    </Switch>
  </Router>
)
```

注意由于`/app`路由还是模糊匹配，所以当出现`/app/a`类似这样的时候，这个路由对应的页面还是会出现。

## 其他

## render 更新机制

父组件渲染的时候会重新渲染当前的子组件，但子组件渲染的时候并不会使父组件和兄弟组件更新。

### Cannot read property 'setState' of undefined 解决方案

[React 中，报错"Cannot read property 'setState' of undefined"时，如何处理 - 前端报刊的个人空间 - OSCHINA - 中文开源技术交流社区](https://my.oschina.net/u/3946362/blog/2251944)

或者直接采用以下方案：

```jsx
import React from 'react'

class Hello extends React.Component {
  state = {
    count: 0,
  }
  handleClick() {
    this.setState({
      count: this.state.count + 1,
    })
  }
  render() {
    return (
      <>
        <h1> 计数器：{this.state.count}</h1>
        <button onClick={() => this.handleClick()}>+</button>
      </>
    )
  }
}

export default Hello
```

## Render 和 diff 判断

注意：**render 方法并不意味着渲染**，render 方法仅意味着更新了一个虚拟 DOM 树，而这个虚拟 DOM 树最终会和现有的 DOM 进行比较（通过 diff 算法）从而得知哪个节点需要更新，从而进行新一轮的渲染。



## Context机制

场景： 跨组件通讯 类似于provider和inject

实现：

```tsx
// context 
import { createContext } from "react";
export const { Provider, Consumer } = createContext({
  a: "Provide value",
});

// app.tsx
import Son from "./comp/Son";
import { Provider } from "./conetxt/idnex";
function App() {
  const [a, seta] = useState('123')
  return (
   <>
    <Provider value={ {a} }>
     <Son/>
    </Provider>
   </>
  );
}

// son.tsx
import { Consumer } from "../conetxt/idnex";
export default function () {
  return (
    <>
      <Consumer>{(value) => <span>{value.a}</span>}</Consumer>
    </>
  );
}
```



## children

 In JSX expressions that contain both an opening tag and a closing tag, the content between those tags is passed as a special prop: `props.children`. 

```tsx
// app.tsx
import Son from "./comp/Son";
function App() {
  return (
    <Son>
      <div>123</div>
    </Son>
  )
}

// son.tsx
import { PropsWithChildren } from "react";
export  function Son(prop: PropsWithChildren) {
  return (
    <>
      {prop.children}
    </>
  );
}
```



## 生命周期（React16之后）

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20221113124809.png)

