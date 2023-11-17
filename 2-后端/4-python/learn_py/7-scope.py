""" 
    内置作用域: Python 预先定义好的变量，如: print, len 
    全局作用域: 函数外的变量，作用域为整个程序
    局部作用域: 函数内的变量
    
    在函数中，局部变量会覆盖全局变量，但不会覆盖内置变量。
"""

# 1. 全局变量
a = 10

# 2. 局部变量
def func():
    b = 20
    print(a, b)
func()

# 3. 局部变量覆盖全局变量
def func2():
    a = 20
    print(a)
func2()

# 修改全局变量, 我们需要使用 global 关键字
def func3():
    global a
    a = 30
    print(a)
func3()