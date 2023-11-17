# 生命函数的一般形式：
"""
    def func_name([参数列表]) 
        '函数语句'
        return '返回值' 
"""

def hello(name):
    """打印问候语"""
    print(f'hello {name}')

hello('lihua')

"""
    参数类型：1.位置参数 2.默认参数 3.可变参数 4.关键字参数
"""
# 1.位置参数：必须按照顺序传值, 不能为空
def hello2(name, age):
    print(f'hello {name}, your age is {age}')
hello2('lihua', 18) # 打印：hello lihua, your age is 18

# 2.默认参数：可以传值也可以不传值，默认值在函数定义时指定, 注意：默认参数必须放在位置参数后面
def hello3(name, age=18):
    print(f'hello {name}, your age is {age}')
hello3('lihua') # 打印：hello lihua, your age is 18

# 3.可变参数：可传任意个数的参数，在函数定义时使用*args
def hello4(*args):
    print(args)
    print(type(args))
    
hello4('lihua', 18, 'male')

# 4.关键字参数：通过参数名=值的方式传参,
hello3(age=18, name='lihua') # 即使参数顺序不同，也可以通过参数名=值的方式传参

# 5.混合使用：
def hello5(name, age=18, *args, **kwargs):
    print(name, age)
    print(args)
    print(kwargs)
    
hello5('lihua', 18, 'male', qq=123) # 打印：lihua 18 ('male',) {'qq': 123}\    

# **kwargs：可以传任意个数的参数，在函数内部收集成了一个字典，参数名作为字典的键，参数值作为字典的值
def hello6(**kwargs):
    print(kwargs)
    print(type(kwargs))
hello6(name='lihua', age=18, sex='male') # 打印：{'name': 'lihua', 'age': 18, 'sex': 'male'} <class 'dict'>

