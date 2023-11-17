"""
    print函数的参数意义：
    sep：分隔符，默认是空格
    end：结束符，默认是换行符
"""

print('hello', 'world', sep=',', end='!')

print('hello', 'world', sep='\n', end='!')

# 占位符
# %s 字符串占位符 %d 整数占位符 %f 浮点数占位符 %x 十六进制整数占位符 %e 指数型浮点数占位符 %c 字符占位符 %nf 浮点数占位符，n代表浮点数的位数，默认保留6位小数
print('Hello %s' % 'py') # Hello py

# 格式化字符串
# 使用 format() 函数格式化字符串
print('Hello {}'.format('py')) # Hello py
print('Hello {2}{1}{0}'.format('py0','py1', 'py2')) # Hello py2py1py0
a = '3'
print(f'12{3}') # 123

# 使用 f-string 格式化字符串 (python 3.6+)
name = 'py'
print(f'Hello {name}') # Hello py

"""
    input函数的参数意义：
    prompt：提示信息
"""

num = input('请输入一个数字：')

print(num)