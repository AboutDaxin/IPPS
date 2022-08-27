# 定义一些键名，并赋值，用于生成列表
# 静态参数
CONST = 0  # 随机化常数（0-1）
rJ = 3  # job释放时间（release of job）
NPT = 4  # job下道序的执行时间（next process time）
PT = 5  # job当前序的执行时间（process time）
DD = 6  # job的交货期（due date）
# W = 17  # job权重（weight）

# 算子
PLUS = 7
MINUS = 8
TIMES = 9
DIVIDED_BY = 10
MOD = 11
MAX = 12
MIN = 13

# 动态参数
NIQ = 1  # station当前queue中的job数量（number in queue）
WIQ = 2  # station当前queue中的job的总作业时间（work in queue）
TIS = 14  # 系统时间
NOR = 15  # job当前剩余工序数量（number of operations remaining）
WR = 16  # job当前剩余工序时间(work remaining of job)

# 使用列表对上列被赋值的参数进行分类，分为算子、非静态、叶节点(包含非静态)
OPERATORS = [PLUS, MINUS, TIMES, DIVIDED_BY, MOD, MAX, MIN]
NONSTATIC = [TIS, NOR, NIQ, WIQ, WR]
LEAVES = [CONST, WIQ, rJ, NPT, DD, PT, TIS, NOR, NIQ, WR]

# 定义OPSUM为算子和叶节点合列表
OPSUM = OPERATORS + LEAVES
