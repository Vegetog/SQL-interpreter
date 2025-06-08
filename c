from ast_nodes import SelectStatement, Column, BinaryOp, Value, InsertStatement, UpdateStatement, DeleteStatement, LogicOp, CreateTableStatement, TableColumn, DropTableStatement, JoinClause, UnionStatement, IntersectStatement

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def eat(self, type_=None):
        tok = self.current()
        if tok is None:
            return None
        if type_ is not None and tok.type != type_:
            raise RuntimeError(f'Expected {type_}, got {tok.type}')
        self.pos += 1
        return tok

    def parse(self):
        stmt = self.parse_single()
        stmts = [stmt]
        mode = None  # 'UNION'、'INTERSECT'、'EXCEPT'
        all_flag = False
        while self.current() and self.current().type in ('UNION', 'INTERSECT', 'EXCEPT'):
            print('[parser调试] 当前token:', self.current().type)
            if self.current().type == 'UNION':
                self.eat('UNION')
                mode = 'UNION'
                if self.current() and self.current().type == 'ALL':
                    self.eat('ALL')
                    all_flag = True
                stmts.append(self.parse_single())
            elif self.current().type == 'INTERSECT':
                self.eat('INTERSECT')
                mode = 'INTERSECT'
                stmts.append(self.parse_single())
            elif self.current().type == 'EXCEPT':
                self.eat('EXCEPT')
                mode = 'EXCEPT'
                stmts.append(self.parse_single())
        print('[parser调试] mode:', mode, 'stmts类型:', [type(s).__name__ for s in stmts])
        if len(stmts) > 1:
            if mode == 'UNION':
                print('[parser调试] 返回UnionStatement')
                return UnionStatement(stmts, all=all_flag)
            elif mode == 'INTERSECT':
                print('[parser调试] 返回IntersectStatement')
                return IntersectStatement(stmts)
            elif mode == 'EXCEPT':
                print('[parser调试] 返回ExceptStatement')
                from ast_nodes import ExceptStatement
                return ExceptStatement(stmts)
        return stmt

    def parse_single(self):
        tok = self.current()
        if tok.type in ('IDENT', 'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP'):
            keyword = tok.value.upper()
            if keyword == 'SELECT':
                return self.parse_select()
            elif keyword == 'INSERT':
                return self.parse_insert()
            elif keyword == 'UPDATE':
                return self.parse_update()
            elif keyword == 'DELETE':
                return self.parse_delete()
            elif keyword == 'CREATE':
                return self.parse_create_table()
            elif keyword == 'DROP':
                return self.parse_drop_table()
            else:
                raise RuntimeError(f'不支持的SQL类型: {keyword}')
        else:
            raise RuntimeError('SQL语句必须以关键字开头')

    def parse_select(self):
        self.eat('SELECT')  # SELECT
        columns = self.parse_column_list()
        self.eat('FROM')  # FROM
        table = self.eat('IDENT').value
        join = None
        # 检查是否有 JOIN
        if self.current() and self.current().type in ('JOIN', 'INNER', 'LEFT', 'RIGHT', 'FULL', 'CROSS'):
            join_type = 'INNER'
            if self.current().type == 'INNER':
                self.eat('INNER')
                self.eat('JOIN')
            elif self.current().type == 'LEFT':
                self.eat('LEFT')
                if self.current() and self.current().type == 'OUTER':
                    self.eat('OUTER')
                self.eat('JOIN')
                join_type = 'LEFT'
            elif self.current().type == 'RIGHT':
                self.eat('RIGHT')
                if self.current() and self.current().type == 'OUTER':
                    self.eat('OUTER')
                self.eat('JOIN')
                join_type = 'RIGHT'
            elif self.current().type == 'FULL':
                self.eat('FULL')
                if self.current() and self.current().type == 'OUTER':
                    self.eat('OUTER')
                self.eat('JOIN')
                join_type = 'FULL'
            elif self.current().type == 'CROSS':
                self.eat('CROSS')
                self.eat('JOIN')
                join_type = 'CROSS'
            else:
                self.eat('JOIN')
            right_table = self.eat('IDENT').value
            # 只CROSS JOIN不需要ON
            if join_type == 'CROSS':
                on_expr = None
            else:
                if self.current() and self.current().type == 'ON':
                    self.eat('ON')
                    on_expr = self.parse_expr()
                else:
                    raise RuntimeError('JOIN 目前只支持 ON 子句')
            join = JoinClause(table, right_table, join_type, on_expr)
        where = None
        order_by = None
        limit = None
        if self.current() and self.current().type == 'WHERE':
            self.eat('WHERE')  # WHERE
            where = self.parse_expr()  # 支持复杂表达式
        # 解析 ORDER BY
        if self.current() and self.current().type == 'ORDER':
            self.eat('ORDER')  # ORDER
            self.eat('BY')  # BY
            order_by = []
            while True:
                col = self.eat('IDENT').value
                direction = 'ASC'
                if self.current() and self.current().type in ('ASC', 'DESC'):
                    direction = self.eat(self.current().type).value.upper()
                order_by.append((col, direction))
                if self.current() and self.current().type == 'COMMA':
                    self.eat('COMMA')
                else:
                    break
        # 解析 LIMIT
        if self.current() and self.current().type == 'LIMIT':
            self.eat('LIMIT')  # LIMIT
            tok = self.eat('NUMBER')
            limit = int(tok.value)
        return SelectStatement(columns, table, where, order_by, limit, join)

    def parse_column_list(self):
        columns = []
        if self.current() and self.current().type == 'OP' and self.current().value == '*':
            self.eat('OP')
            columns.append(Column('*'))
            return columns
        while True:
            col = self.parse_column_name()
            columns.append(Column(col))
            if self.current() and self.current().type == 'COMMA':
                self.eat('COMMA')
            else:
                break
        return columns

    def parse_column_name(self):
        # 支持表.字段
        name = self.eat('IDENT').value
        if self.current() and self.current().type == 'DOT':
            self.eat('DOT')
            name2 = self.eat('IDENT').value
            return f'{name}.{name2}'
        return name

    def parse_condition(self):
        # 兼容旧接口，直接调用 parse_expr
        return self.parse_expr()

    # 递归下降表达式解析：OR > AND > NOT > 原子
    def parse_expr(self):
        return self.parse_or()

    def parse_or(self):
        left = self.parse_and()
        while self.current() and self.current().type == 'IDENT' and self.current().value.upper() == 'OR':
            self.eat('IDENT')
            right = self.parse_and()
            left = LogicOp('OR', left, right)
        return left

    def parse_and(self):
        left = self.parse_not()
        while self.current() and self.current().type == 'IDENT' and self.current().value.upper() == 'AND':
            self.eat('IDENT')
            right = self.parse_not()
            left = LogicOp('AND', left, right)
        return left

    def parse_not(self):
        if self.current() and self.current().type == 'IDENT' and self.current().value.upper() == 'NOT':
            self.eat('IDENT')
            operand = self.parse_not()
            return LogicOp('NOT', operand)
        else:
            return self.parse_atom()

    def parse_atom(self):
        if self.current() and self.current().type == 'LPAREN':
            self.eat('LPAREN')
            expr = self.parse_expr()
            self.eat('RPAREN')
            return expr
        else:
            # 解析表.字段 = 表.字段 或 = 值
            left = self.parse_column_name()
            op = self.eat('OP').value
            # 右侧可以是表.字段，也可以是常量
            if self.current().type == 'IDENT':
                right = Column(self.parse_column_name())
            elif self.current().type == 'NUMBER':
                tok = self.eat('NUMBER')
                right = Value(float(tok.value) if '.' in tok.value else int(tok.value))
            elif self.current().type == 'STRING':
                tok = self.eat('STRING')
                right = Value(tok.value.strip("'"))
            else:
                tok = self.eat()
                right = Value(tok.value)
            return BinaryOp(Column(left), op, right)

    def parse_insert(self):
        self.eat('INSERT')  # INSERT
        self.eat('INTO')  # INTO
        table = self.eat('IDENT').value
        columns = []
        if self.current() and self.current().type == 'LPAREN':
            self.eat('LPAREN')
            while True:
                columns.append(self.eat('IDENT').value)
                if self.current() and self.current().type == 'COMMA':
                    self.eat('COMMA')
                else:
                    break
            self.eat('RPAREN')
        self.eat('VALUES')  # VALUES
        values_list = []
        while True:
            self.eat('LPAREN')
            values = []
            while True:
                tok = self.eat()
                if tok.type == 'NUMBER':
                    val = float(tok.value) if '.' in tok.value else int(tok.value)
                elif tok.type == 'STRING':
                    val = tok.value.strip("'")
                else:
                    val = tok.value
                values.append(Value(val))
                if self.current() and self.current().type == 'COMMA':
                    self.eat('COMMA')
                else:
                    break
            self.eat('RPAREN')
            values_list.append(values)
            if self.current() and self.current().type == 'COMMA':
                self.eat('COMMA')
            else:
                break
        return InsertStatement(table, columns, values_list)

    def parse_update(self):
        self.eat('UPDATE')  # UPDATE
        table = self.eat('IDENT').value
        self.eat('SET')  # SET
        assignments = {}
        while True:
            col = self.eat('IDENT').value
            self.eat('OP')  # =
            tok = self.eat()
            if tok.type == 'NUMBER':
                val = float(tok.value) if '.' in tok.value else int(tok.value)
            elif tok.type == 'STRING':
                val = tok.value.strip("'")
            else:
                val = tok.value
            assignments[col] = Value(val)
            if self.current() and self.current().type == 'COMMA':
                self.eat('COMMA')
            else:
                break
        where = None
        if self.current() and self.current().type == 'WHERE':
            self.eat('WHERE')
            where = self.parse_condition()
        return UpdateStatement(table, assignments, where)

    def parse_delete(self):
        self.eat('DELETE')  # DELETE
        self.eat('FROM')  # FROM
        table = self.eat('IDENT').value
        where = None
        if self.current() and self.current().type == 'WHERE':
            self.eat('WHERE')
            where = self.parse_condition()
        return DeleteStatement(table, where)

    def parse_create_table(self):
        self.eat('CREATE')  # CREATE
        self.eat('TABLE')  # TABLE
        table = self.eat('IDENT').value
        self.eat('LPAREN')
        columns = []
        while True:
            name = self.eat('IDENT').value
            col_type = None
            constraints = []
            # 解析类型（如 INT、TEXT、CHAR(50)、REAL）
            if self.current() and (self.current().type == 'IDENT' or self.current().type == 'OP'):
                # 支持如 CHAR(50)
                col_type = self.eat().value
                if col_type.upper() == 'CHAR' and self.current() and self.current().type == 'LPAREN':
                    self.eat('LPAREN')
                    size = self.eat('NUMBER').value
                    col_type += f'({size})'
                    self.eat('RPAREN')
            # 解析约束（如 PRIMARY KEY, NOT NULL），直到遇到逗号或右括号
            while self.current() and self.current().type == 'IDENT':
                word = self.eat('IDENT').value.upper()
                if word in ('PRIMARY', 'NOT') and self.current() and self.current().type == 'IDENT':
                    next_word = self.eat('IDENT').value.upper()
                    constraints.append(f'{word} {next_word}')
                else:
                    constraints.append(word)
            columns.append(TableColumn(name, col_type, constraints))
            if self.current() and self.current().type == 'COMMA':
                self.eat('COMMA')
                continue
            elif self.current() and self.current().type == 'RPAREN':
                break
            else:
                raise RuntimeError(f'Expected COMMA or RPAREN, got {self.current().type if self.current() else None}')
        self.eat('RPAREN')
        return CreateTableStatement(table, columns)

    def parse_drop_table(self):
        self.eat('DROP')  # DROP
        self.eat('TABLE')  # TABLE
        table = self.eat('IDENT').value
        return DropTableStatement(table) 