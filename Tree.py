import copy
from random import choice, randint
from copy import deepcopy
from Operations import *  # import operation constants (bastardized Sum-Type)


# 定义Node类，包含该节点及其子节点的一系列属性和方法
class Node:
    # 定义初始化属性和方法，left、right也为节点类，val为0，op的CONST在Operations模块中定义为0
    def __init__(self, left=None, right=None, val=0, op=CONST):
        self.left = left
        self.right = right
        self.val = val
        self.op = op

    # 实例化方法——节点下的树规模
    # 总结：返还该节点下所有节点数量（包含此节点）
    def size(self):
        # 如果该节点的left或right不是空的，就递归执行size，是空的就返还0+1+0
        return (self.left.size() if self.left is not None else 0) + 1 + \
               (self.right.size() if self.right is not None else 0)

    # 实例化方法——判断是否为非静态
    # 总结：节点下有任何一个子节点的op为NONSTATIC就返还True
    def uses_nonstatic(self):
        # 如果该节点没有子节点，则返还根节点的op是否在NONSTATIC中
        if self.left is None and self.right is None:
            return self.op in NONSTATIC
        # 如果该节点有一侧是空节点，输出错误信息
        elif self.left is None and self.right is not None or self.right is None and self.left is not None:
            print('!!!!!!!malformed tree!!!!!!!!!')
        # 如果该节点有两个子节点。如果op属于NONSTATIC，返还True；如果不属于，则进行递归，bool结果取并集
        else:
            return True if self.op in NONSTATIC else self.left.uses_nonstatic() or self.right.uses_nonstatic()

    # 实例化方法——grow生成法
    # 总结：生成非完成结构树，只限制最大深度，叶节点为LEAVES参数，非叶节点为OPERATORS参数
    def grow(self, depth_limit):
        # 如果此时的深度参数为0，则op为LEAVES中一个随机项
        if depth_limit == 0:
            self.op = choice(LEAVES)
        # 深度参数不是0时，op为OPSUM（OPERATORS并LEAVES）中的一个随机项
        else:
            # 保证深度>1的情况下，有0.3的概率在节点选择操作算子
            if depth_limit == 5 or randint(0, 1) < 0.3:
                self.op = choice(OPERATORS)
            # 有0.7的概率选择叶节点
            else:
                self.op = choice(LEAVES)
        # 如果op选中的是OPERATORS中的项，则对左右节点进行递归，limit减1，
        if self.op in OPERATORS:
            self.left = Node()
            self.left.grow(depth_limit - 1)
            self.right = Node()
            self.right.grow(depth_limit - 1)
        # 如果op是个常系数（在LEAVES中），则节点的val值为一个0-255（包含端点）的整数
        elif self.op == CONST:
            self.val = randint(0, 1)
        # 如果选中的不是OPERATORS，也不是LEAVES中的CONST，就结束生成

    # 实例化方法——full生成法
    # 总结：生成完整结构树，全按最大深度生成，叶节点为LEAVES参数，非叶节点为OPERATORS参数
    def full(self, depth_limit):
        # 如果此时的深度参数已变为0，则op为LEAVES中一个随机项
        if depth_limit == 0:
            self.op = choice(LEAVES)
        # 深度参数不是0时，op属性为OPERATORS中一个随机项
        else:
            self.op = choice(OPERATORS)
            # 定义节点的“左”为一个Node类，并对左节点递归执行full生成，limit减1，直到0选取LEAVES节点
            self.left = Node()
            self.left.full(depth_limit - 1)
            # 右节点同上
            self.right = Node()
            self.right.full(depth_limit - 1)
        # 如果节点的op是一个常系数（LEAVES中），则节点的val值为一个0-255（包含端点）的整数
        if self.op == CONST:
            self.val = randint(0, 1)

    # 实例化方法——选择节点
    # 总结：返还Node的随机节点被node替换后的新Node）
    def choose_node(self, graft=False, node=None):
        # 定义一个choose_r函数（输入一个初始化辅助树列表，一个节点实例，一个初始化索引）
        # 总结：该方法返还一个树结构列表，列表中的索引数字代表了树结构特定位置节点（以层定位，根节点为1，左节点偶，右节点奇）
        def choose_r(tree_array1, node1, i):
            # 如果节点实例的左节点非空且不是叶节点执行以下操作
            if node1.left is not None and node1.op not in LEAVES:
                # 下一个索引翻倍
                next_idx = 2 * i
                # 在当前辅助树列表中添加该索引
                tree_array1.append(next_idx)
                # 对当前实例左节点进行递归
                tree_array1 = choose_r(tree_array1, node1.left, next_idx)
            # 同上（除根节点外，左节点索引为偶数，右节点为奇数）
            if node1.right is not None and node1.op not in LEAVES:
                next_idx = (2 * i) + 1
                tree_array1.append(next_idx)
                tree_array1 = choose_r(tree_array1, node1.right, next_idx)
            # 返还该树列表
            return tree_array1

        # 初始化一个树列表
        tree_array = [1]
        # 对当前节点执行choose_r，生成辅助列表tree_array
        tree_array = choose_r(tree_array, self, 1)
        # 从树列表中随机抽取一个元素，代表选中的节点索引
        random_node = 1 if tree_array == [] else choice(tree_array)

        # 开始生成选中节点的索引
        random_node1 = random_node
        # 初始化一个父列表，用于存放选中节点的所有父节点的索引（不包括根节点）
        parent_list = []
        # 当选中的节点不是根节点时进行以下循环
        while random_node1 != 1:
            # 对节点元素进行地板除，即找到选中节点的上一层节点索引
            random_node1 = random_node1 // 2
            # 在父列表中增加这一索引，到根节点[1]结束（包括1）
            parent_list.append(random_node1)
        # 删除父列表最后添加的那个元素，即根节点[1]
        if parent_list:
            parent_list.pop()
        # 翻转父列表中的元素次序，变为从小到大
        parent_list.reverse()

        # 定义一个current_node为Node实例自身
        current_node = self
        # 使用随机所选节点对当前节点进行替代（根据父列表，是偶数走一次左节点，是奇数走一次右节点）
        for index in range(len(parent_list)):
            if index == len(parent_list):
                break
            current_node = current_node.left if parent_list[index] % 2 == 0 else current_node.right
            # 至此，current_node已变为Node实例的一个随机子节点的父节点

        # 如果graft为true则执行交叉
        if graft:
            # 设置一个参数，判断是否是叶节点
            spam = False
            # 如果随机选中的节点是根节点
            if random_node == 1:
                # 对实例使用参数中输入的节点进行代替
                self = deepcopy(node)
            # 随机选中的节点不是根节点时
            else:
                # # 从这个地方返回出来的current_node是一个node对象，但是对于current_node本身而言，它自己只是一个指针，指向实际存储node对象的物理地址
                # # 这种写法，是使current_node这个指针重新偏向，指向常量1。这种，就是内存指针上的修改
                # # current_node = 1
                # if parent_list[len(parent_list) - 1] % 2 == 0:
                #     # 这种写法，是使current_node这个指针指向的对象的left属性发生物理层面的修改
                #     current_node.left = node
                # else:
                #     current_node.right = node
                # 如果所选节点为叶节点
                if current_node.op in LEAVES:
                    print('PANIC!!!!!')
                    print('OP:{}'.format(current_node.op))
                    spam = True
                # 如果所选节点属于左节点
                if random_node % 2 == 0:
                    # 如果是叶节点则执行输出
                    if spam:
                        print('CURRENT:{}'.format(current_node))
                        print('LEFT:{}'.format(current_node.left))
                    # 将输入节点移植到current_node的左节点
                    current_node.left = deepcopy(node)
                # 如果所选节点是右节点，同上
                else:
                    if spam:
                        print('CURRENT:{}'.format(current_node))
                        print('RIGHT:{}'.format(current_node.right))
                    current_node.right = deepcopy(node)
        # 返还所选节点
            return self
        else:
            return current_node

    # 实例化方法——重组
    def recombine(self, other):
        # 将other.choose_node移植在Node的一个子节点下，返还该子节点
        # other.choose_node只是一个other中被随机选中的current_node
        self.choose_node(True, other.choose_node(False, None))
        return self

    # 实例化方法——树解析（输入作业和当前时间）
    # 总结：根据当前job、Individual、时间，返还该job的优先级数值
    def interpret(self, job, station, current_time):
        # 如果节点op是个常数，返还它的值
        if self.op == CONST:
            return self.val
        # 阻塞开始时间
        elif self.op == BLK_ST:
            return job.task.blocking_start
        # 阻塞持续时间
        elif self.op == BLK_TOT:
            return job.task.blocking_duration
        # 释放时间
        elif self.op == RELEASE:
            return job.task.release
        # 阶段
        elif self.op == N_P_T:
            return job.task.exec_time[1] if len(job.task.exec_time) > 1 else 0
        # 执行时间
        elif self.op == P_T:
            return job.task.exec_time[0]
        # 单项任务的交货期
        elif self.op == DEADLINE:
            return job.task.deadline if job.task.deadline != 0 else float('Inf')
        # 加法，对左右节点进行递归并相加
        elif self.op == PLUS:
            return self.left.interpret(job, station, current_time) + self.right.interpret(job, station, current_time)
        # 减法，同上
        elif self.op == MINUS:
            return self.left.interpret(job, station, current_time) - self.right.interpret(job, station, current_time)
        # 求余，左除以右，求余
        elif self.op == MOD:
            right = self.right.interpret(job, station, current_time)
            left = self.left.interpret(job, station, current_time)
            return left if right == 0 else left % right
        # 乘
        elif self.op == TIMES:
            return self.left.interpret(job, station, current_time) * self.right.interpret(job, station, current_time)
        # 除以，左除以右
        elif self.op == DIVIDED_BY:
            right = self.right.interpret(job, station, current_time)
            return 0 if right == 0 else self.left.interpret(job, station, current_time) / right
        # 取最大
        elif self.op == MAX:
            return max(self.left.interpret(job, station, current_time),
                       self.right.interpret(job, station, current_time))
        # 取最小
        elif self.op == MIN:
            return min(self.left.interpret(job, station, current_time),
                       self.right.interpret(job, station, current_time))
        # 返还当前时间（输入的参数）
        elif self.op == CURRENT_TIME:
            return current_time
        # 作业的交货期
        elif self.op == J_DEADLINE:
            return job.deadline if job.deadline != 0 else float('Inf')
        # 作业的释放时间
        elif self.op == J_RELEASE:
            return job.release
        # 是否阶段性，返还1,2,3
        elif self.op == NOT_PERIODIC:
            return 0 if job.task.period != 0 else 1 if job.task.deadline != 0 else 2
        else:
            print('HELP')

    # 实例化方法——显示字符串
    # 总结：返还节点的类型名称，辅助上方evaluate使用
    def string(self):
        if self.op == CONST:
            return repr(self.val)
        elif self.op == BLK_ST:
            return 'BLK_ST'
        elif self.op == BLK_TOT:
            return 'BLK_TOT'
        elif self.op == RELEASE:
            return 'TASK_RELEASE'
        elif self.op == N_P_T:
            return 'NEXT_PROCESS_TIME'
        elif self.op == P_T:
            return 'PROCESS_TIME'
        elif self.op == DEADLINE:
            return 'TASK_DEADLINE'
        elif self.op == PLUS:
            return '(' + self.left.string() + ' + ' + self.right.string() + ')'
        elif self.op == MINUS:
            return '(' + self.left.string() + ' - ' + self.right.string() + ')'
        elif self.op == MOD:
            return '(' + self.left.string() + ' % ' + self.right.string() + ')'
        elif self.op == TIMES:
            return '(' + self.left.string() + ' * ' + self.right.string() + ')'
        elif self.op == DIVIDED_BY:
            return '(' + self.left.string() + ' / ' + self.right.string() + ')'
        elif self.op == MAX:
            return 'MAX(' + self.left.string() + ', ' + self.right.string() + ')'
        elif self.op == MIN:
            return 'MIN(' + self.left.string() + ', ' + self.right.string() + ')'
        elif self.op == CURRENT_TIME:
            return 'TIME'
        elif self.op == J_DEADLINE:
            return 'JOB_DEADLINE'
        elif self.op == J_RELEASE:
            return 'JOB_RELEASE'
        elif self.op == NOT_PERIODIC:
            return 'PERIODICITY'
        else:
            print('HELP')


