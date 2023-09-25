from random import sample, random, randrange
from copy import deepcopy
from statistics import mean
from math import floor, ceil
import Evaluate
from Tree import Individual
import Plot
import time
import pandas as pd
import os


# 设置一个常数K，用于后边锦标赛法选择子代
K_CONST = 5
# 最大个体评估次数（共26代，3100个个体，不包含初代500个）
MAX_EVALUATIONS = 200
# 最小步长(弃用)
MIN_DELTA = 0.001
# 运行多少次
RUNS = 1


# 定义GP类
class GP:
    # 初始化方法：在GP类进行实例化时执行。参数为：种群规模500，子代规模100，变异率0.1，复制率为0.05，简化参数0.5
    def __init__(self, number, population_size=50, children_size=50, mutation=0.15, duplication=0.05, parsimony=0.5):
        # 生成此实例的一个种群
        # 类属性：定义实例的种群(population)为一个列表
        self.number = number
        self.population = []
        # 传参用
        self.generations = None
        self.data_avg = None
        self.data_best = None
        self.data_time = None
        self.data_complexity = None
        self.time_cost = None

        # grow方法生成半个种群
        # 设置一个用于生成种群的循环，为种群规模的一半，floor表示向下取整
        for _ in range(floor(population_size/2)):
            # 实例化个体，使用Tree模块的Individual类
            individual = Individual(parsimony)
            # 使用grow方法形成个体，使用Tree模块的grow函数
            individual.grow(4)
            # 在种群列表中增加这个个体
            self.population.append(individual)

        # full方法生成剩下半个种群，并结合起来
        # 设置一个用于生成种群的循环，为种群规模的一半，ceil表示向上取整
        for _ in range(ceil(population_size/2)):
            # 实例化个体，使用Tree模块的Individual类
            individual = Individual(parsimony)
            # 使用full方法形成个体，使用Tree模块的full函数
            individual.full(4)
            # 在种群列表中增加这个个体，完成整个种群的构建
            self.population.append(individual)

        # 设置此实例的一些初始化变量
        # “父”，“子”为空列表
        # 评估次数初始值为0，简化参数为预设的0.5
        self.parents = []
        self.population_size = population_size
        self.children = []
        self.children_size = children_size
        self.mutation = mutation
        self.duplication = duplication
        self.evaluations = 0
        self.parsimony = parsimony

    # 定义实例化方法——筛选父代
    def parentSelection(self):
        # K-tournament法（锦标赛选择）
        # 设置实例的parents方法为一个空列表
        self.parents = []
        # 执行一个筛选父代的循环，次数为要产生的子代的规模为**
        for _ in range(self.children_size):
            # 在parents列表中增加个体
            # 使用了random模块的sample方法，K_CONST是片段长度，前边设置为常数10
            # sample方法：在整个列表（population）中随机取一个固定（10）长度的片段，并随机排列
            # 此处选择任意片段中的最大值加入parents，实现锦标赛选择法
            self.parents.append(max(sample(self.population, K_CONST)))

    # 定义实例化方法——生成子代
    def childGeneration(self):
        # 设置实例的children属性为一个空列表
        self.children = []
        # 执行一个生成子代的循环，次数为要产生的子代的规模，用于逐个判断是否要进行变异
        for i in range(self.children_size):
            temprandom = random()
            # 变异：生成一个随机数，小于变异概率0.05就执行下列变异操作
            if temprandom < self.mutation:
                # 实例化一个随机树，使用Tree模块的Individual类
                random_tree = Individual(self.parsimony)
                # 使用Tree模块的root.grow方法
                random_tree.root.grow(2)
                # 设置一个parent_copy，将parentSelection方法中生成好的self.parents的第i个个体取出
                parent_copy = deepcopy(self.parents[i])
                # 设置取出的个体的stats属性为一个空列表
                parent_copy.stats = []
                # 选择节点进行替换
                parent_copy.root.choose_node(True, random_tree.root)
                # 在children列表里添加该个体
                self.children.append(parent_copy)
            # 执行复制操作
            elif self.mutation <= temprandom < self.duplication + self.mutation:
                parent_copy = deepcopy(self.parents[i])
                self.children.append(parent_copy)
            # 执行交叉操作
            else:
                # TTGP
                if self.number == 0 or 2:
                    # 让第i个个体跟一个个体进行交叉
                    parent_copy = deepcopy(self.parents[i]).recombine(self.parents[randrange(0, self.children_size, 1)])
                    # 设置取出个体的stats属性是一个空列表
                    parent_copy.stats = []
                    # 在children列表中添加该个体
                    self.children.append(parent_copy)
                # CCGP
                elif self.number == 1 or 3:
                    # 让第i个个体左右分别跟随机一个进行交叉
                    parent_copy = deepcopy(self.parents[i]).left_recombine(
                        self.parents[randrange(0, self.children_size, 1)])
                    parent_copy = parent_copy.right_recombine(self.parents[randrange(0, self.children_size, 1)])
                    # 设置取出个体的stats属性是一个空列表
                    parent_copy.stats = []
                    # 在children列表中添加该个体
                    self.children.append(parent_copy)

    # 定义实例化方法——再引入
    def reintroduction(self):
        # 在原有的population后添加生成的子代，共500+50个
        self.population += self.children
        # 清空子代列表
        self.children = []

    # 定义实例化方法——生存选择
    def survivalSelection(self):
        # 使用K-tournament方法进行筛选
        # 定义一个空列表new_pop，过渡用
        new_pop = []
        # 循环执行的次数为种群规模，初始化定义为**
        for _ in range(self.population_size):
            # 锦标赛选择法，选取一个片段，取出最大值
            chosen = max(sample(self.population, K_CONST))
            # 将筛选出的个体加入new_pop
            new_pop.append(chosen)
            # 移除种群中的该个体
            self.population.remove(chosen)
        # 将重新排序后的种群赋给population
        self.population = new_pop

    # 定义实例化方法——问题的适应度评估(GP类)
    def evaluate(self, problems, whether_complexity):
        whether_complexity = whether_complexity
        # 对子代中的个体进行遍历
        for individual in self.children:
            # 对每个个体执行核心evaluate(Individual类)方法
            Evaluate.evaluate(individual, problems, whether_complexity)
            # 执行一次循环，评估次数参数+1
            self.evaluations += 1

    # 定义实例化方法——未结束
    def not_finished(self):
        # 返还评估次数小于等于最大评估次数的布尔值
        return self.evaluations < MAX_EVALUATIONS

    # 定义实例化方法——运行
    def run(self, problems, test_index):
        print('start:'+str(test_index))
        # 记录代码运行时间
        start_time = time.process_time()
        # 设置bests为一个空列表，用于存储最优结果
        bests = []
        # 代数：最大评估次数减种群初始规模，除以子代规模，结果向上取整加1，设结果为x（保证与generation变量的匹配性）。
        generations = ceil((MAX_EVALUATIONS - self.population_size) / self.children_size) + 1
        # 生成了一个含x个空列表的列表，用于存储进化过程的数据
        data_best = [[] for _ in range(generations)]
        # 同上
        data_avg = [[] for _ in range(generations)]
        data_time = [[] for _ in range(generations)]
        data_complexity = [[] for _ in range(generations)]

        # 执行RUN次循环
        for run in range(RUNS):
            start_time1 = time.process_time()
            # 执行初始化操作
            self.__init__(number=self.number)
            # 初次评估，因为evaluate方法是针对children属性执行的，所以将population暂时转移了一下
            self.children = self.population
            # 执行适应度评估（GP类）
            self.evaluate(problems, test_index)
            self.population = self.children
            # 列表生成式，遍历population中每个元素的fitness（Tree模块中生成），生成目标值列表
            objective_data = [i.fitness for i in self.population]
            # 同上，生成复杂度列表
            complexity_data = [i.size for i in self.population]
            # 在data_best的第一个列表中添加最大的适应度值
            data_best[0].append(max(objective_data))
            # 在data_avg的第一个列表中添加平均适应度值
            data_avg[0].append(mean(objective_data))
            # 同上
            data_time[0].append(0)
            data_complexity[0].append(mean(complexity_data))

            # 正式执行进化操作
            # 先设置一个新变量
            generation = 1
            # 完成演化，判断not_finished方法的bool值，若评估次数evaluations<=设定值则继续执行
            while self.not_finished():
                print('evaluation'+str(generation))
                # 记录每代演化时间
                time1 = time.process_time()
                # 执行父代选择方法
                self.parentSelection()
                # 执行子代生成方法
                self.childGeneration()
                # 更新适应度评估（GP类，此方法执行一次，evaluations值会+20）
                self.evaluate(problems, test_index)
                # 执行再引入方法
                self.reintroduction()
                # 执行生存选择方法
                self.survivalSelection()
                # 记录每代演化时间
                time2 = time.process_time()

                # 记录进化过程数据
                # 列表生成式，遍历population中每个Individual的目标值
                objective_data = [i.objective for i in self.population]
                complexity_data = [i.size for i in self.population]
                # 在data_best的第generation（2-**）个列表中添加最大目标值
                data_best[generation].append(max(objective_data))
                # 在data_avg的第generation（2-**）个列表中添加平均目标值
                data_avg[generation].append(mean(objective_data))
                # 记录每代演化时间
                data_time[generation].append(time2 - time1)
                # 记录每代平均复杂度
                data_complexity[generation].append(mean(complexity_data))
                # 执行上述操作后，代数generation加1。跳出时填满data列表
                generation += 1
            end_time1 = time.process_time()

            # 本轮运行完成，输出优化信息
            # 输出本次运行次数（占位符）
            print('==== RUN {} ===='.format(run))
            # 设置当前最佳为population中的最优Individual（富比较）
            current_best = max(self.population)
            # 输出终代最优及平均Individual的适应度值和heuristic格式等信息
            print('best fitness: {}\nbest objective: {}\nmean objective: {}'
                  '\n(Min-based)heuristic-routing: {}\n(Min-based)heuristic-sequencing: {}'.
                  format(current_best.fitness, current_best.objective, data_avg[generation - 1],
                         current_best.root.left.string(), current_best.root.right.string()))
            print('time cost:{}'.format(end_time1 - start_time1))

            # 输出目标函数值
            print('total process time: {}\ntotal due time: {}\nmakespan: {}'.
                  format(current_best.total_process_time, current_best.total_due_time, current_best.makespan))
            # 输出stats值
            print('stats:{{{}, total set time: {}}}'.format(current_best.stats, current_best.total_transtime))
            # 列表bests中添加本轮的最优值
            bests.append(current_best)

        # 记录总演化时间
        end_time = time.process_time()
        # 结束上述所有轮运行，提示执行全局优化
        print('==== GLOBAL OPTIMUM ====')
        # 取bests列表中的最大值
        best = max(bests)

        # 解码
        # 索引解码
        decoding_array1 = best.root.decoding_index()
        decoding_array1 = [str(i) for i in decoding_array1]
        decoding_array1 = ','.join(decoding_array1)
        # 算子解码
        decoding_array2 = best.root.decoding_operation()
        decoding_array2 = [str(i) for i in decoding_array2]
        decoding_array2 = ','.join(decoding_array2)
        # 文字输出
        decoding_array3 = best.root.left.string()
        decoding_array4 = best.root.right.string()
        # node值解码
        # 算子解码
        decoding_array5 = best.root.decoding_val()
        decoding_array5 = [str(i) for i in decoding_array5]
        decoding_array5 = ','.join(decoding_array5)

        # 输出heuristic数据表格
        # 初始化一个excel
        df1 = pd.DataFrame({"Type": ['Index array', 'Operations array', 'Val', 'Routing heuristic', 'Sequencing heuristic'],
                           "Value": [decoding_array1, decoding_array2, decoding_array5, decoding_array3, decoding_array4]})
        df1 = df1.set_index("Type")
        df1.to_excel(os.path.dirname(os.getcwd()) + '\\output_file\\heuristic.xlsx')
        # 生成调度表
        data_jobs = []
        for i in range(len(best.draw_value)):
            data_job = []
            for j in best.draw_key[i]:
                data_job.append(j)
            for j in best.draw_value[i]:
                data_job.append(j)
            data_jobs.append(data_job)
        df2 = pd.DataFrame(data_jobs)
        df2.rename(columns={0: 'Job index', 1: 'Operation index', 2: 'Station index', 3: 'Start time', 4: 'Finish time',
                            5: 'Process time', 6: 'Setup time'}, inplace=True)
        df2 = df2.sort_values(by='Job index', ascending=True)
        df2 = df2.set_index("Job index")
        df2.to_excel(os.path.dirname(os.getcwd()) + '\\output_file\\schedule.xlsx')

        # 输出最优值的适应度和根字符
        print('best fitness: {}\nbest objective: {}'
              '\n(Min-based)heuristic-routing: {}\n(Min-based)heuristic-sequencing: {}'.
              format(best.fitness, best.objective,
                     best.root.left.string(), best.root.right.string()))
        # 输出目标函数值
        print('total process time: {}\ntotal due time: {}\nmakespan: {}'.
              format(best.total_process_time, best.total_due_time, best.makespan))
        # 输出最优值的stats
        print('stats: {{{}, total set time: {}, time cost: {}}}'.
              format(best.stats, best.total_transtime, round(end_time-start_time, 5)))

        # 传参用
        self.generations = generations
        self.data_avg = data_avg
        self.data_best = data_best
        self.data_time = data_time
        self.data_complexity = data_complexity
        self.time_cost = round((end_time-start_time)/RUNS, 4)
        # # 输出进化过程图
        # Plot.plt_evolve(self, generations, data_avg, data_best)
        # 输出最优方案的甘特图
        Plot.plt_gantt(best, self.number)
