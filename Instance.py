from GP import GP
from Modeling import Problem
from Modeling import Task, Station
import Input


def Instance():
    # 实例化一个gp
    gp = GP()
    # 创建一个存储实例问题的列表
    problems = []
    # 实例化一个任务
    task_list = []
    for t in Input.TASK:
        task_list.append(Task(t[0], t[1], t[2], t[3], t[4], t[5], t[6]))
    # 实例化一个车间
    station_list = []
    for s in Input.STATION:
        station_list.append(Station(s[0], s[1], s[2]))
    # 将该实例加入problems列表
    problems.append(Problem(task_list, station_list, 100))
    # 执行该问题
    gp.run(problems)
