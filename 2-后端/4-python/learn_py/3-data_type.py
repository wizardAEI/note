"""
    python的数据类型：
        1. 文本类型：str
        2. 数字类型：int, float, complex（复数）
        3. 序列类型：list, tuple（元组）, range（序列）
        4. 映射类型：dict (字典)
        5. 集合类型：set, frozenset（冻结集合）
        6. 布尔类型：bool
        7. 二进制类型：bytes, bytearray, memoryview (内存视图)
"""

# 使用 type() 函数查看变量的数据类型

# 1. 文本类型：str
# str 类型的变量可以使用单引号或双引号或三引号声明。三引号可以用来声明多行字符串。
a = 'Hello World'
print(a, type(a)) # Hello World <class 'str'>
b = '''Hello World1
    Hello World2
'''
print(b)
# 常用的字符串处理函数： len(string) 获取字符串长度 str() 将其他类型转换为字符串 find() 查找字符串中是否包含指定字符串，如果包含返回索引，否则返回-1
# replace() 替换字符串中的指定字符串 split() 将字符串按指定字符串分割成列表 lower() 将字符串转换为小写 upper() 将字符串转换为大写 strip() 去除字符串两边的空格
# join() 将列表中的字符串按指定字符串连接成一个字符串
print(len(a)) # 11
print('abc'.join('efg')) # eabcfabcg

# 2. 数字类型：int, float, complex（复数）
a = 1
print(a, type(a)) # 1 <class 'int'>
b = 3.1
print(b, type(b)) # 3.1 <class 'float'>
print(a + b, type(a + b)) # 4.1 <class 'float'>
print(b // 2, type(b // 2)) # 1.0 <class 'float'> # //是取整除 (向下取整）

# 3. 序列类型：list, tuple（元组）, range（序列）
# list 常用方法： append() 在列表末尾添加新元素 clear() 清空列表 copy() 复制列表 count() 统计某个元素在列表中出现的次数 extend() 在列表末尾添加新列表
# index() 获取指定元素在列表中的索引 insert() 在指定位置插入新元素 pop() 删除列表中指定索引的元素 remove() 删除列表中指定元素 reverse() 反转列表
a = [1, 2, 3, 'a', 'b', 'c']
a.remove(2)
print(a, type(a)) # [1, 3, 'a', 'b', 'c'] <class 'list'>
b = list()
print(b, type(b)) # [] <class 'list'>
b = (1, 2, 3)
print(b, type(b)) # (1, 2, 3) <class 'tuple'>
c = range(1, 10)
print(c, type(c)) # range(1, 10) <class 'range'>

# 4. 映射类型：dict (字典)
# dict 常用方法： clear() 清空字典 copy() 复制字典 fromkeys() 使用指定的键创建字典 get() 获取指定键的值 items() 获取字典中所有的键值对
# keys() 获取字典中所有的键 pop() 删除指定键的值 popitem() 随机删除一个键值对 setdefault() 获取指定键的值，如果不存在则设置默认值 update() 更新字典的值
# values() 获取字典中所有的值
a = {'name': 'py', 'age': 18}
print(a, type(a)) # {'name': 'py', 'age': 18} <class 'dict'>
print(a.get('name'), a['name']) # py py
a.pop('name', 'default') # 删除指定键的值，如果不存在则返回默认值, 默认值不写则抛出 KeyError 异常

# 5. 集合类型：set, frozenset（冻结集合）
# set 常用方法： add() 向集合中添加元素 clear() 清空集合 copy() 复制集合 
# discard() 删除集合中指定的元素 pop() 随机删除集合中的一个元素 remove() 删除集合中指定的元素
set = {1, 2, 3} # 或者 set = set([1, 2, 3])
print(set, type(set)) # {1, 2, 3} <class 'set'>
set.add(4)
print(set) # {1, 2, 3, 4}

# 6. 布尔类型：bool
a = True
print(a, type(a)) # True <class 'bool'>
# 布尔运算符： and 与 or 或 not 非
print(True and False) # False
print(True or False) # True
print(not 1) # False 0, '', [], {}, (), None 都是 False

# 7. 二进制类型：bytes, bytearray, memoryview (内存视图)
a = b'Hello World'
print(a, type(a)) # b'Hello World' <class 'bytes'>