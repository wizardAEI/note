# React hooks

## 实现一个useWindowScroll hook

```ts
import { useState } from "react"

export default function() {
    const [height, setHeight] = useState(document.documentElement.scrollTop)
    window.addEventListener('scroll', (e) => {
        setHeight(document.documentElement.scrollTop)
    })
    return height
}
```

## 使用useEffect代替类组件生命周期

[useEffect代替常用生命周期函数（三） - 每天都要进步一点点 - 博客园 (cnblogs.com)](https://www.cnblogs.com/crazycode2/p/11746278.html#:~:text=用 useEffect 函数来代替生命周期函数 在使用 React,Hooks 的情况下，我们可以使用下面的代码来完成上边代码的生命周期效果，代码如下（修改了以前的diamond）： 记得要先引入 useEffect 后，才可以正常使用。)

## 使用useEffect清理副作用

在组件销毁的时候，有些副作用（如定时器）需要被清理：

```tsx
// son.tsx
function Son() {
    setInterval(() => {
        console.log('di')
      }, 1000)
    return (<div>son</div>)
}
```

此时当Son函数在父组件中被销毁时，定时器并不会因此被销毁掉。

我们可以使用useEffect函数的回调**返回值**，作为一个函数来执行清理动作（侧面说明useEffect返回值在函数销毁时调用，或者在执行下一个effect时）

```tsx
  useEffect(() => {
    const timer = setInterval(() => {
      console.log('di')
    }, 1000)
    return () => {
      clearInterval(timer)
    }
  }, []) // 注意第二个参数要加
```



## 使用useEffect发送请求

```ts
useEffect(() => {
	async function fn() {
		const res = await getXxx()
	}
	fn()
}, [])
```





## useContext

```tsx
// context
export const AppContext = createContext()

// App组件
function App() {
  const [number, setNumber] = useState(3)
  return (
    <AppContext.Provider value={{val: number}}>
      <div className="App">
        <Son></Son>
      </div>
    </AppContext.Provider>
  )
}

// son组件
export function Son() {
    const { val } = useContext(AppContext)
    return (
        <div>{val}</div>
    )
}
```



## useRef

`useRef` is a React Hook that lets you reference a value that’s not needed for rendering.

Usage:

1. Referencing a value with a ref

   we can call useRef to declare a value (the ref object that have current property to store information)

   the different between `useRef` and `useState` is: **changing a ref does not trigger a re-render and its value can be stored between re-renders** .

   **that means use useRef you can change and store information between re-renders**

2. 用于获取dom对象

```tsx
...

const divRef = useRef<HTMLDivElement>(null)
  useEffect(() => {
    console.log(divRef.current) //<div class="App">...</div>
  }, [])

...

return (
    <div className="App" ref={divRef}>
      123
      <Son></Son>
    </div>
  )
```

同时，类组件也具有ref属性:

```tsx
// 子类组件
export class ClassSon extends React.Component {
    render(): React.ReactNode {
        return (
            <div>
                class component
            </div>
        )
    }
}

// 父组件
const SonRef = useRef<ClassSon>(null)
useEffect(() => {
console.log(SonRef.current) // 组件实例
}, [])
return (
	<ClassSon ref={SonRef}></ClassSon>
)
```



## useEffect第二个参数为[]和不加第二个参数有什么区别

当第二个参数为[]时，useEffect只会在dom挂载完成后去执行一次，类似于类组件的componentDidMount。而如果不加第二个参数，则useEffect中的函数会在dom挂载完和每次更新时都执行一次。

也可以这样看，当第二个参数为[]时，则说明该副作用函数什么状态都不依赖。而如果不提供第二个参数表明什么都依赖，也就造成了在每一次组件需要更新时都回执行一次。

## memo

由于react所以每次当组件更新时都会去重新一颗虚拟dom树，所以每次更新组件，默认情况下会**自上而下递归**的对组件和其子组件更新。这样会带来一些没有必要的更新和性能损失。

**memo通过记忆组件渲染结果的方式来提高组件的性能表现（避免无效的重复渲染子组件，对应类组件中的shouldComponentUpdate）**

`React.memo` 仅检查 props 变更，未变更则不重新渲染。但如果函数组件被 `React.memo` 包裹，且其实现中拥有 [`useState`](https://zh-hans.reactjs.org/docs/hooks-state.html)，[`useReducer`](https://zh-hans.reactjs.org/docs/hooks-reference.html#usereducer) 或 [`useContext`](https://zh-hans.reactjs.org/docs/hooks-reference.html#usecontext) 的 Hook，当 state 或 context 发生变化时，它仍会重新渲染。

使用方式：

```tsx
const MyComponent = React.memo(function MyComponent(props) {
  /* 使用 props 渲染 */
});
```

默认情况下其只会对复杂对象做浅层对比，如果你想要控制对比过程，那么请将自定义的比较函数通过第二个参数传入来实现。

```
function MyComponent(props) {
  /* 使用 props 渲染 */
}
function areEqual(prevProps, nextProps) {
  /*
  如果把 nextProps 传入 render 方法的返回结果与
  将 prevProps 传入 render 方法的返回结果一致则返回 true，
  否则返回 false
  */
}
export default React.memo(MyComponent, areEqual);
```

>注意
>
>与 class 组件中 [`shouldComponentUpdate()`](https://zh-hans.reactjs.org/docs/react-component.html#shouldcomponentupdate) 方法不同的是，如果 props 相等，`areEqual` 会返回 `true`；如果 props 不相等，则返回 `false`。这与 `shouldComponentUpdate` 方法的返回值相反。

[React 顶层 API – React (reactjs.org)](https://zh-hans.reactjs.org/docs/react-api.html#reactmemo)



## useCallback

使用`useCallback`的背景问题：

在函数组件的情况下，当父组件的发生变化的时，由于函数组件的特征，会重新执行函数。其中定义的函数等引用类型会不断创建，其中函数的内容虽然还是一样，但是其实已经不一样了（因为不是基础类型）。

此时如果这个函数又是子组件的prop，则子组件即使有`memo`包裹，也会意外地重新创建。

此时我们就可以使用`useCallback`包裹住该函数生成新变量，再传递给子组件，并且根据依赖项判断该变量是否需要更新。

这样就不会出现由于父组件更新导致引用类型的变量一定被改变导致子组件意外更新了。

例子：

```jsx
function Main() {
  const useMemoryCallback = useCallback(() => {
    console.log('xxx')
  }, [])

  return (
    <ChildComponent fn={useMemoryCallback} />
  )
}
```

[前端 - hooks 系列五：useCallback_个人文章 - SegmentFault 思否](https://segmentfault.com/a/1190000040416622)

## hooks使用注意点

hooks在目前来说，需要保证每一次的函数组件渲染时，hooks顺序和多少不能变化。保证函数组件可以正确渲染。这是由于在构建时，reacct内部将函数组件中的hooks以链表的形式存储下来，并在之后的渲染中，遍历链表取出对应的数据进行组件更新。在这一过程中，如果我们更改了hooks的顺序或多少，那么对应的数据就会错误渲染或者浏览器报错。// TODO 查看当前版本的react还会不会有这样的问题



# react-router

## 使用方法

```
// 引入组件
import Home from './components/home'
import About from './components/about'

// 路由配置
import {
  BrowserRouter,
  Link,
  Routes,
  Route
} from 'react-router-dom'

function App() {
return (
  <BrowserRouter>
    <Link to='/'>首页</Link>
    <Link to='/about'>关于</Link>
    <Routes>
      <Route path='/' element={<Home/>}/>
      <Route path='/about' element={<About/>}/>
    </Routes>
  </BrowserRouter>
  )
}
```



## BrowserRouter和HashRouter

用于包裹整个应用，一个React应用只需要使用一次

两种常见的router：`BrowserRouter`和`HashRouter`

HashRouter：

使用URL的hash值实现（http://localhost:3000/#/about）

BrowserRouter

利用`window.history.pushState`API实现（http://localhost:3000/about）

使用案例：

```tsx
// 路由配置
import {
  BrowserRouter,
  Link,
  Routes,
  Route
} from 'react-router-dom'

function App() {
return (
  <BrowserRouter>
    <Link to='/'>首页</Link>
    <Link to='/about'>关于</Link>
    <Routes>
      <Route path='/' element={<Home/>}/>
      <Route path='/about' element={<About/>}/>
    </Routes>
  </BrowserRouter>
  )
}
```

  这里将路由设置在App出，我们也可以在最外层，即`main.tsx`中使用，如：

```tsx
ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
    <BrowserRouter>
    <Routes>
      <Route path='/' element={<App/>}/>
      <Route path='/home' element={<Home/>}/>
      <Route path='/about' element={<About/>}/>
    </Routes>
  </BrowserRouter>
)
```



## 路由跳转

```tsx
import { useNavigate } from 'react-router-dom'

    ...

const nav = useNavigate()
const toAbout = () => {
    nav('/about', {
        // repalce: true 表明无法回退
    })
}
```



## 携带参数

两种方式：

1. searchParams传参 （/xxx?val=123）

   ```tsx
   // 某个进行跳转的页面
   const nav = useNavigate()
   const toAbout = () => {
       nav('/about?val=123')
   }
   ...
   
   // about页面 注意这是v6版本，之前的版本可以使用
   const [routeParams] = useSearchParams('val=1&name=2') // 参数作为预设
       useEffect(() => {
           console.log(routeParams.get('val')) //123
           console.log(routeParams.get('name')) //2
       })
   ```

   上述版本可以在v6版本后使用，v6版本之前可以使用react-router-dom中提供的useLocation hook和query-string库。

   ```tsx
   // /comp?a=1&b=2
   import { useLocation } from 'react-router-dom';
   import queryString from 'query-string';
   
   function MyComponent() {
     const location = useLocation();
     const queryParams = queryString.parse(location.search);
     console.log(queryParams.a); // 输出1
     console.log(queryParams.b); // 输出2
     // ...
   }
   ```

   

2. params传参 (/xxx/123)

   需要注意的是，为了不让params传参被当成路由，我们需要修改`Route`，表明这里是一个参数

```tsx
// 在设置路由的地方
<BrowserRouter>
    <Routes>
        <Route path="/" element={<App />} />
        <Route path="/home" element={<Home />} />
        <Route path="/about/:id" element={<About />} />  // 这里要使 /:id 的形式
    </Routes>
</BrowserRouter> 
```

```tsx
// about页面
import { useParams } from 'react-router-dom';

function UserDetails() {
  const { id } = useParams();
  // ...
}
```



## 嵌套路由

嵌套路由即二级路由：

首先，我们在`main.tsx`中声明子路由：

```tsx
  <BrowserRouter>
    <Routes>
      <Route path="/home" element={<Home />}>
        <Route path="/home/son" element={<Son />}></Route>
      </Route>
      <Route path="/about/:id" element={<About />} />
    </Routes>
  </BrowserRouter>
```

然后我们在`Home.tsx`中声明一个二级路由出口（使用`Outlet`）

```tsx
import { Outlet } from "react-router-dom";

export default function Home() {
    return (
        <div>
            home
            <h1>子路由：</h1>
            <Outlet /> 
        </div>
    )
}
```

### 默认二级路由

要使用默认二级路由，去掉path，加上`index`属性

```tsx
<BrowserRouter>
    <Routes>
      <Route path="/home" element={<Home />}>
        <Route index element={<Son />}></Route>
      </Route>
      <Route path="/about/:id" element={<NotFound />} />
    </Routes>
</BrowserRouter>
```

## 404路由（兜底路由）

```tsx
<BrowserRouter>
    <Routes>	
      <Route path="/home" element={<Home />} />
      <Route path="/about/:id" element={<NotFound />} />
      <Route path="*" element={<About />} />
    </Routes>
</BrowserRouter>
```



# Mobx

## 环境配置

npm包：

```
mobx
mobx-react-lite
```

目录搭建：

```
src
 - store
  - counter.ts // 作为第一个mobx store案例
```

我们在一个组件中利用计数器案例来使用mobx：

在counter.ts中编写类：

```ts
import { makeAutoObservable } from "mobx"

class CounterStore {
    // 定义数据
    count = 0
    // 使数据响应式
    constructor() {
        makeAutoObservable(this)
    }
    // 定义action函数（修改数据）
    addCount = () => {
        this.count ++
    }
}

export const counterStore = new CounterStore()
```

在组件中使用`counterStore`

```tsx
import { observer } from "mobx-react-lite";
import { counterStore } from "../store/counter";

//被observer包裹的函数式组件会被监听在它每一次调用前发生的任何变化，也就包括了mobx的更改 如果不监听mobx，其实和memo一样
export default observer(function Home() {
  return (
    <div>
      <button onClick={counterStore.addCount}>点击增加</button>
      {counterStore.count}
    </div>
  );
});
```

我们尝试着把onClick事件更改一下：

```ts
onClick={() => {counterStore.count++}
```

发现对count的更改依旧生效。说明了mobx对响应式的处理类似于vue使用了defineProperty或者Proxy等，在get，set中进行了依赖收集和触发副作用。

## 计算属性

创建一个从其他 observable 中派生出来的 observable。但只要底层 observable 不变，这个值就不会被重新计算。

我们把上面的`counter.ts`稍作修改：

```ts
import { computed, makeAutoObservable } from "mobx"

class CounterStore {
    count = 0
    constructor() {
        makeAutoObservable(this, {
            sumCount: computed  // 在此处说明sumCount是一个计算属性
        })
    }
    addCount = () => {
        this.count ++
    }
    // 计算属性 注意要写成get property
    get sumCount() {
        return this.count + 3
    }
}

export const counterStore = new CounterStore()
```

在组件中使用：

```tsx
{counterStore.sumCount}
```



## 模块化

1. 不再从每一个store分别实例化，二是直接导出类

2. 在`store/index.ts`中统一实例化每个store类，利用react的Context机制来统一实例化

   ```tsx
   import { createContext, useContext } from "react";
   import { CounterStore } from "./counter";
   import { ListStore } from "./list";
   // 组合子模块
   class RootStore {
       counterStore
       listStore
        constructor() {
           // 实例化模块
           this.counterStore = new CounterStore()
           this.listStore = new ListStore()
       }
   }
   
   const rootStore = new RootStore
   // 这里createContext采用默认参数声明值，当不写StoreContext.Provider时会找到这个值
   const StoreContext = createContext(rootStore) 
   export const useStore = () => useContext(StoreContext) 
   
   ```

3. 在组件中实例化store来使用

   ```tsx
   import { observer } from "mobx-react-lite";
   import { useStore } from "../store";
   
   //被observer包裹的函数式组件会被监听在它每一次调用前发生的任何变化，也就包括了mobx的更改
   export default observer(function Home() {
     const { counterStore } = useStore()
     return (
       <div>
         <button
           onClick={() => {
             counterStore.count++;
           }}
         >
           点击增加
         </button>
         {counterStore.count}
         <h3>计算属性：</h3>
         {counterStore.sumCount}
       </div>
     );
   });
   ```




# 应用

## cdn部署

1. webpack项目可以使用`craco`进行cdn配置；配置文件为`craco.config.js`
2. vite项目 [vite+vue3使用cdn减小生成体积 | 摸鱼人的正常操作 (lzols.com)](https://www.lzols.com/articles/23550/) [vite-plugin-cdn-import - npm (npmjs.com)](https://www.npmjs.com/package/vite-plugin-cdn-import)

## 路由懒加载

主要使用到`lazy`方法和`<Suspense>`组件完成路由懒加载的效果

```tsx
import ReactDOM from "react-dom/client";
import "./index.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { lazy, Suspense } from "react";

const Home = lazy(() => import("./components/home"));

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <BrowserRouter>
    <Suspense
     fallback={<p>loading...</p>} // 没加载完成之前显示fallback
    >
      <Routes>
        <Route path="/" element={<Home />} />
      </Routes>
    </Suspense>
  </BrowserRouter>
);
```





# 深入React

[深入浅出React【真正吃透React知识链路与底层逻辑】共23讲_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1zB4y1773E/?spm_id_from=333.880.my_history.page.click&vd_source=9f4f5fa0ddf7994dab77edc934f59978)
