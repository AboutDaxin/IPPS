# 定义一些键名，并赋值，用于生成列表
# 静态参数
CONST = 0  # 随机化常数

WIQ = 2  # 一个station完成当前的queue的总时间（work in queue）
rJ = 3  # 释放时间（release of job）
NPT = 4  # 下道序的执行时间（next process time）
PT = 5  # 当前序的执行时间（process time）
DD = 6  # 截止时间（due date）

# 算子
PLUS = 7
MINUS = 8
TIMES = 9
DIVIDED_BY = 10
MOD = 11
MAX = 12
MIN = 13

# 动态参数
NIQ = 1  # 一个station的queue中当前的job数量（number in queue）
TIS = 14  # 当前时间
NOR = 15  # job当前剩余工序数量（number of operations remaining）

# 使用列表对上列被赋值的参数进行分类，分为算子、非静态、叶节点(包含非静态)
OPERATORS = [PLUS, MINUS, TIMES, DIVIDED_BY, MOD, MAX, MIN]
NONSTATIC = [TIS, NOR, NIQ]
LEAVES = [CONST, WIQ, rJ, NPT, DD, PT, TIS, NOR, NIQ]

# 定义OPSUM为算子和叶节点合列表
OPSUM = OPERATORS + LEAVES
