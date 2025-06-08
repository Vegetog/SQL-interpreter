import re

class Token:
    def __init__(self, type_, value, position):
        self.type = type_
        self.value = value
        self.position = position
    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.position})"

# token_specification 定义了词法分析器要识别的所有 Token 类型及其正则表达式
# 顺序很重要，先匹配的优先ß
token_specification = [
    ('COMMENT',  r'--.*'),                # 单行注释
    ('MLCOMMENT', r'/\*[\s\S]*?\*/'), # 多行注释
    ('NUMBER',   r'\d+(?:\.\d+)?'),      # 数字（整数或小数），如 123 或 45.67
    ('STRING',   r"'(?:[^']|'')*'"),      # 字符串字面量，单引号包裹，如 'abc'，支持转义''
    ('IDENT',    r'[A-Za-z_][A-Za-z0-9_]*'), # 标识符（表名、列名、关键字），以字母或下划线开头，后接字母/数字/下划线
    ('DOT',      r'\.'),                  # 点号 .
    ('OP',       r'=|<>|!=|<=|>=|<|>|\+|-|\*|/'), # 操作符，包括=、<>、!=、<=、>=、<、>、+、-、*、/
    ('COMMA',    r','),                    # 逗号，用于分隔列
    ('LPAREN',   r'\('),                  # 左括号
    ('RPAREN',   r'\)'),                  # 右括号
    ('SKIP',     r'[ \t\n]+'),           # 跳过空格、制表符、换行符
    ('MISMATCH', r'.'),                    # 其他未匹配字符，遇到报错
]
tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)

KEYWORDS = {
    'SELECT', 'FROM', 'WHERE', 'INSERT', 'INTO', 'VALUES', 'UPDATE', 'SET', 'DELETE',
    'CREATE', 'TABLE', 'DROP', 'PRIMARY', 'KEY', 'NOT', 'NULL', 'ORDER', 'BY', 'ASC', 'DESC',
    'LIMIT', 'UNION', 'ALL', 'JOIN', 'INNER', 'LEFT', 'RIGHT', 'FULL', 'OUTER', 'ON', 'CROSS',
    'INTERSECT', 'EXCEPT'
}

def tokenize(sql):
    tokens = []
    for mo in re.finditer(tok_regex, sql):
        kind = mo.lastgroup
        value = mo.group()
        pos = mo.start()
        if kind == 'SKIP' or kind == 'COMMENT' or kind == 'MLCOMMENT':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Unexpected character {value!r} at {pos}')
        if kind == 'IDENT' and value.upper() in KEYWORDS:
            kind = value.upper()
        tokens.append(Token(kind, value, pos))
    return tokens 