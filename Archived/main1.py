import os
import sys
from lexer import tokenize
from parser import Parser
from executor import execute

def ast_to_python(ast):
    from ast_nodes import CreateTableStatement, TableColumn, InsertStatement, SelectStatement, UpdateStatement, DeleteStatement, DropTableStatement, Column, BinaryOp, LogicOp, Value, IntersectStatement, ExceptStatement, UnionStatement
    lines = []
    def get_output_columns_py(rows, ast):
        if hasattr(ast, 'columns') and len(ast.columns) == 1 and ast.columns[0].name == '*':
            if rows:
                return list(rows[0].keys())
            else:
                return []
        else:
            return [col.name for col in getattr(ast, 'columns', [])]
    def row_key_py(row, columns):
        return tuple(row.get(col) for col in columns)
    if isinstance(ast, CreateTableStatement):
        # CREATE TABLE
        col_defs = []
        for col in ast.columns:
            desc = col.name
            if col.col_type:
                desc += f': {col.col_type}'
            if col.constraints:
                desc += ' [' + ', '.join(col.constraints) + ']'
            col_defs.append(desc)
        lines.append(f"tables['{ast.table}'] = []  # {', '.join(col_defs)}")
    elif isinstance(ast, DropTableStatement):
        # DROP TABLE
        lines.append(f"if '{ast.table}' in tables:")
        lines.append(f"    del tables['{ast.table}']")
        lines.append(f"    # 可选：同步删除表结构")
        lines.append(f"    if '_schemas' in tables and '{ast.table}' in tables['_schemas']:")
        lines.append(f"        del tables['_schemas']['{ast.table}']")
    elif isinstance(ast, InsertStatement):
        # INSERT INTO
        for values in ast.values:
            row_items = []
            for col, val in zip(ast.columns, values):
                v = repr(val.value) if hasattr(val, 'value') else repr(val)
                row_items.append(f"'{col}': {v}")
            lines.append(f"tables['{ast.table}'].append({{{', '.join(row_items)}}})")
    elif isinstance(ast, UpdateStatement):
        # UPDATE
        cond = expr_to_py(ast.where) if ast.where else 'True'
        assign = ', '.join([f"row['{col}'] = {repr(val.value)}" for col, val in ast.assignments.items()])
        lines.append(f"for row in tables['{ast.table}']:")
        lines.append(f"    if {cond}:")
        for col, val in ast.assignments.items():
            lines.append(f"        row['{col}'] = {repr(val.value)}")
    elif isinstance(ast, DeleteStatement):
        # DELETE
        cond = expr_to_py(ast.where) if ast.where else 'False'
        lines.append(f"tables['{ast.table}'] = [row for row in tables['{ast.table}'] if not ({cond})]")
    elif isinstance(ast, SelectStatement):
        # SELECT
        cond = expr_to_py(ast.where) if ast.where else 'True'
        if len(ast.columns) == 1 and ast.columns[0].name == '*':
            select_expr = 'row.copy()'
        else:
            select_expr = '{' + ', '.join([f"'{col.name}': row['{col.name}']" for col in ast.columns]) + '}'
        lines.append(f"result = [{select_expr} for row in tables['{ast.from_table}'] if {cond}]")
        # ORDER BY
        if ast.order_by:
            for col, direction in reversed(ast.order_by):
                reverse = 'True' if direction == 'DESC' else 'False'
                lines.append(f"result.sort(key=lambda r: r.get('{col}'), reverse={reverse})")
        # LIMIT
        if ast.limit is not None:
            lines.append(f"result = result[:{ast.limit}]")
        lines.append("print('查询结果:')")
        lines.append("for row in result:")
        lines.append("    print(row)")
    elif isinstance(ast, UnionStatement):
        # UNION/UNION ALL
        lines.append('# UNION/UNION ALL')
        lines.append('results = []')
        for sel in ast.selects:
            lines.append('sub_result = []')
            lines.append(ast_to_python(sel) if not isinstance(sel, str) else sel)
            lines.append('results.append(sub_result)')
        lines.append('all_rows = [row for r in results for row in r]')
        lines.append('columns = list(all_rows[0].keys()) if all_rows else []')
        if getattr(ast, 'all', False):
            lines.append('result = all_rows')
        else:
            lines.append('seen = set()')
            lines.append('result = []')
            lines.append('for row in all_rows:')
            lines.append('    k = tuple(row.get(col) for col in columns)')
            lines.append('    if k not in seen:')
            lines.append('        seen.add(k)')
            lines.append('        result.append(row)')
        lines.append("print('查询结果:')")
        lines.append('for row in result:')
        lines.append('    print(row)')
    elif isinstance(ast, IntersectStatement):
        # INTERSECT
        lines.append('# INTERSECT')
        lines.append('results = []')
        for sel in ast.selects:
            lines.append('sub_result = []')
            lines.append(ast_to_python(sel) if not isinstance(sel, str) else sel)
            lines.append('results.append(sub_result)')
        lines.append('if results:')
        lines.append('    columns = list(results[0][0].keys()) if results[0] else []')
        lines.append('    sets = [set(tuple(row.get(col) for col in columns) for row in r) for r in results]')
        lines.append('    common = set.intersection(*sets) if sets else set()')
        lines.append('    seen = set()')
        lines.append('    result = []')
        lines.append('    for row in results[0]:')
        lines.append('        k = tuple(row.get(col) for col in columns)')
        lines.append('        if k in common and k not in seen:')
        lines.append('            seen.add(k)')
        lines.append('            result.append(row)')
        lines.append('else:')
        lines.append('    result = []')
        lines.append("print('查询结果:')")
        lines.append('for row in result:')
        lines.append('    print(row)')
    elif isinstance(ast, ExceptStatement):
        # EXCEPT
        lines.append('# EXCEPT')
        lines.append('results = []')
        for sel in ast.selects:
            lines.append('sub_result = []')
            lines.append(ast_to_python(sel) if not isinstance(sel, str) else sel)
            lines.append('results.append(sub_result)')
        lines.append('if results:')
        lines.append('    columns = list(results[0][0].keys()) if results[0] else []')
        lines.append('    sets = [set(tuple(row.get(col) for col in columns) for row in r) for r in results]')
        lines.append('    base_keys = sets[0] if sets else set()')
        lines.append('    other_keys = set()')
        lines.append('    for s in sets[1:]:')
        lines.append('        other_keys |= s')
        lines.append('    diff_keys = base_keys - other_keys')
        lines.append('    key_to_row = {}')
        lines.append('    for row in results[0]:')
        lines.append('        k = tuple(row.get(col) for col in columns)')
        lines.append('        if k in diff_keys:')
        lines.append('            key_to_row[k] = row')
        lines.append('    result = list(key_to_row.values())')
        lines.append('else:')
        lines.append('    result = []')
        lines.append("print('查询结果:')")
        lines.append('for row in result:')
        lines.append('    print(row)')
    else:
        lines.append(f"# 不支持的SQL类型: {type(ast).__name__}")
    return '\n'.join(lines)

