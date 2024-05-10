import matplotlib.pyplot as plt
from statistics import mean
import os
import pandas as pd
import copy


# 生成gantt图
def plt_gantt(best, number):
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
        "size": 12
    }
    fontdict_time = {
        "family": "Microsoft YaHei",
        "style": "oblique",
        "color": "black",
        "size": 12
    }
    color = ['blue', 'green', 'red', 'yellow', 'purple', 'cyan', 'gray']

    # 提取数据
    complete_data = dict(zip(best.draw_key, best.draw_value))
    # 绘图操作
    plt.figure('A{0} Gantt'.format(number+1), (26, 12))
    for k, v in complete_data.items():
        # 画job甘特图
        plt.barh(y=k[3], width=v[2], left=v[0], edgecolor="black", color=color[k[0] % 7])
        # 画job标注
        # plt.text(v[0] + 0.1, k[2]-0.14, "Task:\n" + "(" + str(k[0]) + "," + str(k[1]) + ")",
        #          fontdict=fontdict_task)
        # plt.text(v[0] + 0.5, k[2], "Start:\n " + str(v[0]), fontdict=fontdict_time)
        # plt.text(v[0] + 0.5, k[2] - 0.35, "End:\n " + str(v[1]), fontdict=fontdict_time)
        plt.text(v[0], k[3]-0.33, "Task:\n" + "(" + str(k[0]) + "," + str(k[1]) + "," + str(k[2]) + ")",
                 fontdict=fontdict_task)

        # 画transtime甘特图
        plt.barh(y=k[3], width=v[3], left=v[0]-v[3], edgecolor="black", color='black', alpha=0.1)
        # 画transtime标注
        plt.text(v[0]-v[3], k[3]-0.33, "Time:\n " + str(v[3]) if v[3] != 0 else '', fontdict=fontdict_time)

    # 生成x轴刻度
    plt.xticks(range(best.makespan+2))
    # 生成y轴label
    ylabels = []
    m = []
    for i in complete_data:
        m.append(i[3])
    for i in range(max(m)):
        ylabels.append("Station" + str(i + 1))
    plt.yticks(range(1, max(m)+1), ylabels, rotation=45)
    # 生成title
    plt.title("A{0} Gantt".format(number+1))
    plt.xlabel("process_time /h")
    plt.ylabel("stations")


# 生成平均目标比较图
def plt_compare1(test_number, generations, data_avg):
    plt.figure('Average_Objective')
    temp_data_avg = []
    x0 = 0
    for n in range(test_number):
        generations0 = generations[n]
        data_avg0 = data_avg[n]
        # map：映射，让data中的元素依次使用mean方法执行，返还值生成一个列表
        # 此处将data_avg中的每一个列表取平均值(run次)，生成一个新列表
        data_avg0 = [i for i in map(mean, data_avg0)]
        # 取相反数，绘图用
        data_avg0 = [-i for i in data_avg0]
        temp_data_avg.append(data_avg0)
        # 生成画图x轴
        x0 = range(0, generations0)
        # 输出代数与平均值和最优值的图像，横轴为评估次数，纵轴为适应度
        plt.plot(x0, data_avg0, label='A{0}'.format(n+1))
    plt.legend(fontsize=12)
    plt.xlabel('Generations', fontsize=12)
    plt.ylabel('Objectives', fontsize=12)
    # 输出时间进化数据表格
    # df = pd.DataFrame({"generations": x0,
    #                    "A1": temp_data_avg[0], "A2": temp_data_avg[1],
    #                    "A3": temp_data_avg[2], "A4": temp_data_avg[3],
    #                    "A5": temp_data_avg[4]})
    # df = df.set_index('generations')
    # df.to_excel(os.path.dirname(os.getcwd()) + '\\IPPS_output_file\\Avg process.xlsx')


