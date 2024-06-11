from Dynamic_instance import Dynamic_instance
from logset import logging

# 需要进行实时调度的任务号
logging.info("==================Begin===================")
task_index = 2
logging.info("Task index is "+str(task_index))
Dynamic_instance(task_index)
