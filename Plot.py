import matplotlib.pyplot as plt
from statistics import mean
import numpy as np


def plt_evolve(GP, generations, data_avg, data_best):
    # map：映射，让data中的元素依次使用mean方法执行，返还值生成一个列表
    # 此处将data_avg中的每一个列表取平均值，生成一个新列表(还是共52个元素)
    data_avg = [i for i in map(mean, data_avg)]
    # 同上
    data_best = [i for i in map(mean, data_best)]
    # 生成画图x轴，从1000到2040（不含），间隔20。实际为1000-2020，共51段
    x = np.arange(GP.population_size, GP.population_size + GP.children_size * generations, GP.children_size)
    # 输出代数与平均值和最优值的图像，横轴为评估次数，纵轴为适应度
    plt.figure(1)
    plt.plot(x, data_avg, x, data_best)
    plt.xlabel('Evaluations')
    plt.ylabel('Fitness')


def plt_gantt(best):
    # 文字格式初始化
    # 使用中文文字
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # 定义两个格式字典
    fontdict_task = {
        "family": "Microsoft YaHei",
        "style": "oblique",
        "weight": "bold",
        "color": "black",
        "size": 8
    }
    fontdict_time = {
        "family": "Microsoft YaHei",
        "style": "oblique",
        "color": "black",
        "size": 8
    }
    color = ['blue', 'green', 'red', 'yellow', 'purple', 'cyan', 'gray']

    # 提取数据
    complete_data = dict(zip(best.draw_key, best.draw_value))
    # 绘图操作
    plt.figure(2, (26, 12))
    for k, v in complete_data.items():
        # 画job甘特图
        plt.barh(y=k[2], width=v[2], left=v[0], edgecolor="black", color=color[k[0] % 7])
        # 画job标注
        plt.text(v[0] + 0.1, k[2] + 0.15, "Task:\n" + "(" + str(k[0]) + "," + str(k[1]) + ")",
                 fontdict=fontdict_task)
        plt.text(v[0] + 0.1, k[2] - 0.13, "Start:\n " + str(v[0]), fontdict=fontdict_time)
        plt.text(v[0] + 0.1, k[2] - 0.36, "End:\n " + str(v[1]), fontdict=fontdict_time)

        # 画transtime甘特图
        plt.barh(y=k[2], width=v[3], left=v[0]-v[3], edgecolor="black", color='black', alpha=0.1)
        # 画transtime标注
        plt.text(v[0]-v[3] + 0.1, k[2], "Set-time:\n " + str(v[3]) if v[3] != 0 else '', fontdict=fontdict_time)

    # 生成y轴label
    ylabels = []
    m = []
    for i in complete_data:
        m.append(i[2])
    for i in range(max(m)):
        ylabels.append("制造单元" + str(i + 1))

    plt.yticks(range(1, max(m)+1), ylabels, rotation=45)
    plt.title("排产方案-甘特图")
    plt.xlabel("加工时间 /h")
    plt.ylabel("工作站")

    plt.show()
