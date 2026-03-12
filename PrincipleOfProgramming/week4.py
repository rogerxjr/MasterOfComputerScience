# numbers = [1, 2, 3, 4, 5]
# doubled_numbers = map(lambda x: x*2, numbers)
# print(doubled_numbers)

#!/usr/bin/python
# from functools import reduce

# def add(x, y) :            # 两数相加
#     return x + y
# sum1 = reduce(add, [1,2,3,4,5])   # 计算列表和：1+2+3+4+5
# sum2 = reduce(lambda x, y: x+y, [1,2,3,4,5])  # 使用 lambda 匿名函数
# print(sum1)
# print(sum2)

def load_logs(): 
    Logs = []
    try:
        with open("logs.txt", "r") as file:
            for line in file:
                Logs.append(line.strip())
    except FileNotFoundError:
        print('logs.txt not found')
    return Logs