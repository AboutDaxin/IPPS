import random
from random import shuffle
import copy
from Modeling import Job
from statistics import mean


# 实例化方法——适应度评估（Individual类的evaluate）（核心）
def evaluate(individual, problems_origin, whether_complexity):
    # 复制源问题
    problems = copy.deepcopy(problems_origin)
    # 用于存储画gantt图用字典的key和value
    draw_key = []
    draw_value = []

    # 遍历problems中的每一项元素，执行评估（目前只有1个problem）
    for problem in problems:
        # hyper_period属性传参
        hyper_period = problem.hyper_period
        # 初始化每个Individual的各项目标函数
        individual.total_process_time = 0
        individual.total_due_time = 0
        # 初始化辅助变量（工时变量）
        process_time = 0
        # 初始化辅助变量（拖期变量）
        missed_deadlines = 0
        # 总转换时间变量
        total_transtime = 0
        # 用于判断是否完成所有任务
        have_finished = False
        makespan = 0
        prcs_time_last = 0
        # 初始化总作业序列列表
        stations = [station for station in problem.stations]

        # 遍历每个时刻，执行过程仿真
        for time in range(hyper_period + 1):
            # 问题处于未完成状态
            if not have_finished:

                # 路由规则
                # 遍历所有task，用于给每个station的job序列加入新Job
                for task in problem.tasks:
                    # 到达一个判定点（task已到释放时间，还有未执行的工序，任务刚弹出需要重排）
                    if task.release <= time and task.process_time != [] and task.need_popped is True:
                        # 初始化一个备选station临时存放点
                        stations_temp = []
                        # 基于该task遍历所有station，释放一个job至对应station的job序列
                        for station in stations:
                            # 如果该task的最前道序可以使用该station
                            if task.process_path[0] in station.capacity:
                                # 生成备选station列表
                                stations_temp.append(station)
                                # 评估确定该station的优先级
                                # 如果该station序列中存在job
                                if station.queue:
                                    # 过渡优先值初始化
                                    priority_temp = 0
                                    # 遍历station中所有job并分别计算优先值
                                    for job in station.queue:
                                        # 临时优先值为所有遍历完job的优先值总和
                                        priority_temp += individual.root.left.interpret(job, station, time)
                                    # 得到该station的当前优先值
                                    station.priority = priority_temp
                                # 如果该station序列中没有任务，则优先值为随机数
                                else:
                                    station.priority = random.random()
                        # 确定被选中的station（优先值最小为最高级别）
                        station_best = min(stations_temp) if stations_temp else print("no!")
                        # 在job序列对应的station中加入一个Job
                        station_best.queue.append(Job(task, station_best, time))
                        # 该station排序状态改为“需要重排”
                        station_best.need_popped = False
                        # 该task状态变为“不需要重排”
                        task.need_popped = False

                # 排序规则
                # 判断是否要执行重排
                for station in stations:
                    # 如果该station需要进行重排
                    if not station.have_popped:
                        # 对该station的job序列执行遍历，重排
                        for job in station.queue:
                            # 计算该job的优先级数值
                            job.priority = individual.root.right.interpret(job, station, time)
                        # 随机排列该station的job序列
                        shuffle(station.queue)
                        # 将该station的job序列按优先级从小到大排序（根据Job的富比较方法）
                        station.queue.sort()
                        # # 对station进行能力变更
                        if station.current_capacity == 0:
                            # 初始情况
                            station.current_capacity = station.queue[0].task.process_path[0] if station.queue else 0
                            station.have_trans = True
                            station.current_trans_time = station.set_time
                            total_transtime += station.set_time
                        elif station.current_capacity == station.queue[0].task.process_path[0] if station.queue else 0:
                            # 不需要转变
                            station.have_trans = False
                            station.current_trans_time = 0
                        else:
                            # 需要转变
                            station.current_capacity = station.queue[0].task.process_path[0] if station.queue else 0
                            station.have_trans = True
                            station.current_trans_time = station.set_time
                            total_transtime += station.set_time
                        # 排序状态变为已排完，不需要重排
                        station.have_popped = True

                # 对每个station的job执行一系列操作
                # 按每个station分别进行判断
                for station in stations:
                    # 如果该station还存在job则执行
                    if len(station.queue) > 0:
                        # station正在发生转变
                        if station.have_trans and 0 < station.current_trans_time <= station.set_time:
                            # 转换消耗时间赋值
                            station.current_trans_time -= 1
                            station.have_trans = True
                        # station已经完成转变
                        else:
                            # 序列中第一个job执行时间-1
                            station.queue[0].process_time -= 1
                        # 总工时+1
                        process_time += 1
                        # 状态改为“正在运行”
                        station.queue[0].has_run = True

                        # 如果当前job执行完毕
                        if station.queue[0].process_time <= 0:
                            # 逐步生成draw_key中的元组(任务序号、工序序号、工作站序号)
                            draw_key.append((station.queue[0].task_index, station.queue[0].task.process_num[0], station.task_index))
                            # 逐步生成draw_value中的元组（开始时间、结束时间、持续时间、转换时间）
                            draw_value.append((time + 1 - station.queue[0].task.process_time[0],
                                               time + 1, station.queue[0].task.process_time[0],
                                               station.set_time if station.have_trans else 0))
                            # 删除该task的当前序工艺类型
                            station.queue[0].task.process_path.pop(0)
                            station.queue[0].task.process_num.pop(0)
                            # 删除该task的当前序执行时间
                            station.queue[0].task.process_time.pop(0)
                            # 该task状态变为刚弹出
                            station.queue[0].task.need_popped = True
                            # 状态改为未排完，需要重排
                            station.have_popped = False
                            # 在序列中删除该运行结束的job
                            station.queue.pop(0)

                        # 对当前station的job序列进行遍历，计算拖期
                        for job in station.queue:
                            # 如果遍历出有个job，已经超期，且还没执行完毕
                            if job.task.deadline != 0 and job.task.deadline < time and job.process_time > 0:
                                # 如果是非周期任务则零星拖期参数+1
                                missed_deadlines += 1
                # 判断是否执行完毕
                prcs_time_now = process_time
                if prcs_time_last == prcs_time_now:
                    makespan = time
                    have_finished = True
                else:
                    prcs_time_last = prcs_time_now

        # 添加个体对本问题的适应度值
        individual.fitnesses.append(
            (-missed_deadlines - process_time - makespan)/3
            - ((missed_deadlines + process_time + makespan)/3 * 0.02 * individual.tree_complexity()
               if whether_complexity == 0 else 0))
        # 添加个体对本问题的优化目标值（不考虑复杂度函数影响）
        individual.objectives.append((-missed_deadlines - process_time - makespan)/3)
        # 添加各项目标函数值
        individual.total_due_time = missed_deadlines
        individual.total_process_time = process_time
        # 添加绘图辅助参数
        individual.draw_key = draw_key
        individual.draw_value = draw_value
        individual.makespan = makespan
        individual.total_transtime = total_transtime

    # 个体适应度值取列表平均数（目前只有一个）
    individual.fitness = mean(individual.fitnesses)
    # 个体目标函数值列表平均数（目前只有一个）
    individual.objective = mean(individual.objectives)
