from random import sample, random, randrange
from copy import deepcopy
from statistics import mean
from math import floor, ceil
import Evaluate
from Tree import Individual
import Plot


# 设置一个常数K，用于后边锦标赛法选择子代
K_CONST = 10
# 最大评估次数
MAX_EVALUATIONS = 2000
# 最小步长
MIN_DELTA = 0.001
# 运行多少次
RUNS = 3


# 定义GP类
class GP:
    # 初始化方法：在GP类进行实例化时执行。参数为：种群规模1000，子规模20，变异率0.05，复制率0.1，简化参数0.5
    def __init__(self, population_size=1000, children_size=20, mutation=0.05, duplication=0.1, parsimony=0.5):
        # 生成此实例的一个种群
        # 类属性：定义实例的种群(population)为一个列表
        self.population = []

        # grow方法生成半个种群
        # 设置一个用于生成种群的循环，为种群规模的一半，floor表示向下取整
        for _ in range(floor(population_size/2)):
            # 实例化个体，使用Tree模块的Individual类
            individual = Individual(parsimony)
            # 使用grow方法形成个体，使用Tree模块的grow函数
            individual.grow(5)
            # 在种群列表中增加这个个体
            self.population.append(individual)

        # full方法生成剩下半个种群，并结合起来
        # 设置一个用于生成种群的循环，为种群规模的一半，ceil表示向上取整
        for _ in range(ceil(population_size/2)):
            # 实例化个体，使用Tree模块的Individual类
            individual = Individual(parsimony)
            # 使用full方法形成个体，使用Tree模块的full函数
            individual.full(5)
            # 在种群列表中增加这个个体，完成整个种群的构建
            self.population.append(individual)

        # 设置此实例的一些初始化变量
        # “父”，“子”为空列表，父，子种群规模为预设的1000和20，变异率0.05，辅助率0.1，交叉率0.85
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
        # 执行一个筛选父代的循环，次数为要产生的子代的规模20
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
        # 执行一个生成子代的循环，次数为要产生的子代的规模20，用于逐个判断是否要进行变异
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
            elif self.mutation <= temprandom < self.duplication:
                parent_copy = deepcopy(self.parents[i])
                self.children.append(parent_copy)
            # 执行交叉操作
            else:
                # 让第i个个体跟它后一个进行交叉
                parent_copy = deepcopy(self.parents[i]).recombine(self.parents[randrange(0, self.children_size, 1)])
                # 设置取出个体的stats属性是一个空列表
                parent_copy.stats = []
                # 在children列表中添加该个体
                self.children.append(parent_copy)

    # 定义实例化方法——再引入
    def reintroduction(self):
        # 在原有的population后添加生成的子代，共1000+20个
        self.population += self.children
        # 清空子代列表
        self.children = []

    # 定义实例化方法——生存选择
    def survivalSelection(self):
        # 使用K-tournament方法进行筛选
        # 定义一个空列表new_pop，过渡用
        new_pop = []
        # 循环执行的次数为种群规模，初始化定义为1000
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
    def evaluate(self, problems):
        # 对子代中的个体进行遍历
        for individual in self.children:
            # 对每个个体执行核心evaluate(Individual类)方法
            Evaluate.evaluate(individual, problems)
            # 执行一次循环，评估次数参数+1
            self.evaluations += 1

    # 定义实例化方法——未结束
    def not_finished(self):
        # 返还评估次数小于等于最大评估次数2000的布尔值
        return self.evaluations <= MAX_EVALUATIONS

    # 定义实例化方法——运行
    def run(self, problems):
        # 设置bests为一个空列表，用于存储最优结果
        bests = []
        # 代数：最大评估次数2000减种群规模1000，除以子代规模20，结果向上取整加2，为52（保证与generation变量的匹配性）。
        generations = ceil((MAX_EVALUATIONS - self.population_size) / self.children_size) + 2
        # 生成了一个含52个空列表的列表，用于存储进化过程的数据
        data_best = [[] for _ in range(generations)]
        # 同上
        data_avg = [[] for _ in range(generations)]

        # 执行RUN次循环
        for run in range(RUNS):
            # 执行初始化操作
            self.__init__()
            # 初次评估，因为evaluate方法是针对children属性执行的，所以将population暂时转移了一下
            self.children = self.population
            # 执行适应度评估（GP类）
            self.evaluate(problems)
            self.population = self.children
            # 列表生成式，遍历population中每个元素的fitness（Tree模块中生成），生成列表fitness_data
            fitness_data = [i.fitness for i in self.population]
            # 在data_best的第一个列表中添加最大的适应度值
            data_best[0].append(max(fitness_data))
            # 在data_avg的第一个列表中添加平均适应度值
            data_avg[0].append(mean(fitness_data))

            # 正式执行进化操作
            # 先设置一个新变量
            generation = 1
            # 判断not_finished方法的bool值，若评估次数evaluations<=2000则继续执行
            # 注：每一次evaluations值会加20 ，初始化种群后为1000。因此跳出时，evaluations值为2020，而generation此时正好为52
            while self.not_finished():
                # 执行父代选择方法
                self.parentSelection()
                # 执行子代生成方法
                self.childGeneration()
                # 更新适应度评估（GP类，此方法执行一次，evaluations值会+20）
                self.evaluate(problems)
                # 执行再引入方法
                self.reintroduction()
                # 执行生存选择方法
                self.survivalSelection()

                # 记录进化过程数据
                # 列表生成式，遍历population中每个Individual的fitness，生成列表fitness_data
                fitness_data = [i.fitness for i in self.population]
                # 在data_best的第generation（2-52）个列表中添加最大的适应度值
                data_best[generation].append(max(fitness_data))
                # 在data_avg的第generation（2-52）个列表中添加平均适应度值
                data_avg[generation].append(mean(fitness_data))
                # 执行上述操作后，代数generation加1。跳出时正好为52，填满data列表
                generation += 1

            # 本轮运行完成，输出优化信息
            # 输出本次运行次数（占位符）
            print('==== RUN {} ===='.format(run))
            # 设置当前最佳为population中的最优Individual（富比较）
            current_best = max(self.population)
            # 输出最优Individual的适应度值和heuristic格式
            print('best fitness: {}\n(Min-based)heuristic-routing: {}\n(Min-based)heuristic-sequencing: {}'.
                  format(current_best.fitness, current_best.root.left.string(), current_best.root.right.string()))
            # 输出目标函数值
            print('total process time: {}\ntotal due time: {}\nmakespan: {}'.
                  format(current_best.total_process_time, current_best.total_due_time, current_best.makespan))
            # 输出stats值
            print('stats:{{{}, total set time: {}}}'.format(current_best.stats, current_best.total_transtime))
            # 列表bests中添加本轮的最优值
            bests.append(current_best)

        # 结束上述所有轮运行，提示执行全局优化
        print('==== GLOBAL OPTIMUM ====')
        # 去bests列表中的最大值
        best = max(bests)
        # 输出最优值的适应度和根字符
        print('best fitness: {}\n(Min-based)heuristic-routing: {}\n(Min-based)heuristic-sequencing: {}'.
              format(best.fitness, best.root.left.string(), best.root.right.string()))
        # 输出目标函数值
        print('total process time: {}\ntotal due time: {}\nmakespan: {}'.
              format(best.total_process_time, best.total_due_time, best.makespan))
        # 输出最优值的stats
        print('stats: {{{}, total set time: {}}}'.format(best.stats, best.total_transtime))

        # 输出进化过程图
        Plot.plt_evolve(self, generations, data_avg, data_best)
        # 输出最优方案的甘特图
        Plot.plt_gantt(best)
