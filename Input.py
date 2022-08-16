from Modeling import Task, Station

# 任务
task_list = [Task(num=1, process=[1, 2, 3], release=0, period=0, deadline=4, exec_time=[2, 5, 1], blk_st=2, blk_dur=2),
             Task(2, [1, 3], 0, 0, 11, [2, 5], 2, 5),
             Task(3, [3, 1], 0, 0, 7, [2, 5], 2, 4),
             Task(4, [2, 3, 2], 0, 0, 6, [2, 5, 3], 2, 1),
             Task(5, [2], 0, 0, 10, [6], 2, 4),
             Task(6, [2, 3], 0, 0, 8, [5, 5], 1, 4),
             Task(7, [1], 0, 0, 4, [5], 2, 2),
             Task(8, [3], 0, 0, 7, [5], 2, 5),
             Task(9, [1, 3], 0, 0, 10, [2, 5], 2, 4),
             Task(10, [3, 2], 0, 0, 6, [2, 5], 2, 1),
             Task(11, [1, 2], 0, 0, 20, [2, 5], 2, 4)]

# 车间
station_list = [
                Station(num=1, capacity=1),
                Station(2, 2),
                Station(3, 2),
                Station(4, 3),
                Station(5, 3)
                ]
