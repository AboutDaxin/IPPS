import copy
from Modeling import Job
from logset import logging


# 实例化方法——适应度评估（包括两次试验不同的方法）
def evaluate(individual, problems_origin, test_index, generation, solve_task):
    global task
    # 复制源问题
    problems = copy.deepcopy(problems_origin)
    # 第几个算法?
    test_index = test_index
    # 识别代数
    generation = generation

    # 遍历problems中的每一项元素，执行评估（目前只有1个problem）
    for problem in problems:
        # 初始化每个Individual的各项目标函数
        individual.total_process_time = 0
        individual.total_due_time = 0
        # 总转换时间变量
        total_transtime = 0
        # 用于判断是否完成所有任务
        have_finished = False
        # 初始化总作业序列列表
        stations = [station for station in problem.stations]
        # 计算最大释放时间
        task_release = []
        for i in problem.tasks:
            task_release.append(i.release)
        # 定义结束时间，决定是否使用代理
        # 不使用代理
        logging.info("Surrogate not used")
        if test_index in [666]:
            pass
        else:
            print("no test index! ", generation, test_index)

        # 执行过程仿真
        true_time = 0
        while not have_finished:
            # 路由规则
            # 首先，遍历所有task，形成可执行task列表
            temp_available_tasks = []
            available_tasks = []
            group = problem.task_groups[solve_task-1]
            # 先转换一下finished_task_index格式
            logging.info("Finished tasks data reading...")
            finished = [0]
            n = 1
            for i in group.finished_task_index:
                if i == 1:
                    finished.append(n)
                    n += 1
            group.finished_task_index = finished
            # 确认可选任务工序
            logging.info("Identify available processes...")
            for task in group.tasks:
                # 判断本task是否能执行，是否是未完成工序
                if task.have_finished == 0:
                    temp_available_tasks.append(task)
            for task in temp_available_tasks:
                # 判断本task是否能执行，前序约束是否已满足
                c = 0
                for a in task.pre_process_constraint:
                    if a in group.finished_task_index:
                        c += 1
                if c == len(task.pre_process_constraint):
                    available_tasks.append(task)
            # 读取可选任务索引
            available_tasks_index = [[i.task_index, i.task_string_index] for i in available_tasks]
            logging.info("Available processes are " + str(available_tasks_index))

            # 把输入表queue里的内容JOB化加入station里
            logging.info("Current jobs sequencing data reading...")
            for station in problem.stations:
                if station.queue_task:
                    # 获取station当前正在进行的任务并删除
                    logging.info("Current job of station{0} is: task{1}".format(station.station_index, station.queue_task[0]))
                    station.queue_task.pop(0)
                    station.queue_task_process.pop(0)
                    for i in range(len(station.queue_task)):
                        temp_task_index1 = station.queue_task[i]
                        temp_task_index2 = station.queue_task_process[i]
                        station_task = problem.task_groups[temp_task_index1-1].tasks[temp_task_index2-1]
                        station.queue.append(Job(station_task, station, true_time))
                    # 获取station当前能力
                    station.current_capability = station.queue[0].task.process_path[0]
                    logging.info("Current capability of station{0} is: {1}".format(station.station_index, station.current_capability))

            # 之后，遍历所有可用task，进行job分配
            logging.info("Identify available stations...")
            if available_tasks:
                stations_best = []
                for task in available_tasks:
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
                    stations_best.append(min(stations_temp)) if stations_temp else print("no!")
                # 识别最优可用单元
                available_stations_index = [[i.station_index] for i in stations_best]
                logging.info("Available stations are " + str(available_stations_index))

                # 在job决定选择的station中加入该Job
                temp_task_index3 = [i for i, x in enumerate(stations_best) if x == min(stations_best)]
                final_task = available_tasks[temp_task_index3[0]]
                station_best = min(stations_best)
                print("建议分配任务{0}的工序{1}至单元{2}。".format(final_task.task_index, final_task.process_string_index, station_best.station_index))
                logging.info("Task{0} process{1} to station{2}".format(final_task.task_index, final_task.process_string_index, station_best.station_index))
                # 加入该job
                station_best.queue.append(Job(final_task, station_best, true_time))
                # 该station排序状态改为“需要重排”
                station_best.need_popped = False
                # 该task状态变为“不需要重排”
                final_task.need_popped = False

                # # 排序规则
                station = station_best
                # 对该station的job序列执行遍历，重排
                for job in station.queue:
                    # 计算该job的优先级数值
                    job.priority = individual.root.right.interpret(job, station, true_time)
                # 随机排列该station的job序列
                # shuffle(station.queue)
                # 将该station的job序列按优先级从小到大排序（根据Job的富比较方法）
                station.queue.sort()
                print("建议单元{0}上的任务排序如下：".format(station.station_index))
                logging.info("Sequencing in station{0} is: ".format(station.station_index))
                for i in range(len(station.queue)):
                    print(str(i+1) + " :任务{}的工序{}。".format(station.queue[i].task.task_index, station.queue[i].task.task_string_index))
                    logging.info(str(i+1) + ":Task{} process{}".format(station.queue[i].task.task_index, station.queue[i].task.task_string_index))
                # 对station进行能力变更
                if station.current_capability == 0:
                    # 初始情况
                    station.current_capability = station.queue[0].task.process_path[0] if station.queue else 0
                    station.have_trans = True
                    station.current_trans_time = station.configuration_time
                    total_transtime += station.configuration_time
                    print("单元能力需要转换，消耗{0}小时。".format(station.configuration_time))
                    logging.info("Capability reconfiguration time is {0}".format(station.configuration_time))
                elif station.current_capability == station.queue[0].task.process_path[0] if station.queue else 0:
                    # 不需要转变
                    station.have_trans = False
                    station.current_trans_time = 0
                    print("单元能力不需要转换。")
                    logging.info("No need to reconfiguration")
                else:
                    # 需要转变
                    station.current_capability = station.queue[0].task.process_path[0] if station.queue else 0
                    station.have_trans = True
                    station.current_trans_time = station.configuration_time
                    total_transtime += station.configuration_time
                    print("单元能力需要转换，消耗{0}小时。".format(station.configuration_time))
                    logging.info("Capability reconfiguration time is {0}".format(station.configuration_time))
                # 排序状态变为已排完，不需要重排
                station.have_popped = True
                have_finished = True
            else:
                print("任务{}已完成所有工序。".format(task.task_index))
                logging.warning("Task{} has done".format(task.task_index))
                have_finished = True
