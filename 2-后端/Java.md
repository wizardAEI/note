# 基本概念

## JDK和JRE

![1652365151257](C:\Users\wizard\AppData\Roaming\Typora\typora-user-images\1652365151257.png)



## 别名

```java
int[] a = new int[N];
a[i] = 456;
int[] b = a;
b[i] = 123 //此时a[i]也变成了123。如果你是想将数组复制一份，那么应该声明、创建并初始化一个新的数组，然后将原数组中的元素值挨个复制到新数组。
```

