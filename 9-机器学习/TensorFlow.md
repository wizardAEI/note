## 机器学习

训练机器学习模型的步骤包括：

制定任务：

- 是回归问题还是分类问题？
- 可以通过监督式学习还是非监督式学习来完成？
- 输入数据的形状是什么？输出数据应该是什么样的？

准备数据：

- 清理数据并尽可能手动检查它是否存在任何模式
- 在使用数据进行训练之前对数据进行重排
- 将数据归一化为神经网络的合理范围。通常，对于数值数据，0-1 或 -1-1 是合适的范围。
- 将数据转换为张量

构建并运行您的模型：

- 使用 `tf.sequential` 或 `tf.model` 定义模型，然后使用 `tf.layers.*` 向模型中添加层（层中可指定函数）
- 选择优化器`optimize`（[adam](https://developers.google.com/machine-learning/glossary/#optimizer) 随机梯度下降法通常是一个不错的选择），以及批次大小和周期数等参数。
- 为您的问题选择合适的[损失函数](https://developers.google.com/machine-learning/glossary/#loss)`loss`，并选择准确率指标来帮助您评估进度。[`meanSquaredError`](https://developers.google.com/machine-learning/glossary/#MSE) 是处理回归问题的常见损失函数。
- 监控训练，看看损失是否降低

评估模型

- 为您的模型选择一个评估指标，您可以在训练过程中对模型进行监控。训练完成后，请尝试进行一些测试预测，以了解预测质量。



## 名词解释：

### 张量 tensor

一个包含着数学属性的结构，这些数学属性可以是一个数，一个数组，矩阵（一维，多维）

张量具有value，shape，size， dtype (float int boolean)







## TensorFlow

### 张量 Tensor

中央单元`tf.Tensor` ：一组形状为一维或多维数组的值。

#### 包含的属性

 `rank`: 维度 `   shape`：维度大小(形状)     `dtype`：张量的数据类型

#### 创建方法

`tf.tensor(value,shape,dtype)`

```js
//例
const a = tf.tensor([[1, 2], [3, 4], [5, 6]])
//或
const b = tf.tensor([1, 2, 3, 4, 5, 6], [3,2])
//两种创建方法的tensor都是 [[1, 2], [3, 4], [5, 6]]
```

### 重塑 reshape

 [`tf.Tensor`](https://tensorflow.google.cn/api_docs/python/tf/Tensor) 中元素的数量是其形状大小的乘积。由于通常可以有多个具有相同大小的形状，因此将 [`tf.Tensor`](https://tensorflow.google.cn/api_docs/python/tf/Tensor) 重塑为具有相同大小的其他形状通常非常实用。这可以通过 `reshape()` 方法实现： 

```js
const a = tf.tensor([[1, 2], [3, 4]]);
const b = a.reshape([4, 1]);//参数为 reshape(shape)
b.print()//[[1], [2], [3], [4]]
```

### 获取Tensor数据

通过`data()`,`array()`来获取tensor的数据，但注意，这是异步的

```js
async function writeDataEl() {
        let data = await b.data()
    }
```

同时，也有同步获取数据的方法`dataSync()`和`arraySync()`，但是可能会浪费性能

### 运算

例如x<sup>2</sup>运算：

```js
const x = tf.tensor([1, 2, 3, 4]);
const y = x.square();  // equivalent to tf.square(x)
y.print();
```

 由于张量是不可变的，因此这些运算不会改变其值。相反，return 运算一般会返回新的 [`tf.Tensor`](https://tensorflow.google.cn/api_docs/python/tf/Tensor) 。同时，一些运算函数可能不是同步的，所以要看清其返回值（可能返回promise）。

### 内存

为了防止内存泄漏，我们需要管理内存

#### dispose 销毁内存

```js
const a = tf.tensor([[1, 2], [3, 4]]);
a.dispose(); // Equivalent to tf.dispose(a)
```

#### tidy 清理内存

 清理执行函数后未被该函数返回的所有 [`tf.Tensor`](https://tensorflow.google.cn/api_docs/python/tf/Tensor)，类似于执行函数时清理局部变量的方式： 

```js
const a = tf.tensor([[1, 2], [3, 4]]);
const y = tf.tidy(() => {
  const result = a.square().log().neg();
  return result;
});
```

 在此示例中，`square()` 和 `log()` 的结果将被自动处置。`neg()` 的结果不会被处置，因为它是 tf.tidy() 的返回值。 

#### tf.memory() 查询内存

```js
console.log(tf.memory());
```

### 运算

​	

### API

 [TensorFlow.js API](https://js.tensorflow.org/api/latest/#Operations) 



### 主成分分析

将数据转换成n个主成分的过程，步骤如下：

1. 去中心化（去除均值）
2. 计算协方差公式
3. 计算协方差矩阵的特征值和特征向量
4. 将特征值从大到小排序
5. 保留最上面的n个特征向量
6. 将数据转换到上述n个特征向量构建的新空间中

