from Dynamic_GP import Dynamic_GP
from Modeling import Problem
from Modeling import Task, Task_Group, Station
import Dynamic_realtime_input


def Dynamic_instance(solve):
    # 对比试验组数设定
    test_number = 1
    # 执行n次，对比复杂度函数影响
    for n in range(test_number):
        print('==== ALGORITHM {} ===='.format(n))
        # 是否考虑复杂度参数(是0考虑，是1不考虑)
        test_index = n
        # 创建一个存储实例问题的列表
        problems = []

        # 实例化一个任务
        task_list = []
        task_group_list = []
        for t in Dynamic_realtime_input.TASK:
            task_list.append(Task(t[0], t[1], t[2], t[3], t[4], t[5], t[6], t[7], t[8], t[9]))
        # 任务预处理，形成一个分层级的任务列表
        max_index = task_list[-1].task_index
        # 分的总组数，因为task_index就是总一级任务数
        for j in range(max_index):
            # 用于存储组内的所有工序串
            list_temp = []
            # 用于存储该组内已完工的工序串
            finished_task_index = []
            # 定义组内的工序串索引
            index = 1
            # i是全局的每个工序串
            for i in task_list:
                # 遍历索引判断，i的索引符合本组（j）就赋值
                if i.task_index == j + 1:
                    # 工序串的组内索引赋值
                    i.task_string_index = index
                    list_temp.append(i)
                    index += 1
                    finished_task_index.append(i.have_finished)
            # 实例化一个task group
            task_group_list.append(Task_Group(list_temp, j, finished_task_index))

        # 实例化一个车间
        station_list = []
        for s in Dynamic_realtime_input.STATION:
            station_list.append(Station(s[0], s[1], s[2], s[3], s[4], s[5]))
        # 将该实例加入problems列表（第三个参数为限定时间）
        problems.append(Problem(task_list, task_group_list, station_list, 99999))
        # 实例化一个gp
        gp = Dynamic_GP()
        # 执行该问题
        gp.run(problems, solve)
