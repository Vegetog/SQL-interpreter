class SelectStatement:
    def __init__(self, columns, from_table, where=None, order_by=None, limit=None, join=None):
        self.columns = columns  # 列表: Column
        self.from_table = from_table  # 字符串
        self.where = where  # BinaryOp/LogicOp/None
        self.order_by = order_by  # 列表: (列名, 升降序) 元组，或 None
        self.limit = limit  # 整数或 None
        self.join = join  # JoinClause 或 None

class Column:
    def __init__(self, name, alias=None):
        self.name = name  # 字符串
        self.alias = alias  # 字符串或 None

class BinaryOp:
    def __init__(self, left, op, right):
        self.left = left  # 可以是 Column/Value/BinaryOp
        self.op = op  # 字符串
        self.right = right  # 可以是 Column/Value/BinaryOp

class Value:
    def __init__(self, value):
        self.value = value 

class InsertStatement:
    def __init__(self, table, columns, values):
        self.table = table          # 表名
        self.columns = columns      # 列名列表
        self.values = values        # 多行插入: [ [v1, v2, ...], [v1, v2, ...], ... ]

class UpdateStatement:
    def __init__(self, table, assignments, where=None):
        self.table = table              # 表名
        self.assignments = assignments  # 列名到新值的映射 dict
        self.where = where              # 条件（可选）

class DeleteStatement:
    def __init__(self, table, where=None):
        self.table = table      # 表名
        self.where = where      # 条件（可选） 

class LogicOp:
    def __init__(self, op, left, right=None):
        self.op = op      # 'AND', 'OR', 'NOT'
        self.left = left  # 左操作数（可以是 BinaryOp、LogicOp、Column、Value）
        self.right = right  # 右操作数（NOT 时为 None） 

class TableColumn:
    def __init__(self, name, col_type=None, constraints=None):
        self.name = name
        self.col_type = col_type  # 如 INT, TEXT, CHAR(50), REAL
        self.constraints = constraints or []  # 如 ['PRIMARY KEY', 'NOT NULL']

class CreateTableStatement:
    def __init__(self, table, columns):
        self.table = table      # 表名
        self.columns = columns  # 列表: TableColumn 

class DropTableStatement:
    def __init__(self, table):
        self.table = table  # 表名 

class JoinClause:
    def __init__(self, left_table, right_table, join_type, on_expr):
        self.left_table = left_table
        self.right_table = right_table
        self.join_type = join_type  # 'INNER'
        self.on_expr = on_expr      # ON 条件表达式 

class UnionStatement:
    def __init__(self, selects, all=False):
        self.selects = selects  # List[SelectStatement]
        self.all = all          # True=UNION ALL, False=UNION 

class IntersectStatement:
    def __init__(self, selects):
        self.selects = selects  # List[SelectStatement] 

class ExceptStatement:
    def __init__(self, selects):
        self.selects = selects  # List[SelectStatement] 