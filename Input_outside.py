import pandas as pd
import os

# 文件名
filename = os.getcwd() + r'\input01.xlsx'

# 读取excel的task
data_task = pd.read_excel(filename, sheet_name=0)
# 用于存储格式化后的总数据
format_datas = []
# 进行格式化
# 按行遍历
for i in range(data_task.shape[0]):
    # 临时存储格式化后的行数据
    format_data = []
    # 在每行中按列遍历
    for j in range(5):
        # 字符串表格化
        if j == 1 or j == 2:
            # 以‘,’为分隔符，将字符串列表化
            lst1 = str(data_task.values[i, j]).split(',')
            # 将列表元素转为int
            lst2 = list(map(int, lst1))
            format_data.append(lst2)
        # 整型数据正常处理
        else:
            format_data.append(data_task.values[i, j])
    # 插入格式化后的整行数据
    format_datas.append(format_data)
TASK = format_datas

# 读取excel的station
data_station = pd.read_excel(filename, sheet_name=1)
# 用于存储格式化后的总数据
format_datas = []
# 进行格式化
# 按行遍历
for i in range(data_station.shape[0]):
    # 临时存储格式化后的行数据
    format_data = []
    # 在每行中按列遍历
    for j in range(3):
        # 字符串表格化
        if j == 1:
            # 以‘,’为分隔符，将字符串列表化
            lst3 = str(data_station.values[i, j]).split(',')
            # 将列表元素转为int
            lst4 = list(map(int, lst3))
            format_data.append(lst4)
        # 整型数据正常处理
        else:
            format_data.append(data_station.values[i, j])
    # 插入格式化后的整行数据
    format_datas.append(format_data)
STATION = format_datas
