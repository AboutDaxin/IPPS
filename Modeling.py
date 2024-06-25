# 定义任务类
class Task:
    # 初始化方法，定义任务层的一些属性
    # 任务索引，工序串索引，串内工艺路径，对应工时，前序约束工序串索引，是否刚性线，到达时间，交货期，权重
    def __init__(self, task_index=0, process_string_index=0, process_path=None,
                 process_time=None, pre_process_constraint=None, whether_rigid=0, release=0, deadline=0, weight=0,
                 have_finished=None, isrunning=None):
        # 固有属性
        if have_finished is None:
            have_finished = [0]
        if isrunning is None:
            isrunning = [0]
        self.task_index = task_index
        self.process_string_index = process_string_index
        self.process_path = process_path
        self.process_time = process_time
        self.pre_process_constraint = pre_process_constraint
        self.whether_rigid = whether_rigid
        self.release = release
        self.deadline = deadline
        self.weight = weight
        self.have_finished = have_finished
        self.isrunning = isrunning
        self.task_string_index = None
        # 衍生属性
        self.process_num = [i + 1 for i in range(len(process_path))]
        self.priority = None
        self.need_popped = True

    # 富比较方法，当实例被用于比较大小时，以priority属性值比较进行代替（lt方法正常用小于号写返还值）
    def __lt__(self, other):
        return self.priority < other.priority


# 定义任务组类
class Task_Group:
    def __init__(self, list_temp, index, finished_task_index, isrunning=None):
        if isrunning is None:
            isrunning = [0]
        self.tasks = list_temp
        self.isrunning = isrunning
        self.index = index + 1
        self.finished_task_index = finished_task_index


# 定义工位类
class Station:
    def __init__(self, station_index=0, capability=None, configuration_time=0, whether_rigid=0, queue_task=None, queue_task_process=None):
        self.station_index = station_index
        self.capability = capability
        self.current_capability = 0
        self.configuration_time = configuration_time
        self.current_trans_time = 0
        self.whether_rigid = whether_rigid
        self.queue_task = queue_task
        self.queue_task_process = queue_task_process
        self.have_trans = False
        self.queue = []
        self.priority = None
        self.have_popped = False

    # 富比较方法，当实例被用于比较大小时，以priority属性值比较进行代替（lt方法正常用小于号写返还值）
    def __lt__(self, other):
        return self.priority < other.priority


# 定义人员类
class Worker:
    def __init__(self, worker_index=0, capability=None):
        self.worker_index = worker_index
        self.capability = capability
        self.priority = None
        self.worktime = 0
        self.using = False

    def __lt__(self, other):
        return self.priority < other.priority


# 定义资源类
class Instrument:
    def __init__(self, instrument_index=0, capability=None):
        self.instrument_index = instrument_index
        self.capability = capability
        self.priority = None
        self.worktime = 0
        self.using = False

    def __lt__(self, other):
        return self.priority < other.priority


# 定义作业类（一个task在station执行时作为一个job）
class Job:
    # 初始化方法，定义作业层的一些属性（Task为声明task的类型）
    def __init__(self, task: Task, station: Station, time):
        # 注意，此处的task为未执行的全部任务，执行过的部分将被删除
        self.task = task
        self.station = station
        self.available_workers = None
        self.available_instrument = None
        self.worker = None
        self.instrument = None
        self.task_index = task.task_index
        # job剩余执行时间
        self.process_time = task.process_time[0] if len(task.process_time) != 0 else 0
        # job释放时间是当前时间
        self.release = time
        self.priority = None
        self.has_run = False

    # 富比较方法
    def __lt__(self, other):
        # 若两个作业优先级相同，自身在运行而另一个没运行，则self排在前边
        if self.priority == other.priority and self.has_run is True and other.has_run is False:
            return True
        # 否则将值小的排前边（lt方法正常使用小于号）
        else:
            return self.priority < other.priority


# 定义问题类
class Problem:
    def __init__(self, tasks, task_groups, stations, workers, instrument, hyper_period=0):
        # 实例化时时，tasks是个列表
        self.tasks = tasks
        self.task_groups = task_groups
        self.stations = stations
        self.workers = workers
        self.instrument = instrument
        self.hyper_period = hyper_period
        # 计算总工时
        self.pcstime = 0
        for i in self.tasks:
            for j in i.process_time:
                self.pcstime += j

