import pandas as pd
import os

# 文件名
filename = os.path.dirname(os.getcwd()) + r'/realtime data/realtime data.xlsx'

# 读取excel的数据
data_realtime = pd.read_excel(filename, sheet_name=0)
# 用于存储格式化后的总数据
format_datas = []

# 进行格式化
# 按行遍历
for i in range(data_realtime.shape[0]):
    # 临时存储格式化后的行数据
    format_data = []
    # 在每行中按列遍历
    for j in range(data_realtime.shape[1]):
        # 字符串数据表格化
        if j == 3 or j == 4 or j == 5 or j == 6 or j == 7:
            # 以‘,’为分隔符，将字符串列表化
            lst1 = data_realtime.values[i, j][1:-1]
            lst2 = str(lst1).split(',')
            # 将列表元素转为int
            lst3 = list(map(int, lst2))
            format_data.append(lst3)
        # 整型数据正常处理
        else:
            format_data.append(data_realtime.values[i, j])
    # 插入格式化后的整行数据
    format_datas.append(format_data)
RealtimeData = format_datas
