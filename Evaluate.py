import copy
from Modeling import Job


# 实例化方法——适应度评估（包括两次试验不同的方法）
def evaluate(individual, problems_origin, test_index):
    # 复制源问题
    problems = copy.deepcopy(problems_origin)
    # 用于存储画gantt图用字典的key和value
    draw_key = []
    draw_value = []
    # 定义结束时间
    end_time = 0
    # 第几个算法
    test_index = test_index

    # 遍历problems中的每一项元素，执行评估（目前只有1个problem）
    for problem in problems:
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
        # 计算最大释放时间
        task_release = []
        for i in problem.tasks:
            task_release.append(i.release)
        release_max = max(task_release)
        # 定义结束时间，决定是否使用代理
        # 不使用代理
        if test_index in [1, 2, 3, 4, 5, 6, 7]:
            end_time = 99999
        # 使用代理
        elif test_index in [0]:
            end_time = problem.pcstime * 0.6

        # 评估：遍历每个时刻，执行过程仿真
        true_time = 0
        while not have_finished:
            # 路由规则
            # 首先，遍历所有task，形成可执行task列表
            available_tasks = []
            for group in problem.task_groups:
                # 基于每个组，进行分析
                for task in group.tasks:
                    # 判断本task是否能执行，前序约束是否已满足
                    c = 0
                    for a in task.pre_process_constraint:
                        if a in group.finished_task_index:
                            c += 1
                    if c == len(task.pre_process_constraint):
                        available_tasks.append(task)

            # 之后，遍历所有可用task，进行job分配
            for task in available_tasks:
                # 到达一个判定点（task已到释放时间，还有未执行的工序，任务刚弹出需要重排）
                if task.release <= true_time and task.process_time != [] and task.need_popped is True:
                    # 初始化一个备选station临时存放点
                    stations_temp = []
                    # 基于该task遍历所有station，释放一个job至对应station的job序列
                    for station in stations:
                        # 如果该task的最前道序可以使用该station
                        if task.process_path[0] in station.capability:
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
                                    priority_temp += individual.root.left.interpret(job, station, true_time)
                                # 得到该station的当前优先值
                                station.priority = priority_temp
                            # 如果该station序列中没有任务，则优先值跟num相关
                            else:
                                station.priority = station.station_index/100
                    # 确定被选中的station（优先值最小为最高级别）
                    station_best = min(stations_temp) if stations_temp else print("no!")
                    # 在job序列对应的station中加入一个Job
                    station_best.queue.append(Job(task, station_best, true_time))
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
                        job.priority = individual.root.right.interpret(job, station, true_time)
                    # 随机排列该station的job序列
                    # shuffle(station.queue)
                    # 将该station的job序列按优先级从小到大排序（根据Job的富比较方法）
                    station.queue.sort()
                    # 对station进行能力变更
                    if station.current_capability == 0:
                        # 初始情况
                        station.current_capability = station.queue[0].task.process_path[0] if station.queue else 0
                        station.have_trans = True
                        station.current_trans_time = station.configuration_time
                        total_transtime += station.configuration_time
                    elif station.current_capability == station.queue[0].task.process_path[0] if station.queue else 0:
                        # 不需要转变
                        station.have_trans = False
                        station.current_trans_time = 0
                    else:
                        # 需要转变
                        station.current_capability = station.queue[0].task.process_path[0] if station.queue else 0
                        station.have_trans = True
                        station.current_trans_time = station.configuration_time
                        total_transtime += station.configuration_time
                    # 排序状态变为已排完，不需要重排
                    station.have_popped = True

            # 对每个station的job执行一系列操作
            # 按每个station分别进行判断
            for station in stations:
                # 如果该station还存在job则执行
                if len(station.queue) > 0:
                    # station正在发生转变
                    if station.have_trans and 0 < station.current_trans_time <= station.configuration_time:
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
                        draw_key.append((station.queue[0].task_index, station.queue[0].task.task_string_index,
                                         station.queue[0].task.process_num[0], station.station_index))
                        # 逐步生成draw_value中的元组（开始时间、结束时间、持续时间、转换时间）
                        draw_value.append((true_time + 1 - station.queue[0].task.process_time[0],
                                           true_time + 1, station.queue[0].task.process_time[0],
                                           station.configuration_time if station.have_trans else 0))
                        # 删除该task的当前序工艺类型
                        station.queue[0].task.process_path.pop(0)
                        station.queue[0].task.process_num.pop(0)
                        # 删除该task的当前序执行时间
                        station.queue[0].task.process_time.pop(0)
                        # 该task状态变为需要重排
                        station.queue[0].task.need_popped = True
                        # 该station状态改为未排完，需要重排
                        station.have_popped = False
                        # 如果本task的所有job执行完毕，那么序号加入have_finished列表
                        if not station.queue[0].task.process_num:
                            # task定位
                            coord = [station.queue[0].task.task_index, station.queue[0].task.task_string_index]
                            # 搜索到该task
                            pending_task = problem.task_groups[coord[0]-1].tasks[coord[1]-1]
                            # task的string索引加入已完成列表
                            problem.task_groups[coord[0]-1].finished_task_index.append(pending_task.task_string_index)
                        # 在序列中删除该运行结束的job
                        station.queue.pop(0)
                    # 对当前station的job序列进行遍历，计算拖期
                    if station.queue:
                        for job in station.queue:
                            # 如果遍历出有个job，已经超期，且还没执行完毕
                            if job.task.deadline != 0 and job.task.deadline < true_time and job.process_time > 0:
                                # 如果是非周期任务则拖期参数+1
                                missed_deadlines += 1
            # 判断是否执行完毕
            true_time += 1
            prcs_time_now = process_time
            if prcs_time_now > end_time or (prcs_time_last == prcs_time_now and true_time > release_max):
                makespan = true_time
                have_finished = True
            else:
                prcs_time_last = prcs_time_now

        individual.fitnesses.append(-makespan -
                                    ((makespan*0.01*individual.tree_complexity()) if (test_index in [2, 3, 6, 7]) else 0))
        # 记录个体对本问题的优化目标值（不考虑其他策略影响，当前版本与适应度一致）
        individual.objectives.append(-makespan)
        # 添加各项目标函数值
        individual.total_due_time = missed_deadlines
        individual.total_process_time = process_time
        # 添加绘图辅助参数
        individual.draw_key = draw_key
        individual.draw_value = draw_value
        individual.makespan = makespan
        individual.total_transtime = total_transtime

    # 个体适应度值取列表最后一个
    individual.fitness = individual.fitnesses[-1]
    # 个体目标函数值列表最后一个
    individual.objective = individual.objectives[-1]
