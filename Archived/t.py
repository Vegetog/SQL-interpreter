# 自动生成的Python代码 - 由SQL翻译器生成
# 原始SQL文件: t.sql

# 初始化数据结构

# --------------------------------------------------
# CREATE TABLE f
# (
#     id INT PRIMARY KEY NOT NULL,
#     i  TEXT            NOT NULL,
#     j  INT             NOT NULL,
#     k  CHAR(50),
#     m  REAL
# )
# 创建表: f
f = []  # 每次建表自动清空表数据
f_schema = {
    "id": "int",
    "i": "str",
    "j": "int",
    "k": "str",
    "m": "float"
}
