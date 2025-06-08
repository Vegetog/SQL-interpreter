from ast_nodes import SelectStatement, Column, BinaryOp, Value, InsertStatement, UpdateStatement, DeleteStatement, LogicOp, CreateTableStatement, DropTableStatement, UnionStatement, IntersectStatement, ExceptStatement

def execute(ast, tables):
    if isinstance(ast, SelectStatement):
        # 支持 INNER JOIN、LEFT JOIN、RIGHT JOIN、FULL JOIN、CROSS JOIN
        if ast.join:
            left_table = tables[ast.join.left_table]
            right_table = tables[ast.join.right_table]
            join_rows = []
            left_keys = set()
            right_keys = set()
            for lrow in left_table:
                for k in lrow:
                    left_keys.add(f'{ast.join.left_table}.{k}')
            for rrow in right_table:
                for k in rrow:
                    right_keys.add(f'{ast.join.right_table}.{k}')
            if ast.join.join_type == 'RIGHT':
                for rrow in right_table:
                    matched = False
                    for lrow in left_table:
                        merged = {}
                        for k, v in lrow.items():
                            merged[f'{ast.join.left_table}.{k}'] = v
                        for k, v in rrow.items():
                            merged[f'{ast.join.right_table}.{k}'] = v
                        if eval_condition(ast.join.on_expr, merged):
                            join_rows.append(merged)
                            matched = True
                    if not matched:
                        merged = {f'{ast.join.right_table}.{k}': v for k, v in rrow.items()}
                        for k in left_keys:
                            merged[k] = None
                        join_rows.append(merged)
            elif ast.join.join_type == 'FULL':
                matched_left = set()
                matched_right = set()
                # 先做INNER JOIN部分
                for lidx, lrow in enumerate(left_table):
                    for ridx, rrow in enumerate(right_table):
                        merged = {}
                        for k, v in lrow.items():
                            merged[f'{ast.join.left_table}.{k}'] = v
                        for k, v in rrow.items():
                            merged[f'{ast.join.right_table}.{k}'] = v
                        if eval_condition(ast.join.on_expr, merged):
                            join_rows.append(merged)
                            matched_left.add(lidx)
                            matched_right.add(ridx)
                # 补左表未匹配
                for lidx, lrow in enumerate(left_table):
                    if lidx not in matched_left:
                        merged = {f'{ast.join.left_table}.{k}': v for k, v in lrow.items()}
                        for k in right_keys:
                            merged[k] = None
                        join_rows.append(merged)
                # 补右表未匹配
                for ridx, rrow in enumerate(right_table):
                    if ridx not in matched_right:
                        merged = {f'{ast.join.right_table}.{k}': v for k, v in rrow.items()}
                        for k in left_keys:
                            merged[k] = None
                        join_rows.append(merged)
            elif ast.join.join_type == 'CROSS':
                for lrow in left_table:
                    for rrow in right_table:
                        merged = {}
                        for k, v in lrow.items():
                            merged[f'{ast.join.left_table}.{k}'] = v
                        for k, v in rrow.items():
                            merged[f'{ast.join.right_table}.{k}'] = v
                        join_rows.append(merged)
            else:
                for lrow in left_table:
                    matched = False
                    for rrow in right_table:
                        merged = {}
                        for k, v in lrow.items():
                            merged[f'{ast.join.left_table}.{k}'] = v
                        for k, v in rrow.items():
                            merged[f'{ast.join.right_table}.{k}'] = v
                        if eval_condition(ast.join.on_expr, merged):
                            join_rows.append(merged)
                            matched = True
                    if ast.join.join_type == 'LEFT' and not matched:
                        merged = {f'{ast.join.left_table}.{k}': v for k, v in lrow.items()}
                        for k in right_keys:
                            merged[k] = None
                        join_rows.append(merged)
            table = join_rows
        else:
            table = tables[ast.from_table]
        result = []
        if len(ast.columns) == 1 and ast.columns[0].name == '*':
            # SELECT *，返回所有列
            for row in table:
                if ast.where:
                    if not eval_condition(ast.where, row):
                        continue
                result.append(row.copy())
        else:
            for row in table:
                if ast.where:
                    if not eval_condition(ast.where, row):
                        continue
                result.append({col.name: row.get(col.name) for col in ast.columns})
        # ORDER BY 排序
        if ast.order_by:
            for col, direction in reversed(ast.order_by):
                reverse = (direction == 'DESC')
                result.sort(key=lambda r: tuple(sql_sort_key(r.get(col)) for col, _ in ast.order_by), reverse=reverse)
        # LIMIT 截断
        if ast.limit is not None:
            result = result[:ast.limit]
        return result
    elif isinstance(ast, InsertStatement):
        table = tables[ast.table]
        inserted = 0
        for values in ast.values:
            row = {}
            for col, val in zip(ast.columns, values):
                row[col] = val.value
            check_constraints(ast.table, row, tables)
            table.append(row)
            inserted += 1
        return f'插入成功: {inserted} 行'
    elif isinstance(ast, UpdateStatement):
        table = tables[ast.table]
        count = 0
        for row in table:
            if ast.where:
                if not eval_condition(ast.where, row):
                    continue
            # 先构造更新后的新行用于检查
            new_row = row.copy()
            for col, val in ast.assignments.items():
                new_row[col] = val.value
            check_constraints(ast.table, new_row, tables, updating_row=row)
            # 检查通过后再更新
            for col, val in ast.assignments.items():
                row[col] = val.value
            count += 1
        return f'更新行数: {count}'
    elif isinstance(ast, DeleteStatement):
        table = tables[ast.table]
        to_delete = []
        for row in table:
            if ast.where:
                if not eval_condition(ast.where, row):
                    continue
            to_delete.append(row)
        for row in to_delete:
            table.remove(row)
        return f'删除行数: {len(to_delete)}'
    elif isinstance(ast, CreateTableStatement):
        if ast.table in tables:
            return f'表 {ast.table} 已存在'
        tables[ast.table] = []
        # 记录表结构
        if '_schemas' not in tables:
            tables['_schemas'] = {}
        tables['_schemas'][ast.table] = [(col.name, col.col_type, col.constraints) for col in ast.columns]
        return f'创建表成功: {ast.table}，字段: {[f"{col.name} {col.col_type or ''} {' '.join(col.constraints)}".strip() for col in ast.columns]}'
    elif isinstance(ast, DropTableStatement):
        if ast.table in tables:
            del tables[ast.table]
            # 同时删除表结构
            if '_schemas' in tables and ast.table in tables['_schemas']:
                del tables['_schemas'][ast.table]
            return f'已删除表: {ast.table}'
        else:
            return f'表 {ast.table} 不存在'
    elif isinstance(ast, UnionStatement):
        all_rows = []
        for sel in ast.selects:
            rows = execute(sel, tables)
            all_rows.extend(rows)
        # 用输出列做 key
        columns = get_output_columns(all_rows, ast.selects[0]) if all_rows else []
        if ast.all:
            return all_rows
        seen = set()
        result = []
        for row in all_rows:
            key = row_key(row, columns)
            if key not in seen:
                seen.add(key)
                result.append(row)
        return result
    elif isinstance(ast, IntersectStatement):
        # 依次执行每个 SELECT，取交集
        result_sets = []
        all_rows = []
        for sel in ast.selects:
            rows = execute(sel, tables)
            all_rows.append(rows)
        columns = get_output_columns(all_rows[0], ast.selects[0]) if all_rows and all_rows[0] else []
        for rows in all_rows:
            row_keys = set(row_key(row, columns) for row in rows)
            result_sets.append((row_keys, rows))
        if not result_sets:
            return []
        common_keys = set.intersection(*(rk for rk, _ in result_sets))
        seen = set()
        result = []
        for row in result_sets[0][1]:
            k = row_key(row, columns)
            if k in common_keys and k not in seen:
                seen.add(k)
                result.append(row)
        return result
    elif isinstance(ast, ExceptStatement):
        # 只用输出列做 key
        result_sets = []
        all_rows = []
        for sel in ast.selects:
            rows = execute(sel, tables)
            all_rows.append(rows)
        columns = get_output_columns(all_rows[0], ast.selects[0]) if all_rows and all_rows[0] else []
        for rows in all_rows:
            keys = set(row_key(row, columns) for row in rows)
            result_sets.append((keys, rows))
        if not result_sets:
            return []
        base_keys = result_sets[0][0]
        other_keys = set()
        for rk, _ in result_sets[1:]:
            other_keys |= rk
        diff_keys = base_keys - other_keys
        key_to_row = {}
        with open('except_debug.log', 'a', encoding='utf-8') as f:
            f.write('---[EXCEPT 调试]---\n')
            f.write(f'columns: {columns}\n')
            f.write(f'base_keys: {base_keys}\n')
            f.write(f'other_keys: {other_keys}\n')
            f.write(f'diff_keys: {diff_keys}\n')
        for row in result_sets[0][1]:
            k = row_key(row, columns)
            with open('except_debug.log', 'a', encoding='utf-8') as f:
                f.write(f'row: {row} key: {k}\n')
            if k in diff_keys:
                key_to_row[k] = row
        with open('except_debug.log', 'a', encoding='utf-8') as f:
            f.write(f'最终输出: {list(key_to_row.values())}\n')
            f.write('---[END EXCEPT 调试]---\n')
        return list(key_to_row.values())
    else:
        raise NotImplementedError('只支持SelectStatement, InsertStatement, UpdateStatement, DeleteStatement, CreateTableStatement, DropTableStatement, UnionStatement, IntersectStatement, ExceptStatement')

