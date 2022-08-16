from GP import GP
from Modeling import Problem
import Input


def Instance():
    # 实例化一个gp
    gp = GP()
    # 创建一个存储实例问题的列表
    problems = []
    # 实例化一个任务
    task_list = Input.task_list
    # 实例化一个车间
    station_list = Input.station_list
    # 将该实例加入problems列表
    problems.append(Problem(task_list, station_list, 100))
    # 执行该问题
    gp.run(problems)