# 定义Individual类
class Individual:
    # 初始化方法，输入一个简化系数
    def __init__(self, parsimony=0.5):
        # 定义一系列参数（适应度，状态，根，规模，简化参数）
        self._size = None
        self._use_nonstatic = None
        self.scheme = None
        # 用于存储适应度值
        self.fitness = 0
        self.fitnesses = []
        # 用于存储各项目标函数值
        self.total_process_time = 0
        self.total_due_time = 0
        # 用于展示一些数据
        self.stats = []
        # 用于存储排产方案的辅助列表
        self.draw_key = []
        # 个体的root是一个Node类实体
        self.root = Node()
        self.size = 0
        self.parsimony = parsimony

    # 富比较方法，比较实例的大小时比较其fitness
    def __lt__(self, other):
        return self.fitness < other.fitness

    # 实例化方法——调用Node类的grow方法（在根节点执行grow）
    def grow(self, depth):
        self.root.grow(depth)

    # 实例化方法——同上
    def full(self, depth):
        self.root.full(depth)

    # 实例化方法——调用Node类的重组方法
    def recombine(self, other):
        self.root.recombine(other.root)
        return self

    # 实例化方法——个体复杂度
    def tree_complexity(self):
        # _size为根节点的规模
        self._size = self.root.size()
        # 判断个体是否为非静态（有非静态就返还True）
        self._use_nonstatic = self.root.uses_nonstatic()
        # 返还复杂度值（非静态个体系数取2，静态取1，应该用于判断适应度值）
        return 1 - 1 / (self.root.size() * self.parsimony * (2 if self.root.uses_nonstatic() else 1))