def expr_to_py(expr):
    from ast_nodes import Column, BinaryOp, LogicOp, Value
    if expr is None:
        return 'True'
    if isinstance(expr, BinaryOp):
        left = f"row['{expr.left.name}']" if isinstance(expr.left, Column) else repr(expr.left.value)
        right = repr(expr.right.value) if isinstance(expr.right, Value) else f"row['{expr.right.name}']"
        return f"({left} {expr.op} {right})"
    elif isinstance(expr, LogicOp):
        if expr.op == 'AND':
            return f"({expr_to_py(expr.left)} and {expr_to_py(expr.right)})"
        elif expr.op == 'OR':
            return f"({expr_to_py(expr.left)} or {expr_to_py(expr.right)})"
        elif expr.op == 'NOT':
            return f"(not {expr_to_py(expr.left)})"
    elif isinstance(expr, Column):
        return f"row['{expr.name}']"
    elif isinstance(expr, Value):
        return repr(expr.value)
    else:
        return 'True'  # fallback

if __name__ == '__main__':
    
    # 示例内存表
    tables = {
        'Students': [
            {'StudentID': 1, 'Name': '张三', 'Age': 20, 'City': '北京'},
            {'StudentID': 2, 'Name': '李四', 'Age': 22, 'City': '上海'},
            {'StudentID': 3, 'Name': '王五', 'Age': 21, 'City': '广州'},
            {'StudentID': 4, 'Name': '赵六', 'Age': 23, 'City': '北京'}, # 与张三城市重复
            {'StudentID': 5, 'Name': '钱七', 'Age': 19, 'City': '深圳'},
            {'StudentID': 6, 'Name': '李四', 'Age': 25, 'City': '上海'} # 与 StudentID=2 姓名重复
        ],
        'Teachers': [ # 新增一个 Teachers 表用于更好的测试
            {'TeacherID': 101, 'Name': '王老师', 'Subject': '数据库', 'City': '北京'},
            {'TeacherID': 102, 'Name': '李四', 'Subject': '操作系统', 'City': '广州'}, # 与学生姓名重复
            {'TeacherID': 103, 'Name': '张老师', 'Subject': '数据结构', 'City': '上海'}, # 与学生城市重复
            {'TeacherID': 104, 'Name': '赵老师', 'Subject': '算法设计', 'City': '天津'},
            {'TeacherID': 105, 'Name': '王老师', 'Subject': '计算机网络', 'City': '北京'} # 与 TeacherID=101 姓名和城市重复
        ],
        'Courses': [
            {'CourseID': 1001, 'CourseName': '数据库原理', 'Dept': 'CS'},
            {'CourseID': 1002, 'CourseName': '操作系统', 'Dept': 'CS'},
            {'CourseID': 1003, 'CourseName': '计算机网络', 'Dept': 'EE'},
            {'CourseID': 1004, 'CourseName': '数据结构', 'Dept': 'CS'},
            {'CourseID': 1005, 'CourseName': '算法设计', 'Dept': 'CS'},
            {'CourseID': 1006, 'CourseName': '机器学习', 'Dept': 'AI'}
        ]
    }
    # 测试用例：演示 INNER JOIN
    if False:  # 改为True可自动运行测试
        tables['Song'] = [
            {'id': 1, 'name': 'A', 'albumId': 10},
            {'id': 2, 'name': 'B', 'albumId': 20},
            {'id': 3, 'name': 'C', 'albumId': 10},
        ]
        tables['Album'] = [
            {'id': 10, 'title': 'Alpha'},
            {'id': 20, 'title': 'Beta'},
        ]
        sql = "SELECT * FROM Song JOIN Album ON Song.albumId = Album.id"
        tokens = tokenize(sql)
        parser = Parser(tokens)
        ast = parser.parse()
        result = execute(ast, tables)
        print('INNER JOIN 测试结果:')
        for row in result:
            print(row)
        sys.exit()
    
    mode = input('请选择输入模式：1. 交互输入  2. 文件输入  3. 文件翻译  [1/2/3]: ').strip()
    if mode == '2':
        file_path = input('请输入SQL文件路径: ').strip()
        if not os.path.isfile(file_path):
            print('\033[31m错误: 文件不存在\033[0m')
        else:
            with open(file_path, encoding='utf-8') as f:
                content = f.read()
            # 按分号分割，支持多条SQL
            stmts = [stmt.strip() for stmt in content.split(';') if stmt.strip()]
            for sql in stmts:
                try:
                    tokens = tokenize(sql)
                    parser = Parser(tokens)
                    ast = parser.parse()
                    result = execute(ast, tables)
                    print('执行结果:')
                    if isinstance(result, list):
                        for row in result:
                            print(row)
                    else:
                        print(result)
                except Exception as e:
                    print('\033[31m错误:', e, '\033[0m')
                print('当前所有表:')
                for tname, trows in tables.items():
                    print(f'表 {tname}:', trows)
    elif mode == '3':
        print('支持的SQL语法：CREATE TABLE、DROP TABLE、INSERT、SELECT、UPDATE、DELETE、WHERE、ORDER BY、LIMIT、复杂条件等')
        sql_path = input('请输入SQL文件路径: ').strip()
        if not os.path.isfile(sql_path):
            print('\033[31m错误: SQL文件不存在\033[0m')
        else:
            with open(sql_path, encoding='utf-8') as f:
                content = f.read()
            stmts = [stmt.strip() for stmt in content.split(';') if stmt.strip()]
            py_lines = ["tables = {}  # 初始化表字典\n"]
            for sql in stmts:
                try:
                    tokens = tokenize(sql)
                    parser = Parser(tokens)
                    ast = parser.parse()
                    py_code = ast_to_python(ast)
                    py_lines.append(py_code + '\n')
                except Exception as e:
                    py_lines.append(f"# 错误: {e}\n")
            base = os.path.splitext(os.path.basename(sql_path))[0]
            py_path = f"{base}.py"
            with open(py_path, 'w', encoding='utf-8') as f:
                f.writelines(py_lines)
            print(f'已将SQL文件翻译为Python文件: {py_path}')
    else:
        while True:
            print('请输入SQL语句（以分号 ; 结尾，支持多行）：')
            lines = []
            while True:
                line = input()
                if line.strip().endswith(';'):
                    lines.append(line)
                    break
                lines.append(line)
            sql = '\n'.join(lines).strip()
            if not sql:
                break
            if sql.endswith(';'):
                sql = sql[:-1]  # 去掉结尾分号
            try:
                tokens = tokenize(sql)
                parser = Parser(tokens)
                ast = parser.parse()
                result = execute(ast, tables)
                print('执行结果:')
                if isinstance(result, list):
                    for row in result:
                        print(row)
                else:
                    print(result)
            except Exception as e:
                print('\033[31m错误:', e, '\033[0m')
            print('当前所有表:')
            for tname, trows in tables.items():
                print(f'表 {tname}:', trows)

     