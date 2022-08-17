# 定义一些键名，并赋值，用于生成列表
# 静态参数
CONST = 0  # 随机化常数
BLK_ST = 1  # 阻塞开始时间
BLK_TOT = 2  # 阻塞持续时间
RELEASE = 3  # 释放时间
N_P_T = 4  # 下道序执行时间
P_T = 5  # 执行时间
DEADLINE = 6  # 截止时间

# 算子
PLUS = 7
MINUS = 8
TIMES = 9
DIVIDED_BY = 10
MOD = 11
MAX = 12
MIN = 13

# 动态参数
CURRENT_TIME = 14  # 当前时间
J_DEADLINE = 15  # 作业截止时间
J_RELEASE = 16  # 作业释放时间
NOT_PERIODIC = 17  # 非周期参数
# S_QUE_NUM = 18  #

# 使用列表对上列被赋值的参数进行分类，分为算子、非静态、叶节点(包含非静态)
OPERATORS = [PLUS, MINUS, TIMES, DIVIDED_BY, MOD, MAX, MIN]
NONSTATIC = [CURRENT_TIME, J_DEADLINE, J_RELEASE]
LEAVES = [CONST, BLK_ST, BLK_TOT, RELEASE, N_P_T,
          DEADLINE, P_T, CURRENT_TIME, J_DEADLINE, J_RELEASE, NOT_PERIODIC]

# 定义OPSUM为算子和叶节点合列表
OPSUM = OPERATORS + LEAVES
