## 类图

### 类图结构

![1643895140432](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/1643895140432.png)

其中`-`号代表私有方法，`+`号代表共有方法，`#`号表示是受保护的只能由子类访问，`~`表示只要在同一个 package 里就可以被访问到，也是默认类型。经常会被用到的就是`+`，`-`号。（注意如果一个类是抽象类，此时的类名可以使用`<<ClassName>>`来注释类型）

### 继承（泛化）

![1643895728223](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/1643895728223.png)

被指的类是父类或者是抽象类

![1643896602275](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/1643896602275.png)

### 关联

![1643896648622](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/1643896648622.png)

关联两个类，在横线上写上其关系

![1643896975002](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/1643896975002.png)

### 聚合

![1643897097942](C:\Users\wizard\AppData\Roaming\Typora\typora-user-images\1643897097942.png)

聚合表明成员对象是整体对象的一部分，他可以单独存在。例如羊群和一只羊。

![1643897814899](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/1643897814899.png)

### 组合

![1643897937452](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/1643897937452.png)

同样是成员对象组成整体对象，但是整体对象控制生命周期。即当整体对象生命周期结束，成员对象生命周期也相应结束。例如房子和卧室。房子崩塌卧室也会崩塌

![1643898409943](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/1643898409943.png)

### 依赖

依赖通常是一种使用关系，并且有依赖使用物品的特征，且除了使用关系外，其他关系并不明显的时候。例如驾驶人和汽车之间的关系

![1643900704187](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/1643900704187.png)
