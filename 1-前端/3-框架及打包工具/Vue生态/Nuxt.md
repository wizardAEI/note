# 服务端渲染（SSR）

默认情况下，Vue.js可以在浏览器中输出 Vue 组件，进行生成 DOM 和操作 DOM。然而也可以将同一个组件渲染为服务器端的 HTML 字符串，将它们直接发送到浏览器，最后将这些静态标记"激活"为客户端上完全可交互的应用程序。 这种方式便称为SSR。

参考资料：

[服务端渲染(SSR) - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/90746589) 

# Nuxt2

## 起步

参考资料：

 [Nuxt - Installation (nuxtjs.org)](https://nuxtjs.org/docs/get-started/installation) 

 [Nuxt项目搭建到Nuxt项目部署 - 简书 (jianshu.com)](https://www.jianshu.com/p/bbe874c32f90) 

 [介 绍 - Nuxt.js 中文文档 - 服务端渲染 Vue 应用 2.11.X - 长乐未央 (clwy.cn)](https://clwy.cn/guide/pages/nuxt-v2-introduce) 



## nuxt特有生命周期

### asyncData

asyncData方法会在组件（限于页面组件）每次**加载之前**（被调用。它可以在服务端或路由更新之前被调用。在这个方法被调用的时候，第一个参数被设定为当前页面的上下文对象，你可以利用 asyncData方法来获取数据，Nuxt.js 会将 asyncData 返回的数据融合组件 data 方法返回的数据一并返回给当前组件。

例如：

```js
async asyncData({$axios}) {
    const res = await $axios.$get("http://localhost:5000");
    return {content: res.content};
  },
```

content会被作为data中的属性使用

例如我们可以直接这样：

```js
<template>
  <div>{{ content }}</div>
</template>
```

### fetch

 fetch 方法用于在渲染页面前填充应用的状态树（store）数据， 与 asyncData 方法类似，不同的是它不会设置组件的数据。 

例如：

```vue
<template>
  <h1>Stars: {{ $store.state.stars }}</h1>
</template>

<script>
export default {
  async fetch ({ store, params }) {
    let { data } = await axios.get('http://my-api/stars')
    store.commit('setStars', data)
  }
}
</script>
```

如果要在fetch中调用并操作store，请使用store.dispatch，但是要确保在内部使用async / await等待操作结束：

```vue
<script>
export default {
  async fetch ({ store, params }) {
    await store.dispatch('GET_STARS');
  }
}
</script>
```

store/index.js

```js
export const actions = {
  async GET_STARS ({ commit }) {
    const { data } = await axios.get('http://my-api/stars')
    commit('SET_STARS', data)
  }
}
```



### Nuxt加载全局配置（例如CSS）

assets目录下：

```css
/*assets/style/main.css*/
body {
  margin: 0 !important;
}
```

nuxt.config.js:

```js
export default {
    //...
    css: ['@/assets/style.css'],
    //...
}
```



## 解决nuxt的跨域问题

 [(10条消息) nuxt跨域_明月别枝的博客-CSDN博客_nuxt跨域](https://blog.csdn.net/lemisi/article/details/99637257) 

```js
 axios: {
    // Workaround to avoid enforcing hard-coded localhost:3000: https://github.com/nuxt-community/axios-module/issues/308
    proxy: true, // 表示开启代理
    prefix: "/api", // 表示给请求url加个前缀 /api
    credentials: true, // 表示跨域请求时是否需要使用凭证
  },
  proxy: {
    "/api": {
      target: "http://localhost:3001", // 目标接口域名
      changeOrigin: true, // 表示是否跨域
      pathRewrite: {
        "^/api": "/", // 把 /api 替换成 /
      },
    },
  },
```



## 路由守卫

虽然nextjs不需要写路由，但出于安全可以写路由守卫来拦截某些跳转。首先在plugins新建一个路由文件，比如router.js：

```js
export default ({ app, store }) => {
  app.router.beforeEach((to, from, next) => {
    // 设置条件
    console.log(to, from);
    next();
  });
};
```

 再在`nuxt.config.js`中加入plugin字段：

```js
plugins: ["@/plugins/router"] 
```

注意官方的这句话：

如果您的项目中直接使用了`node_modules`中的`axios`，并且使用`axios.interceptors`添加拦截器对请求或响应数据进行了处理，确保使用 `axios.create`创建实例后再使用。否则多次刷新页面请求服务器，服务端渲染会重复添加拦截器，导致数据处理错误。 



## nuxt集成Cesium (暂定)

1. 初始化nuxt项目

2. `npm i cesium -D`下载cesium

3. 将`/node_modules/cesium/Build/Cesium`文件导入到`static`静态文件中

4. ```js
   //在需要使用到cesium的页面文件中添加声明钩子函数加载cesium
   import * as cesium from 'cesium'
   export default {
     name: 'IndexPage',
     mounted() {
       cesium.Ion.defaultAccessToken =  'yourToken'
       const viewer = new cesium.Viewer(this.$refs.cesiumContainer, {
         infoBox: false,
       })
       window.viewer = viewer
     },
   }
   ```

5. 直接这样使用后，会提示`CESIUM_BASE_URL`不存在，所以写一个plugin将其在vue渲染之前加载上去：

   ```js
   // pligins/cesium.js
   import Vue from 'vue'
   
   /**
    * @type {import('vue').PluginObject}
    */
   const Init = {
     install() {
       window.CESIUM_BASE_URL = '/Cesium/' //由于cesium文件放在了static中，在服务器加载时他的相对路径就是/
     },
   }
   
   Vue.use(Init)
   ```

6. 添加在`nuxt.config.js`文件中:

   ```js
   plugins: [
       ...
       {
         src: '@/plugins/cesium',
         ssr: false, //设置ssr为false，不然会提示window不存在,这是因为当ssr设置false时，插件只在客户端运行
       },
     ],
   ```

## Nuxt生命周期

 ![查看源图像](https://resource.shangmayuan.com/droxy-blog/2020/06/08/0256156c2014484383028b43ed88d457-1.jpg) 

 [nuxt生命周期讲解 - 前端小白狐 - 博客园 (cnblogs.com)](https://www.cnblogs.com/XF-eng/p/14611496.html) 

# Nuxt3

## 起步

参考资料：

https://v3.nuxtjs.org/