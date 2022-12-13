## Vue 的生命周期

1. 实例创建之前（对应周期函数 deforeCreate（））
2. 实例创建完成（对应周期函数 created（））
3. 模板编译之前（对应周期函数 beforeMount（））
4. 模板编译完成（对应周期函数 mounted（））
5. 数据更新之前（对应周期函数 beforeUpdate（））
6. 数据更新完成 （对应周期函数 updated（））
7. 实例销毁之前 （对应周期函数 beforeUnmount（））
8. 实例销毁完成 （对应周期函数 unmounted（））

增加两个

9. 缓存的组件激活 (activated)
10. 缓存的组件停用 (deactivated)

缓存的作用是将一些组件放到缓存中，而不是直接销毁，从而在缓存数据回复调用时增加效率

![vue-lifecycle](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/vue-lifecycle.png)

## 修饰器

### 事件修饰器

- `.stop`
- `.prevent`
- `.capture`
- `.self` 点击事件绑定本身才触发
- `.once`
- `.passive `对应`adEventListener`中的 passive 选项，可以忽略掉 event.preventDefault()，立即触发行为

```html
<!-- 阻止单击事件继续冒泡 -->
<a @click.stop="doThis"></a>

<!-- 提交事件不再重载页面 -->
<form @submit.prevent="onSubmit"></form>

<!-- 修饰符可以串联 -->
<a @click.stop.prevent="doThat"></a>

<!-- 只有修饰符 -->
<form @submit.prevent></form>

<!-- 添加事件监听器时使用事件捕获模式 -->
<!-- 即内部元素触发的事件先在此处理，然后才交由内部元素进行处理 -->
<div @click.capture="doThis">...</div>

<!-- 只当在 event.target 是当前元素自身时触发处理函数 -->
<!-- 即事件不是从内部元素触发的 -->
<div @click.self="doThat">...</div>
```

### 按键修饰符

Vue 为最常用的键提供了别名：

- `.enter`
- `.tab`
- `.delete` (捕获“删除”和“退格”键)
- `.esc`
- `.space`
- `.up`
- `.down`
- `.left`
- `.right`

### 系统修饰符

可以用如下修饰符来实现仅在按下相应按键时才触发鼠标或键盘事件的监听器。

- `.ctrl`
- `.alt`
- `.shift`
- `.meta`

### `.exact` 修饰符

```
<!-- 即使 Alt 或 Shift 被一同按下时也会触发 -->
<button @click.ctrl="onClick">A</button>

<!-- 有且只有 Ctrl 被按下的时候才触发 -->
<button @click.ctrl.exact="onCtrlClick">A</button>

<!-- 没有任何系统修饰符被按下的时候才触发 -->
<button @click.exact="onClick">A</button>
```

### 鼠标按钮修饰符

- `.left`
- `.right`
- `.middle`

这些修饰符会限制处理函数仅响应特定的鼠标按钮。

## Vue3.2 setup 语法糖：

### 组件导入,ref 等的引入，方法和响应式数据的定义（无需返回）

```vue
<script setup>
import { ref } from '@vue/reactivity'
import HelloWorld from './components/HelloWorld.vue'
const func1 = () => {
  console.log('hello this is emit')
}
const text = ref('hello vue3')
</script>
```

### Vue3.2 + ts 中使用 vuex

直接 store.state.msg 和监听都可以将 vuex 的值响应式的显现出来

```vue
<!--某vue文件-->
<template>
  {{ store.state.msg }}
  {{ msg }}
</template>

<script setup lang="ts">
import { isRef, computed } from 'vue'
import { useStore } from 'vuex'
const store = useStore()
const msg = computed(() => store.state.msg)
setTimeout(() => {
  store.commit('setMsg', 'abc')
}, 3000) //调用mutations
</script>
```

module 模块化的用法

```ts
// ./one/index.ts
interface State {
  msg: string
}

const one = {
  namespaced: true, //让这里的东西独立成模块
  state: {
    msg: 'one hello',
  },
  mutations: {
    setMsg(state: State, str: string) {
      state.msg = str
    },
  },
}

export { one }
```

```ts
// index.ts
import { createStore } from 'vuex'
import { one } from './one/index'

export const store = createStore({
  state: {
    msg: 'storeData',
  },
  mutations: {
    setMsg(state, str: string) {
      state.msg = str
    },
  },
  strict: true, //开启严格模式，只有在mutation中才可以更改state
  modules: {
    one,
  },
})
```

