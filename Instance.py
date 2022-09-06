from GP import GP
from Modeling import Problem
from Modeling import Task, Station
import Input_outside
import Plot


def Instance():
    # 用于存储每次运行的关键数据
    output_gp = []
    output_generations = []
    output_data_avg = []
    output_data_best = []
    output_time_cost = []
    # 执行两次，对比复杂度函数影响
    for n in range(2):
        # 是否考虑复杂度参数
        whether_complexity = n
        # 实例化一个gp，n为第几次运行
        gp = GP(number=n)
        # 创建一个存储实例问题的列表
        problems = []
        # 实例化一个任务
        task_list = []
        for t in Input_outside.TASK:
            task_list.append(Task(t[0], t[1], t[2], t[3], t[4]))
        # 实例化一个车间
        station_list = []
        for s in Input_outside.STATION:
            station_list.append(Station(s[0], s[1], s[2]))
        # 将该实例加入problems列表（第三个参数为限定时间）
        problems.append(Problem(task_list, station_list, 100))
        # 执行该问题
        gp.run(problems, whether_complexity)
        # 存储绘图用数据
        output_gp.append(gp)
        output_generations.append(gp.generations)
        output_data_avg.append(gp.data_avg)
        output_data_best.append(gp.data_best)
        output_time_cost.append(gp.time_cost)

    # 绘图对比收敛速度
    Plot.plt_compare(output_gp[0], output_generations[0], output_data_avg[0], output_data_best[0],
                     output_gp[1], output_generations[1], output_data_avg[1], output_data_best[1])

    # 绘图对比计算时间
    Plot.plt_process_time(output_time_cost[0], output_time_cost[1])


