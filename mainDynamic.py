from Dynamic_instance import Dynamic_instance
import logging

logging.basicConfig(level=logging.DEBUG)

# 需要进行实时调度的任务号
logging.info("Begin")
task_index = 9
logging.info("Task index is "+str(task_index))
Dynamic_instance(task_index)