```vue
<template>
  {{ store.state.msg }}
  {{ msg }}
  {{ store.state.one.msg }}
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useStore, mapState } from 'vuex'
const store = useStore()
const msg = computed(() => store.state.msg)
setTimeout(() => {
  store.commit('setMsg', 'abc')
}, 3000)
setTimeout(() => {
  store.commit('one/setMsg', 'def')
}, 3000)
</script>
```

### jsx 支持

插件

```
 npm i @vitejs/plugin-vue-jsx -D
```

```
<script lang = 'jsx'>
    import { ref } from "vue";
    export default {
        setup () {
            const msg = ref('hi jsx')
            return ()=>(<>
                    <div>this is jsx</div>
                    <p> this is the reactive data</p>
                    <p> {msg.value} </p>
                </>)
        }
    }
</script>

<style scoped lang="less">

</style>
```

### mock 支持

插件

```
npm i vite-plugin-mock -D
npm i  mockjs -S
```

### eslint 等

[vite+vue3+ts eslint 不生效的(终极解决办法) - 掘金 (juejin.cn)](https://juejin.cn/post/6989500697246957604)

### Vue3 的 prototy

使用方法：

```js
// //全局方法
app.config.globalProperties.fn = () => {
  console.log('ss')
}
// 使用全局方法
import { getCurrentInstance } from 'vue'
const { appContext } = getCurrentInstance()
appContext.config.globalProperties.fn()
```

### Vue 获取 Dom

```javascript
//Vue2 获取DOM
<div ref=“Ref”></div>
this.$refs.Ref
//Vue3 获取单DOM
<template>
  <div ref=“Ref”>获取单个DOM元素</div>
</template>
<script>
import { ref, onMounted } from ‘vue’;
export default {
  setup() {
    const Ref = ref(null);
    onMounted(() => {
      console.dir(Ref.value);
    });
    return {
      Ref
    };
  }
};
</script>
//Vue3 获取多DOM
<template>
  <div>获取多DOM元素</div>
  <ul>
    <li v-for=“(item, index) in arr” :key=“index” :ref=“setRef”>
      {{ item }}
    </li>
  </ul>
</template>
<script>
import { ref, nextTick } from ‘vue’;
export default {
  setup() {
    const arr = ref([1, 2, 3]);
    // 存储dom数组
    const Ref = ref([]);
    const setRef = (el) => {
      Ref.value.push(el);
    };
    nextTick(() => {
      console.dir(Ref.value);
    });
    return {
      arr,
      setRef
    };
  }
};
</script>
```

### 单文件组件

### mixin

```js
Vue2.x 中mixin的使用
// mixin.js
export default{
	data(){
		return{
		}
	},
	created() {
    	// do something...
  	},
	methods:{...}
}

// vue页面中引入
import mixin from 'mixin.js'
export default{
	data(){},
	mixins: [mixin]
}
在mixin定义的方法和值可以在所有引入 mixin.js 的vue页面中调用。
例如 methods、components 和 directives，将被合并为同一个对象。两个对象键名冲突时，取组件对象的键值对。

Vue3中mixin的使用
// mixin.js
import { computed, ref } from 'vue'
export default function () {
	setup(){
		const count = ref(1)
		const plusOne = computed(() => count.value + 1)
		function hello(){
			console.log('hello mixin'+plusOne.value)
		}
		return{
			count,
			plusOne,
			hello
		}
	}
}

// vue页面中引入
import mixin from 'mixin.js'
export default{
	setup(){
		const { count, plusOne, hello } = mixin().setup()
		hello()
		console.log(count.value, plusOne.value)
	}
}

// 调用组件中的局部变量
export default {
  setup () {
    // 某个局部值的合成函数需要用到
    const myLocalVal = ref(0);

    // 它必须作为参数显式地传递
    const { ... } = mixin(myLocalVal);
  }
}
```

### vue.use

[关于 Vue.use()详解 - 简书 (jianshu.com)](https://www.jianshu.com/p/89a05706917a)

[Vue.use()实现原理；使用插件；开发插件 - 简书 (jianshu.com)](https://www.jianshu.com/p/7da83fb72420)

### Vite 中配置别名

```js
//配置vite.config.js

import path from 'path'

export default defineConfig({
  resolve: {
    extensions: [
      '.mjs',
      '.js',
      '.jsx',
      '.ts',
      '.tsx',
      '.json',
      '.sass',
      '.scss',
    ],
    alias: {
      '@': path.resolve(__dirname, 'src'),
      '@components': path.resolve(__dirname, 'src/components'),
    },
  },
})
```

```ts
//tsconfig.js
{
    "compilerOptions": {
        "paths":{
            "@/*": ["src/*"],
            "@components/*": ["src/components/*"],
        },
        }
    }
```

### ref Attribute

vue2:

```js
//template
;<base-input ref="usernameInput"></base-input>

//js
this.$refs.usernameInput.focusInput()
```

vue3

```js
//template
<input type="text"  ref="inputVal" />
    <a-button type="primary" ref="Btn" id="btn">按钮</a-button>

//js
const inputVal = ref()
onMounted(()=> {
    (inputVal.value as HTMLInputElement).focus()
    //这里注意类型，当我们使用组件库的时候，它们常常是一给span块，例如<a-button>
})
```

### Diff 算法

[详解 vue 的 diff 算法 - \_wind - 博客园 (cnblogs.com)](https://www.cnblogs.com/wind-lanyan/p/9061684.html)

[②Vue3 性能比 Vue2 好的原因（diff 算法优化、静态提升、事件侦听器缓存）\_一川烟草，满城风絮-CSDN 博客](https://blog.csdn.net/qq_45613931/article/details/109470718)

[vue3.0 diff 算法详解(超详细) - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/150103393)

[Vue Template Explorer (vue-next-template-explorer.netlify.app)](https://vue-next-template-explorer.netlify.app/#{"src"%3A"\r\n 123<%2Fspan>\r\n {{msg}}<%2Fbutton>\r\n<%2Fdiv>\r\n"%2C"ssr"%3Afalse%2C"options"%3A{"mode"%3A"module"%2C"filename"%3A"Foo.vue"%2C"prefixIdentifiers"%3Afalse%2C"hoistStatic"%3Atrue%2C"cacheHandlers"%3Afalse%2C"scopeId"%3Anull%2C"inline"%3Afalse%2C"ssrCssVars"%3A"{ color }"%2C"compatConfig"%3A{"MODE"%3A3}%2C"whitespace"%3A"condense"%2C"bindingMetadata"%3A{"TestComponent"%3A"setup-const"%2C"setupRef"%3A"setup-ref"%2C"setupConst"%3A"setup-const"%2C"setupLet"%3A"setup-let"%2C"setupMaybeRef"%3A"setup-maybe-ref"%2C"setupProp"%3A"props"%2C"vMySetupDir"%3A"setup-const"}}})

### SSR

[服务端渲染指南 | Vue.js (vuejs.org)](https://v3.cn.vuejs.org/guide/ssr/introduction.html#什么是服务端渲染-ssr)

### 单文件组件样式特性（状态驱动的动态 CSS）

[单文件组件样式特性 | Vue.js (vuejs.org)](https://v3.cn.vuejs.org/api/sfc-style.html#状态驱动的动态-css)

### Vite 的.env 文件

[环境变量和模式 {#env-variables-and-modes} | Vite 中文网 (vitejs.cn)](https://vitejs.cn/guide/env-and-mode.html#env-files)

[vite 添加环境变量 import.meta.env (talktocomputer.site)](https://talktocomputer.site/blogs/161/)

[渲染函数 & JSX — Vue.js (vuejs.org)](https://cn.vuejs.org/v2/guide/render-function.html)



## Vue 的优缺点

优点

- 渐进式框架，使用方便
- spa 单页面应用，跳转快速
- 组件化开发，响应式数据，mvvm 架构，开发更加容易

缺点

- 单页面应用不利于 SEO
- 第一次加载慢
- 不兼容 IE



## Vue的虚拟Dom和组件

虚拟Dom是用来描述真实dom的一个对象，使用它我们可以更灵活的描述dom和进行渲染（即使用`document.createElment()`新增dom等）。例如，我们有一个`div`对象：

```js
vnode = {
	tag: 'div',
	props: {
		onClick: () => { console.log('xxx') }
	},
	children: 'click me'
}
```

那么我们就可以根据虚拟dom来渲染出真实dom：

```html
<div onClick="() => { console.log('xxx') }" >
    click me
</div>
```

组件：

组件就是对一组dom的封装，vue在组件的实现上，也是通过解析成虚拟dom：

```js
myCompnent = function() {
    return {
        tag: 'div',
        props: {
            onClick: () => { console.log('xxx') }
        },
        children: 'click me'
    }
}

vnode = {
	tag: myCompnent
}
```

与普通dom不同的是，组件的tag并不是字符串，而是一个函数（这里只是vue这么做而已，完全可以改成对象或者其他的）。在渲染时，根据tag形式来区分dom和组件，从而对组件进行执行返回其包裹的dom元素来渲染dom。

## 实现 Vue 的 v-model 功能

```vue
<template>
  <input type="text" v-model="input.val" />
  <input type="text" :value="input.val" @input="changeVal" />
  //利用bind触发事件来实现
  {{ input.val }}
</template>

<script setup>
import { reactive } from 'vue'
const input = reactive({
  val: 1,
})
const changeVal = e => {
  input.val = e.target.value
}
</script>
```

如果要将 input 封装起来，可以使用两种方案：

- 使用 provide 和 inject 传递响应式数据
- 使用 emits 和 props 传递数据和方法

## Vue render 的作用

渲染 dom 并返回一个虚拟 DOM

## vite 为什么快，有什么缺点

vite 在开发环境的时候会按需加载（使用 esbuild 构建依赖），并且直接返回 es module 的 js 代码，交给浏览器解析（缺点：会给浏览器负担和按需加载遇到错误才报错）

在生产环境的时候使用了 rollup 打包

## 为什么 Vue 的 data 是函数而不是对象

因为对象是引用类型，多次 new 实例的时候会造成多个实例使用同一个对象的情况。而函数不同，函数是返回一个新对象。

## Vue2 使用 defineProperty 和 Vue3 使用 proxy 的区别

粒度不同，proxy 是相当于对整个对象进行了拦截，而 defineProperty 是对对象的属性进行 get 和 set，这也就造成了如果在对象里直接新增属性，会导致监听不到的情况。并且 defineProperty 是无法对数组进行深度监听的，对于数组的 push，unshift 都是监听不到的

## vue3 tree-shaking 的作用是什么

在编译时就能确定模块的依赖关系 ，从而达到去除无用代码，依赖的效果。

其中tree-shaking就是判断是否要去掉某个依赖，即判断当前依赖是否产生了副作用。

这个功能最开始是由rollup带来的。他会将不使用的和一些可以判断出不产生副作用的方法在打包的时候去除掉。

vue利用这个特性，在其代码中，对一些顶级调用的函数标记上`/*#__PURE__*/`表明该函数没有被其他函数调用时可以放心的去除。

## Vue3 的 diff 算法和静态提升

vue 的 diff 算法用来判断 dom 树中的节点是否有变化，有变化则替换；其中 vue 做出的优化是：1.只比较同层的 dom 2.当节点的标签不同的时候，直接删除，不继续深层比较 3.比较 key，如果 key 相同则认为是相同节点也不进行深层比较。

vue3 增加了一个静态提升，即给不会更改的虚拟 dom 打上静态的标签，之后比较的时候就不比较静态 dom 了，渲染的时候也会直接复用。

## 详细说一下 Vue 的 Mixin

mixin 的主要作用是用来分发 vue 组件中的可复用的部分，同时可以在全局注册一个`app.mixin()`来全局复用一些组件的选项（注意虽然每个组件都可以复用，组件内也是响应式的，但是组件间就不是响应式的了）

在 vue2 中，专门有 mixins 选项来表明复用某个 mixin 文件，当有和本组件产生出冲突的属性时，组件内的属性优先

vue3 中，增加了组合式 API，可以使用` const {obj1, obj2} = mixin1.setup()`,更加灵活的复用 mixin 文件中的特定属性或方法



## vue 的数据响应式，双向绑定，数据驱动是什么？简述一下 Vue 的数据驱动

数据响应式指的是当我们修改逻辑层的数据的时候，页面会随之更新，避免了繁琐的 DOM 操作，这也是 mvvm 框架的一大优势。

双向绑定是指数据层和逻辑层双向绑定，一起更新。vue 中可以使用 v-model 实现双向绑定

不同于微信小程序的 setdata 和 react 的 setState，vue 的数据驱动过程只用关注数据本身不必关心如何渲染到视图层。核心原理在于 vue 的数据劫持(vue2 的 defineProperty，vue3 的 proxy)。进行数据劫持，当数据发生改变的时候会自动触发监听事件并进行更新 dom

## Vue 的依赖收集是什么？

Vue 对需要响应式的数据进行**依赖收集**，当它们的值发生改变时通知页面重新渲染，并触发相关的 callback。

这是一种经典的订阅发布模式。

[深入浅出 Vue 基于“依赖收集”的响应式原理 - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/29318017)

[深入响应性原理 | Vue.js (vuejs.org)](https://v3.cn.vuejs.org/guide/reactivity.html#什么是响应性)

```js
/**
 * 定义一个“依赖收集器”
 */
const Dep = {
  target: null,
}

/**
 * 使一个对象转化成可观测对象
 * @param { Object } obj 对象
 * @param { String } key 对象的key
 * @param { Any } val 对象的某个key的值
 */
function defineReactive(obj, key, val) {
  const deps = []
  Object.defineProperty(obj, key, {
    get() {
      console.log(`我的${key}属性被读取了！`)
      if (Dep.target && deps.indexOf(Dep.target) === -1) {
        deps.push(Dep.target)
      }
      return val
    },
    set(newVal) {
      console.log(`我的${key}属性被修改了！`)
      val = newVal
      deps.forEach(dep => {
        dep()
      })
    },
  })
}

/**
 * 把一个对象的每一项都转化成可观测对象
 * @param { Object } obj 对象
 */
function observable(obj) {
  const keys = Object.keys(obj)
  for (let i = 0; i < keys.length; i++) {
    defineReactive(obj, keys[i], obj[keys[i]])
  }
  return obj
}

/**
 * 当计算属性的值被更新时调用
 * @param { Any } val 计算属性的值
 */
function onComputedUpdate(val) {
  console.log(`我的类型是：${val}`)
}

/**
 * 观测者
 * @param { Object } obj 被观测对象
 * @param { String } key 被观测对象的key
 * @param { Function } cb 回调函数，返回“计算属性”的值
 */
function watcher(obj, key, cb) {
  // 定义一个被动触发函数，被依赖收集，当这个“被观测对象”的依赖更新时调用
  const onDepUpdated = () => {
    const val = cb()
    onComputedUpdate(val)
  }

  Object.defineProperty(obj, key, {
    get() {
      Dep.target = onDepUpdated
      // 执行cb()的过程中会用到Dep.target，
      // 当cb()执行完了就重置Dep.target为null
      const val = cb() //在cb函数中读取了可观测对象
      Dep.target = null
      return val
    },
    set() {
      console.error('计算属性无法被赋值！')
    },
  })
}

const hero = observable({
  health: 3000,
  IQ: 150,
})

watcher(hero, 'type', () => {
  return hero.health > 4000 ? '坦克' : '脆皮' //这里产生了对可观测属性的读取
})

console.log(`英雄初始类型：${hero.type}`)

hero.health = 5000

我的health属性被读取了！
英雄初始类型：脆皮
我的health属性被修改了！
我的health属性被读取了！
我的类型是：坦克
```



## v-if和v-for的优先级

### vue2：

编写一个`p`标签，同时使用`v-if`与 `v-for`

```html
<div id="app">
    <p v-if="isShow" v-for="item in items">
        {{ item.title }}
    </p>
</div>
```

模板指令的代码都会生成在`render`函数中，通过`app.$options.render`就能得到渲染函数

```js
ƒ anonymous() {
  with (this) { return 
    _c('div', { attrs: { "id": "app" } }, 
    _l((items), function (item) 
    { return (isShow) ? _c('p', [_v("\n" + _s(item.title) + "\n")]) : _e() }), 0) }
}
```

`_l`是`vue`的列表渲染函数，函数内部都会进行一次`if`判断

初步得到结论：vue2中的`v-for`优先级是比`v-if`高

### vue3:

template:

```html
<div v-for="item in arr" v-if="isShow">
    Hello World
</div>
```

对应的render函数：

```js
export function render(_ctx, _cache, $props, $setup, $data, $options) {
  return (_ctx.isShow)
    ? (_openBlock(true), _createElementBlock(_Fragment, { key: 0 }, _renderList(_ctx.arr, (item) => {
        return (_openBlock(), _createElementBlock("div", null, "Hello World"))
      }), 256 /* UNKEYED_FRAGMENT */))
    : _createCommentVNode("v-if", true)
}
```

可以看到这里使用了三元表达式，先进行的v-if的判断，如果`isShow`为`true`则进行下面的列表渲染

初步得到结论：vue3中的`v-if`优先级是比`v-for`高



## vue如何扩展组件

在选项式api中，我们可以使用这些方法：

1. 通过插槽来拓展组件
2. 可以通过mixin拓展组件
3. 通过extends选项进行组件继承

在组合式api中，我们可以使用：

1. app.mixin() 进行全局注入。组合式api中不存在单个组件的mixin了
2. 逻辑复用采用组合式函数：[组合式函数 | Vue.js (vuejs.org)](https://cn.vuejs.org/guide/reusability/composables.html)

关于逻辑复用的概念，这其实是由于hooks的写法带来的一种优势，可以将有状态的函数封装起来进行复用。





## Jsx是怎么在JavaScript中生效的：

jsx会被编译成`React.createElement()`,`React.createElement()`将返回一个叫`React Element`的JS对象（编译靠babel）。

我们可以使用babel官网的在线演示工具来试验jsx的编译效果：

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20221113104714.png)

