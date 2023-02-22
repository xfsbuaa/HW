import numpy as np
import pandas as pd

# 使用pandas库的read_excel()函数读取Excel文件数据
df = pd.read_excel('data.xlsx')

# 选择需要的列数据，并将其转换为NumPy数组
data = np.column_stack((df['time']))
data = np.column_stack(data)
print(type(data))

#创建一个空列表
result = []
round = []

for i in range(len(data)-1):
    deta_t = data[i+1] - data[i]
    round_num =  60/ deta_t
    round.append(round_num)

print(round)



