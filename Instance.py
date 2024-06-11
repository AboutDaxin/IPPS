from GP import GP
from Modeling import Problem
from Modeling import Task, Task_Group, Station
import Input_outside
# import Plot


def Instance():
    # 用于存储两次对比运行的关键数据
    # output_gp = []
    output_generations = []
    output_data_avg = []
    output_data_best = []
    output_data_time = []
    output_time_cost = []
    # 对比试验组数设定
    test_number = 1
    # 执行两次，对比复杂度函数影响
    for n in range(test_number):
        print('==== ALGORITHM {} ===='.format(n))
        # 是否考虑复杂度参数(是0考虑，是1不考虑)
        test_index = n
        # 创建一个存储实例问题的列表
        problems = []
        # 实例化一个任务
        task_list = []
        task_group_list = []
        for t in Input_outside.TASK:
            task_list.append(Task(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8]))

        # 任务预处理，形成一个分层级的任务列表
        max_index = task_list[-1].task_index
        for j in range(max_index):
            list_temp = []
            index = 1
            for i in task_list:
                # 索引判断分组
                if i.task_index == j + 1:
                    # 工序串索引赋值
                    i.task_string_index = index
                    list_temp.append(i)
                    index += 1
            # 实例化一个task group
            task_group_list.append(Task_Group(list_temp, j, [0]))

        # 实例化一个车间
        station_list = []
        for s in Input_outside.STATION:
            station_list.append(Station(s[0], s[1], s[2]))
        # 将该实例加入problems列表（第三个参数为限定时间）
        problems.append(Problem(task_list, task_group_list, station_list, 99999))
        # 实例化一个gp，n为第几次运行
        gp = GP(number=n)
        # 执行该问题
        gp.run(problems, test_index)
        # 存储绘图用数据
        # output_gp.append(gp)
        output_generations.append(gp.generations)
        output_data_avg.append(gp.data_avg)
        output_data_best.append(gp.data_best)
        output_data_time.append(gp.data_time)
        output_time_cost.append(gp.time_cost)

    # # 绘图对比收敛速度
    # Plot.plt_compare1(test_number, output_generations, output_data_avg)
    # Plot.plt_compare2(test_number, output_generations, output_data_best)
    # Plot.plt_compare3(test_number, output_generations, output_data_time)
    #
    # # 绘图对比计算时间
    # Plot.plt_process_time(test_number, output_time_cost)
    #
    # # 绘图10次独立运行的优化目标提琴图
    # Plot.plt_violin(test_number, output_data_avg, output_data_best)