# 生成最优目标比较图
def plt_compare2(test_number, generations, data_best):
    plt.figure('Best_Objective')
    temp_data_best = []
    x0 = 0
    for n in range(test_number):
        generations0 = generations[n]
        data_best0 = data_best[n]
        # map：映射，让data中的元素依次使用mean方法执行，返还值生成一个列表
        # 此处将data_avg中的每一个列表取平均值(run次)，生成一个新列表
        data_best0 = [i for i in map(mean, data_best0)]
        # 取相反数，绘图用
        data_best0 = [-i for i in data_best0]
        temp_data_best.append(data_best0)
        # 生成画图x轴
        x0 = range(0, generations0)
        # 输出代数与平均值和最优值的图像，横轴为评估次数，纵轴为适应度
        plt.plot(x0, data_best0, label='A{0}'.format(n+1))
    plt.legend(fontsize=12)
    plt.xlabel('Generations', fontsize=12)
    plt.ylabel('Objectives', fontsize=12)
    # 输出时间进化数据表格
    # df = pd.DataFrame({"generations": x0,
    #                    "A1": temp_data_best[0], "A2": temp_data_best[1],
    #                    "A3": temp_data_best[2], "A4": temp_data_best[3],
    #                    "A5": temp_data_best[4]})
    # df = df.set_index('generations')
    # df.to_excel(os.path.dirname(os.getcwd()) + '\\IPPS_output_file\\Best process.xlsx')


# 生成演化时间比较图
def plt_compare3(test_number, generations, data_time):
    plt.figure('time cost comparison ')
    temp_data_time = []
    x0 = 0
    for n in range(test_number):
        generations0 = generations[n]
        data_time0 = data_time[n]
        data_time0 = [i for i in map(mean, data_time0)]
        # 去掉第一个元素，0
        temp_data_time0 = copy.deepcopy(data_time0)
        temp_data_time0.pop(0)
        temp_data_time.append(temp_data_time0)
        # x轴
        x0 = range(1, generations0)
        # 绘图
        plt.plot(x0, temp_data_time0, label='A{0}'.format(n+1))
    plt.legend(fontsize=12)
    plt.xlabel('Generations', fontsize=12)
    plt.ylabel('Time', fontsize=12)
    # 输出时间进化数据表格
    # df = pd.DataFrame({"generations": x0,
    #                    "A1": temp_data_time[0], "A2": temp_data_time[1],
    #                    "A3": temp_data_time[2], "A4": temp_data_time[3],
    #                    "A5": temp_data_time[4]})
    # df = df.set_index('generations')
    # df.to_excel(os.path.dirname(os.getcwd()) + '\\IPPS_output_file\\Time process.xlsx')


# 生成运算时间比较图
def plt_process_time(test_number, time):
    plt.figure('time_cost')
    for n in range(test_number):
        time0 = time[n]
        plt.bar(n+1, time0, width=0.3, edgecolor='white')
        plt.text(n+1, time0+0.05, '%.5f' % time0, ha='center', va='bottom')
        # x刻度赋值
        key = [i+1 for i in range(test_number)]
        value = ['A{0}'.format(i+1) for i in range(test_number)]
        plt.xticks(key, value)


# 生成提琴图
def plt_violin(test_number, data_avg, data_best):
    plt.figure('Violin_Objective', (7, 7))
    data_avg_total = []
    data_best_total = []
    for n in range(test_number):
        data_avg0 = data_avg[n][-1]
        data_best0 = data_best[n][-1]
        # 取相反数，绘图用
        data_avg0 = [-i for i in data_avg0]
        data_best0 = [-i for i in data_best0]
        data_avg_total.append(data_avg0)
        data_best_total.append(data_best0)

    # 绘图
    plt.subplot(2, 1, 1)
    plt.violinplot(data_avg_total, showmeans=True, showmedians=True)
    key = [i + 1 for i in range(test_number)]
    value = ['A{0}'.format(i + 1) for i in range(test_number)]
    plt.xticks(key, value)
    plt.xlabel('Algorithm', fontsize=12)
    plt.ylabel('Average value', fontsize=12)
    plt.subplot(2, 1, 2)
    plt.violinplot(data_best_total, showmeans=True, showmedians=True)
    key = [i + 1 for i in range(test_number)]
    value = ['A{0}'.format(i + 1) for i in range(test_number)]
    plt.xticks(key, value)
    plt.xlabel('Algorithm', fontsize=12)
    plt.ylabel('Best value', fontsize=12)

    plt.show()
