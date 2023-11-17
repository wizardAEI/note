# 1. if else
score = int(input("Enter your score: "))

if score >= 90:
    print("Your grade is A")
elif score >= 80:
    print("Your grade is B")
elif score >= 70:
    print("Your grade is C")
elif score >= 60:
    print("Your grade is D")
else:   
    print("Your grade is F")
    
# 2. for loop
for i in range(5):
    print(i)
# for loop with range 有时候我们需要使用range来快速生成一个可循环的对象。 range(start,end[,step])，其中start为起始值，end为结束值，step为步长，默认为1。
for i in range(5, 10):
    print(i)
dict1 = {
    'a': 'apple',
    'b': 'banana',
}
for key in dict1:
    print(key, dict1[key])

# 3. while loop
i = 0
while i < 5:
    print(i)
    if i == 3:
        break
    i += 1
    