def eval_condition(cond, row):
    if isinstance(cond, BinaryOp):
        left = row.get(cond.left.name) if isinstance(cond.left, Column) else cond.left.value
        right = cond.right.value if isinstance(cond.right, Value) else row.get(cond.right.name)
        if cond.op == '=':
            return left == right
        elif cond.op == '>':
            return left > right
        elif cond.op == '<':
            return left < right
        elif cond.op == '>=':
            return left >= right
        elif cond.op == '<=':
            return left <= right
        elif cond.op in ('!=', '<>'):
            return left != right
        else:
            raise NotImplementedError(f'不支持的操作符: {cond.op}')
    elif isinstance(cond, LogicOp):
        if cond.op == 'AND':
            return eval_condition(cond.left, row) and eval_condition(cond.right, row)
        elif cond.op == 'OR':
            return eval_condition(cond.left, row) or eval_condition(cond.right, row)
        elif cond.op == 'NOT':
            return not eval_condition(cond.left, row)
        else:
            raise NotImplementedError(f'不支持的逻辑操作符: {cond.op}')
    else:
        raise NotImplementedError('只支持简单二元条件和逻辑运算')

def check_constraints(table, row, tables, updating_row=None):
    print(f"[调试] check_constraints 调用: 表={table}, 行={row}")
    schema = tables.get('_schemas', {}).get(table)
    if not schema:
        print(f"[调试] 未找到表结构: {table}")
        return  # 没有表结构信息，跳过检查
    # 找出主键字段
    pk_cols = [col_name for col_name, _, constraints in schema if 'PRIMARY KEY' in constraints]
    for col_name, col_type, constraints in schema:
        val = row.get(col_name)
        print(f"[调试] 字段={col_name}, 类型={col_type}, 约束={constraints}, 当前值={val}")
        # NOT NULL 检查
        if 'NOT NULL' in constraints and (val is None):
            print(f"[调试] 触发 NOT NULL 检查: {col_name}")
            raise RuntimeError(f'NOT NULL constraint failed: {col_name}')
        # PRIMARY KEY 不能为 NULL
        if 'PRIMARY KEY' in constraints and (val is None):
            print(f"[调试] 触发 PRIMARY KEY NULL 检查: {col_name}")
            raise RuntimeError('PRIMARY KEY constraint failed')
        # 只有不是 None 时才做类型检查
        if val is not None and col_type:
            if col_type.startswith('INT') and not (isinstance(val, int) and not isinstance(val, bool)):
                print(f"[调试] 触发类型检查: {col_name} 应为整数")
                raise RuntimeError(f'字段 {col_name} 必须为整数')
            if col_type.startswith('CHAR') or col_type == 'TEXT':
                if not isinstance(val, str):
                    print(f"[调试] 触发类型检查: {col_name} 应为字符串")
                    raise RuntimeError(f'字段 {col_name} 必须为字符串')
                if col_type.startswith('CHAR'):
                    maxlen = int(col_type[col_type.find('(')+1:col_type.find(')')])
                    if len(val) > maxlen:
                        print(f"[调试] 触发长度检查: {col_name} 长度超限")
                        raise RuntimeError(f'字段 {col_name} 长度不能超过 {maxlen}')
            if col_type == 'REAL' and not (isinstance(val, float) or isinstance(val, int)):
                print(f"[调试] 触发类型检查: {col_name} 应为实数")
                raise RuntimeError(f'字段 {col_name} 必须为实数')
    # 主键唯一性检查（只支持单主键）
    if pk_cols:
        pk_col = pk_cols[0]
        pk_val = row.get(pk_col)
        for r in tables[table]:
            if updating_row is not None and r is updating_row:
                continue  # 跳过自身
            if r.get(pk_col) == pk_val:
                print(f"[调试] 触发主键唯一性检查: {pk_col}={pk_val}")
                raise RuntimeError(f'主键字段 {pk_col} 的值 {pk_val} 已存在，必须唯一')

def get_output_columns(rows, ast):
    # 递归处理复合查询节点
    if hasattr(ast, 'selects') and ast.selects:
        return get_output_columns(rows, ast.selects[0])
    if hasattr(ast, 'columns'):
        if len(ast.columns) == 1 and ast.columns[0].name == '*':
            if rows:
                return list(rows[0].keys())
            else:
                return []
        else:
            return [col.name for col in ast.columns]
    else:
        raise RuntimeError('AST节点没有columns属性')

def row_key(row, columns):
    return tuple(row.get(col) for col in columns)

def sql_sort_key(val):
    return (val is None, val)
