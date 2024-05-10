import pandas as pd
import os


def Coding_index(heu_index):
    # 文件名
    filename = os.path.dirname(os.getcwd()) + r'/output/heuristic{0}.xlsx'.format(heu_index)
    # 读取excel的task
    data_task = pd.read_excel(filename, sheet_name='Sheet1')
    # 用于存储格式化后的总数据
    data_index = str(data_task.values[0, 1]).split(',')
    data_index = list(map(int, data_index))
    return data_index


def Coding_operation(heu_index):
    # 文件名
    filename = os.path.dirname(os.getcwd()) + r'/output/heuristic{0}.xlsx'.format(heu_index)
    # 读取excel的task
    data_task = pd.read_excel(filename, sheet_name='Sheet1')
    # 用于存储格式化后的总数据

    data_operation = str(data_task.values[1, 1]).split(',')
    data_operation = list(map(int, data_operation))
    return data_operation


def Coding_val(heu_index):
    # 文件名
    filename = os.path.dirname(os.getcwd()) + r'/output/heuristic{0}.xlsx'.format(heu_index)
    # 读取excel的task
    data_task = pd.read_excel(filename, sheet_name='Sheet1')
    # 用于存储格式化后的总数据
    data_val = str(data_task.values[2, 1]).split(',')
    data_val = list(map(float, data_val))
    return data_val
