import pandas as pd
import os

# 文件名
filename = os.path.dirname(os.getcwd()) + r'/IPPS-Instance-Generator/Instance.xlsx'

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
    for j in range(data_task.shape[1]):
        # 字符串数据表格化
        if j == 2 or j == 3 or j == 4:
            # 以‘,’为分隔符，将字符串列表化
            lst1 = data_task.values[i, j][1:-1]
            lst2 = str(lst1).split(',')
            # 将列表元素转为int
            lst3 = list(map(int, lst2))
            format_data.append(lst3)
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
    for j in range(data_station.shape[1]):
        # 字符串表格化
        if j == 1:
            # 以‘,’为分隔符，将字符串列表化
            lst1 = data_station.values[i, j][1:-1]
            lst2 = str(lst1).split(',')
            # 将列表元素转为int
            lst3 = list(map(int, lst2))
            format_data.append(lst3)
        # 整型数据正常处理
        else:
            format_data.append(data_station.values[i, j])
    # 插入格式化后的整行数据
    format_datas.append(format_data)
STATION = format_datas
