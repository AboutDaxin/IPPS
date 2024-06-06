from math import ceil
import Dynamic_Evaluate
from Tree import Individual
from logset import logging


# 设置一个常数K，用于后边锦标赛法选择子代
K_CONST = 5
# 最大个体评估次数
MAX_EVALUATIONS = 1
# 最小步长(弃用)
MIN_DELTA = 0.001
# 运行多少次
RUNS = 1


# 定义GP类
class Dynamic_GP:
    # 初始化方法
    def __init__(self, population_size=1, parsimony=0.5):
        # 生成此实例的一个种群
        self.children = None
        self.number = 0
        self.population = []

        # 使用现成heuristic
        logging.info("Using current heuristics")
        if self.number in [0]:
            for _ in range(ceil(population_size)):
                # 实例化个体，使用Tree模块的Individual类
                individual = Individual(parsimony)
                # 使用full方法形成个体，使用Tree模块的full函数
                individual.heuristic(self.number)
                logging.info("Heuristic analysis complete")
                # 在种群列表中增加这个个体，完成整个种群的构建
                self.population.append(individual)

    # 定义实例化方法——问题的适应度评估(GP类)
    def evaluate(self, problems, test_index, generation, solve_task):
        # 对子代中的个体进行遍历
        for individual in self.children:
            # 对每个个体执行核心evaluate(Individual类)方法
            logging.info("Evaluation begin, number of individual is {0}".format(len(self.children)))
            Dynamic_Evaluate.evaluate(individual, problems, test_index, generation, solve_task)

    # 定义实例化方法——运行
    def run(self, problems, solve_task):
        # 执行RUN次循环
        for run in range(RUNS):
            # start_time1 = time.process_time()
            # 设置代数变量
            generation = 0
            # 执行初始化操作
            self.__init__()
            # 因为evaluate方法是针对children属性执行的，所以将population暂时转移了一下
            self.children = self.population
            # 执行适应度评估（GP类）
            print("开始实时调度")
            self.evaluate(problems, 666, generation, solve_task)
            print("结束")
