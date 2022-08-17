import matplotlib.pyplot as plt


def plt_gantt(complete_data):
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
        "size": 10
    }
    fontdict_time = {
        "family": "Microsoft YaHei",
        "style": "oblique",
        "color": "black",
        "size": 10
    }
    color = ['blue', 'green', 'red', 'yellow', 'purple', 'cyan', 'gray']

    # 绘图操作
    for k, v in complete_data.items():
        # 画甘特图
        plt.barh(y=k[2], width=v[2], left=v[0], edgecolor="black", color=color[k[0] % 7])
        # 画标注
        plt.text(v[0] + 0.1, k[2] + 0.15, "Task:\n" + "(" + str(k[0]) + "," + str(k[1]) + ")",
                 fontdict=fontdict_task)
        plt.text(v[0] + 0.1, k[2] - 0.13, "Start:\n " + str(v[0]), fontdict=fontdict_time)
        plt.text(v[0] + 0.1, k[2] - 0.36, "End:\n " + str(v[1]), fontdict=fontdict_time)

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
