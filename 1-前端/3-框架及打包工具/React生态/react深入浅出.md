## CreateElement和ReactElement的作用

createElement相当于一个处理层，将格式化jsx编译后的产生的`type`，`props`,`children`进行梳理，转换成ReactElement需要的参数，然后调用ReactElement并返回。

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20221113110225.png)

ReactElement主要起到创建虚拟Dom的作用，其中包含了各种对于dom的描述。通过`ReactDom.render()`方法对虚拟dom进行渲染并创建真实dom。

## componentWillReceiveProps()生命周期

当类组件更新导致重新渲染时会触发该方法，即使父组件的props没有改变，也会调用该方法。如果只想处理改变请确保进行当前值与更改值的比较。

react16之后`componentWillReceiveProps`可以使用`getDerivedStateFromProps`和`componentDidUpdate`组合代替其功能。

## React fiber架构

在react16之前。生成的虚拟dom树在进行diff算法后，生成渲染dom树进行render。这个render过程是递归且不可被打断的。在这个过程中，render一直占据主线程，导致可能会出现一些其他任务无法执行的情况。

fiber架构将渲染任务拆分成多个小任务，进行分次，可被打断的**异步**渲染部分，并且记录渲染中断点从而可以继续渲染。

### fiber架构下的注意点

由于fiber架构下，render过程是可以被打断的，所以又将render分为`render perse`和`人render commit`两个阶段。render parse阶段一直到render函数被执行后，而render commit则是真正生成dom到挂载完成的过程。

`render perse`可以被打断，从而使得在这个周期内部的生命周期钩子都是可能重复执行的。这也是为什么react16放弃了`componentWillMount`,`componentWillupdate`,`componentWillReceiveProps`几个声明周期。因为他们都可能产生副作用且重复执行。 相比之下，`getDerivedStateFromProps`不允许在函数中访问this,想要更改state也是通过返回值的方式，更加安全。

## 在react组件中一个元素绑定onClick事件，点击后总会向上传播，如何阻止冒泡？

React 为提高性能，有自己的一套事件处理机制（合成事件），相当于将事件代理到全局进行处理，也就是说监听函数并未绑定到DOM元素上。因此，如果你使用禁止react事件冒泡`e.stopPropagation()`，其实无法阻止原生事件冒泡（但可以阻止react的组合事件冒泡）；你禁用原生事件冒泡`e.nativeEvent.stopPropagation()`，React的监听函数就调用不到了。

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

