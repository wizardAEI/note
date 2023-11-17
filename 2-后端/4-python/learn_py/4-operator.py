# is, is not 运算符，比较两个对象的内存地址是否相等

# 对于简单的数据类型，比如整数，Python会对其进行缓存，所以内存地址相同 (但是不要依赖这个特性，因为这个特性在不同的Python解释器中可能不同)
a = 5
b = 5
print(a is b)  # 输出：True

# 对于复杂的数据类型
list1 = [1, 2,3]
list2 = [1, 2, 3]
print(list1 is list2)  # 输出：False

# 对于同一个对象的引用
list3 = list1
print(list1 is list3)  # 输出：True
