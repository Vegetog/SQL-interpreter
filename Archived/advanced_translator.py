"""
高级SQL翻译器
支持更复杂的SQL语法和多表操作
"""

import re
import json
import os
from typing import Dict, List, Any, Union, Optional, Tuple

class AdvancedSQLTranslator:
    def __init__(self):
        # 存储所有表的数据结构
        self.tables = {}
        # 存储创建的表格的结构
        self.table_schemas = {}
        # 存储所有表的外键关系
        self.foreign_keys = {}

    def translate_file(self, sql_file_path: str, output_file_path: str = None) -> str:
        """
        翻译SQL文件中的所有语句
        """
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
            
        # 按语句分割SQL
        sql_statements = self._split_sql_statements(sql_content)
        
        # 翻译每条语句
        python_code = [
            "# 自动生成的Python代码 - 由SQL翻译器生成",
            "# 原始SQL文件: " + os.path.basename(sql_file_path),
            "",
            "# 初始化数据结构",
            ""
        ]
        
        for stmt in sql_statements:
            if stmt.strip():
                python_code.append("# " + "-" * 50)
                for line in stmt.splitlines():
                    python_code.append(f"# {line}")
                python_code.append(self.translate(stmt))
        
        result = "\n".join(python_code)
        
        # 保存到文件
        if output_file_path:
            with open(output_file_path, 'w', encoding='utf-8') as out_file:
                out_file.write(result)
                
        return result
    
    def _split_sql_statements(self, sql_content: str) -> List[str]:
        """
        分割SQL语句，处理注释和引号内的分号
        """
        # 移除SQL注释
        sql_content = re.sub(r'--.*?(\n|$)', '\n', sql_content)
        sql_content = re.sub(r'/\*.*?\*/', '', sql_content, flags=re.DOTALL)
        
        statements = []
        current_stmt = ""
        in_quotes = False
        quote_char = None
        
        for char in sql_content:
            if char in ("'", '"') and (quote_char is None or char == quote_char):
                in_quotes = not in_quotes
                if in_quotes:
                    quote_char = char
                else:
                    quote_char = None
                current_stmt += char
            elif char == ';' and not in_quotes:
                statements.append(current_stmt.strip())
                current_stmt = ""
            else:
                current_stmt += char
        
        # 添加最后一个语句（如果没有以分号结尾）
        if current_stmt.strip():
            statements.append(current_stmt.strip())
            
        return statements
        
    def translate(self, sql: str) -> str:
        """
        将SQL语句翻译为Python代码
        """
        sql = sql.strip()
        
        # 移除SQL语句中的注释
        sql = re.sub(r'--.*?(\n|$)', '', sql)
        sql = re.sub(r'/\*.*?\*/', '', sql, flags=re.DOTALL)
        
        # 规范化SQL语句，忽略大小写
        sql = sql.strip().rstrip(';')
        
        # 判断SQL语句类型并调用相应的处理函数
        if re.search(r'^\s*CREATE\s+TABLE', sql, re.IGNORECASE):
            return self._translate_create_table(sql)
        elif re.search(r'^\s*INSERT\s+INTO', sql, re.IGNORECASE):
            return self._translate_insert(sql)
        elif re.search(r'^\s*DELETE\s+FROM', sql, re.IGNORECASE):
            return self._translate_delete(sql)
        elif re.search(r'^\s*SELECT', sql, re.IGNORECASE):
            return self._translate_select(sql)
        elif re.search(r'^\s*UPDATE', sql, re.IGNORECASE):
            return self._translate_update(sql)
        else:
            return f"print('不支持的SQL语句类型: {sql}')"
    
    def _translate_create_table(self, sql: str) -> str:
        """
        翻译CREATE TABLE语句
        """
        # 解析表名
        table_match = re.search(r'CREATE\s+TABLE\s+(\w+)', sql, re.IGNORECASE)
        if not table_match:
            return "# 无法解析表名"
            
        table_name = table_match.group(1)
        
        # 提取列定义
        columns_match = re.search(r'\(\s*(.*)\s*\)', sql, re.IGNORECASE | re.DOTALL)
        if not columns_match:
            return "# 无法解析列定义"
        columns_text = columns_match.group(1)

        # 健壮分割列定义（考虑嵌套括号）
        column_defs = []
        paren_level = 0
        current_col = ""
        for char in columns_text:
            if char == '(': 
                paren_level += 1
                current_col += char
            elif char == ')':
                paren_level -= 1
                current_col += char
            elif char == ',' and paren_level == 0:
                column_defs.append(current_col.strip())
                current_col = ""
            else:
                current_col += char
        if current_col.strip():
            column_defs.append(current_col.strip())

        # 解析每个列的名称和类型
        schema = {}
        foreign_keys = {}
        for column in column_defs:
            # 处理表级约束
            if re.search(r'^\s*(?:CONSTRAINT\s+\w+\s+)?FOREIGN\s+KEY', column, re.IGNORECASE):
                fk_match = re.search(r'FOREIGN\s+KEY\s*\(([^)]+)\)\s*REFERENCES\s+(\w+)\s*\(([^)]+)\)', column, re.IGNORECASE)
                if fk_match:
                    local_col = fk_match.group(1).strip()
                    ref_table = fk_match.group(2).strip()
                    ref_col = fk_match.group(3).strip()
                    if table_name not in foreign_keys:
                        foreign_keys[table_name] = []
                    foreign_keys[table_name].append({
                        'local_column': local_col,
                        'ref_table': ref_table,
                        'ref_column': ref_col
                    })
                continue
            elif re.search(r'^\s*(PRIMARY|UNIQUE|CHECK|CONSTRAINT)', column, re.IGNORECASE):
                continue
            # 处理列定义
            col_parts = column.strip().split()
            if len(col_parts) < 2:
                continue
            col_name = col_parts[0]
            col_type = col_parts[1]
            # 检查列级外键
            fk_match = re.search(r'REFERENCES\s+(\w+)\s*\(([^)]+)\)', column, re.IGNORECASE)
            if fk_match:
                ref_table = fk_match.group(1).strip()
                ref_col = fk_match.group(2).strip()
                if table_name not in foreign_keys:
                    foreign_keys[table_name] = []
                foreign_keys[table_name].append({
                    'local_column': col_name,
                    'ref_table': ref_table,
                    'ref_column': ref_col
                })
            # 规范化数据类型
            if re.search(r'INT|INTEGER|BIGINT|SMALLINT', col_type, re.IGNORECASE):
                py_type = 'int'
            elif re.search(r'FLOAT|DOUBLE|REAL|NUMERIC|DECIMAL', col_type, re.IGNORECASE):
                py_type = 'float'
            elif re.search(r'CHAR|VARCHAR|TEXT|STRING', col_type, re.IGNORECASE):
                py_type = 'str'
            elif re.search(r'BOOL|BOOLEAN', col_type, re.IGNORECASE):
                py_type = 'bool'
            elif re.search(r'DATE|TIME|DATETIME', col_type, re.IGNORECASE):
                py_type = 'str'  # 日期时间类型以字符串形式存储
            else:
                py_type = 'str'  # 默认为字符串类型
            schema[col_name] = py_type
        
        # 保存表结构和外键关系
        self.table_schemas[table_name] = schema
        if foreign_keys:
            self.foreign_keys.update(foreign_keys)
        
        # 生成Python代码
        code = [
            f"# 创建表: {table_name}",
            f"{table_name} = []  # 每次建表自动清空表数据",
            f"{table_name}_schema = {json.dumps(schema, indent=4)}",
            ""
        ]
        
        if table_name in foreign_keys:
            code.append(f"# 定义外键关系")
            code.append(f"{table_name}_foreign_keys = {json.dumps(foreign_keys[table_name], indent=4)}")
            code.append("")
        
        return "\n".join(code)
    
    def _translate_insert(self, sql: str) -> str:
        """
        翻译INSERT INTO语句
        """
        # 解析表名
        table_match = re.search(r'INSERT\s+INTO\s+(\w+)', sql, re.IGNORECASE)
        if not table_match:
            return "# 无法解析表名"
            
        table_name = table_match.group(1)
        
        # 解析列名
        column_pattern = r'INSERT\s+INTO\s+\w+\s*\(([^)]+)\)'
        column_match = re.search(column_pattern, sql, re.IGNORECASE)
        
        columns = []
        if column_match:
            columns = [col.strip() for col in column_match.group(1).split(',')]
        elif table_name in self.table_schemas:
            columns = list(self.table_schemas[table_name].keys())
            
        # 解析值
        values_pattern = r'VALUES\s*\(([^)]+)\)'
        values_match = re.search(values_pattern, sql, re.IGNORECASE)
        
        if not values_match:
            return "# 无法解析VALUES子句"
            
        # 处理值列表
        values_str = values_match.group(1)
        values = []
        
        # 解析值，考虑引号内的逗号
        value = ""
        in_quotes = False
        quote_char = None
        
        for char in values_str:
            if char in ("'", '"') and (quote_char is None or char == quote_char):
                in_quotes = not in_quotes
                if in_quotes:
                    quote_char = char
                else:
                    quote_char = None
                value += char
            elif char == ',' and not in_quotes:
                values.append(value.strip())
                value = ""
            else:
                value += char
                
        if value:
            values.append(value.strip())
        
        # 根据表结构做类型转换
        row_dict = {}
        schema = self.table_schemas.get(table_name, {})
        for col, val in zip(columns, values):
            col_type = schema.get(col, 'str')
            # 先去除外层引号
            if (val.startswith("'") and val.endswith("'")) or (val.startswith('"') and val.endswith('"')):
                val = val[1:-1]
            if val.upper() == 'NULL':
                row_dict[col] = None
            elif col_type == 'int':
                row_dict[col] = int(val)
            elif col_type == 'float':
                row_dict[col] = float(val)
            elif col_type == 'bool':
                row_dict[col] = val.upper() in ('TRUE', '1')
            else:
                row_dict[col] = val
        
        # 插入调试
        print('插入调试:', col, val, col_type)
        
        # 生成Python代码（用Python字面量格式，保证类型）
        def py_literal(val):
            if val is None:
                return 'None'
            elif isinstance(val, str):
                return repr(val)
            else:
                return str(val)
        row_items = [f"{repr(k)}: {py_literal(v)}" for k, v in row_dict.items()]
        code = [
            f"# 向表 {table_name} 插入一条记录",
            f"new_row = {{{', '.join(row_items)}}}",
            f"{table_name}.append(new_row)",
            ""
        ]
        
        # 检查外键约束
        if table_name in self.foreign_keys:
            code.append("# 验证外键约束")
            for fk in self.foreign_keys[table_name]:
                local_col = fk['local_column']
                ref_table = fk['ref_table']
                ref_col = fk['ref_column']
                code.append(f"# 检查 {local_col} 是否存在于 {ref_table}.{ref_col} 中")
                code.append(f"# 这里只是注释，实际项目中可以实现外键约束检查")
            code.append("")
        
        return "\n".join(code)
    
    def _translate_delete(self, sql: str) -> str:
        """
        翻译DELETE FROM语句
        """
        # 解析表名
        table_match = re.search(r'DELETE\s+FROM\s+(\w+)', sql, re.IGNORECASE)
        if not table_match:
            return "# 无法解析表名"
            
        table_name = table_match.group(1)
        
        # 解析WHERE子句
        where_match = re.search(r'WHERE\s+(.*?)(?:$|;)', sql, re.IGNORECASE | re.DOTALL)
        
        if not where_match:
            # 删除所有记录
            code = [
                f"# 删除表 {table_name} 中的所有记录",
                f"{table_name}.clear()",
                ""
            ]
        else:
            # 解析条件
            condition = where_match.group(1).strip()
            python_condition = self._translate_condition(condition)
            
            code = [
                f"# 删除表 {table_name} 中满足条件的记录",
                f"{table_name} = [row for row in {table_name} if not ({python_condition})]",
                ""
            ]
        
        return "\n".join(code)
    
    def _translate_select(self, sql: str) -> str:
        """
        翻译SELECT语句
        """
        # 解析选择的列
        select_pattern = r'SELECT\s+(.*?)\s+FROM'
        select_match = re.search(select_pattern, sql, re.IGNORECASE | re.DOTALL)
        
        if not select_match:
            return "# 无法解析SELECT语句"
            
        select_items = select_match.group(1).strip()
        
        # 处理 SELECT *
        all_columns = select_items == '*'
        
        if not all_columns:
            # 分割列，但考虑函数调用和别名
            columns = []
            current = ""
            depth = 0
            in_quotes = False
            quote_char = None
            
            for char in select_items:
                if char in ("'", '"') and (quote_char is None or char == quote_char):
                    in_quotes = not in_quotes
                    if in_quotes:
                        quote_char = char
                    else:
                        quote_char = None
                    current += char
                elif char == '(':
                    depth += 1
                    current += char
                elif char == ')':
                    depth -= 1
                    current += char
                elif char == ',' and depth == 0 and not in_quotes:
                    columns.append(current.strip())
                    current = ""
                else:
                    current += char
                    
            if current.strip():
                columns.append(current.strip())
        
        # 解析FROM子句
        tables_info = self._parse_from_clause(sql)
        if not tables_info:
            return "# 无法解析FROM子句"
            
        main_table = tables_info[0]['name']
        join_conditions = []
        
        # 处理JOIN
        for i in range(1, len(tables_info)):
            join_info = tables_info[i]
            if 'condition' in join_info:
                join_conditions.append(join_info['condition'])
        
        # 解析WHERE子句
        where_pattern = r'WHERE\s+(.*?)(?:$|;|ORDER\s+BY|GROUP\s+BY|HAVING|LIMIT)'
        where_match = re.search(where_pattern, sql, re.IGNORECASE | re.DOTALL)
        
        filter_condition = "True"  # 默认不过滤
        if where_match:
            condition = where_match.group(1).strip()
            filter_condition = self._translate_condition(condition)
        
        # 生成查询代码
        code = [
            f"# 从表 {', '.join([t['name'] for t in tables_info])} 中查询数据"
        ]
        # 多表JOIN处理
        if len(tables_info) > 1:
            alias_map = {}
            for t in tables_info:
                alias = t.get('alias') or t['name']
                alias_map[alias] = t['name']
            indent = ""
            # 嵌套for循环和JOIN条件
            for idx, t in enumerate(tables_info):
                alias = t.get('alias') or t['name']
                code.append(f"{indent}for row_{alias} in {alias_map[alias]}:")
                indent += "    "
                if idx > 0 and 'condition' in t:
                    cond = t['condition']
                    cond = re.sub(r'(\b\w+)\.(\w+)', r"row_\1['\2']", cond)
                    cond = re.sub(r'(?<![<>=!])=(?!=)', '==', cond)
                    code.append(f"{indent}if {cond}:")
                    indent += "    "
            # WHERE条件
            if where_match:
                where_cond = where_match.group(1).strip()
                where_cond = re.sub(r'(\b\w+)\.(\w+)', r"row_\1['\2']", where_cond)
                where_cond = re.sub(r'(?<![<>=!])=(?!=)', '==', where_cond)
                code.append(f"{indent}if {where_cond}:")
                indent += "    "
            # 结果投影
            if not all_columns:
                projection = []
                for col in columns:
                    if '.' in col:
                        alias, field = col.split('.', 1)
                        projection.append(f"'{field}': row_{alias}['{field}']")
                    else:
                        projection.append(f"'{col}': row_{col}['{col}']")
                code.append(f"{indent}joined_row = {{{', '.join(projection)}}}")
                code.append(f"{indent}result.append(joined_row)")
            else:
                joined_row = ', '.join([f"'{alias}': row_{alias}" for alias in alias_map])
                code.append(f"{indent}joined_row = {{{joined_row}}}")
                code.append(f"{indent}result.append(joined_row)")
        else:
            # 单表查询
            code.append(f"result = {main_table}.copy()")
            if where_match:
                code.append(f"result = [row for row in result if {filter_condition}]")
            # 处理列选择
            if not all_columns:
                projection_code = []
                for col in columns:
                    # 处理列别名
                    alias_match = re.search(r'(.*?)\s+[aA][sS]\s+(\w+)$', col)
                    if alias_match:
                        col_expr = alias_match.group(1).strip()
                        col_alias = alias_match.group(2).strip()
                        projection_code.append(f"'{col_alias}': row['{col_expr}']")
                    else:
                        projection_code.append(f"'{col}': row['{col}']")
                code.append(f"result = [{{" + ", ".join(projection_code) + f"}} for row in result]")
        code.append(f"print(result)")
        code.append("")
        return "\n".join(code)
    
    def _parse_from_clause(self, sql: str) -> List[Dict[str, str]]:
        """
        解析FROM子句，包括表名和JOIN条件
        """
        # 匹配FROM子句
        from_pattern = r'FROM\s+(.*?)(?:WHERE|ORDER\s+BY|GROUP\s+BY|HAVING|LIMIT|$)'
        from_match = re.search(from_pattern, sql, re.IGNORECASE | re.DOTALL)
        if not from_match:
            return []
        from_clause = from_match.group(1).strip()
        # 检查是否有JOIN
        has_join = bool(re.search(r'\bJOIN\b', from_clause, re.IGNORECASE))
        if not has_join:
            # 简单的FROM子句，可能有别名
            parts = from_clause.split()
            if len(parts) == 1:
                return [{'name': parts[0]}]
            elif len(parts) >= 3 and parts[1].upper() == 'AS':
                return [{'name': parts[0], 'alias': parts[2]}]
            elif len(parts) >= 2:
                return [{'name': parts[0], 'alias': parts[1]}]
            else:
                return []
        else:
            # 处理JOIN链
            result = []
            # 提取第一个表
            main_table_match = re.match(r'^(\w+)(?:\s+(?:AS\s+)?(\w+))?', from_clause, re.IGNORECASE)
            if main_table_match:
                table_name = main_table_match.group(1)
                alias = main_table_match.group(2) if main_table_match.group(2) else None
                result.append({'name': table_name, 'alias': alias} if alias else {'name': table_name})
            # 提取JOIN链
            join_pattern = r'(JOIN)\s+(\w+)(?:\s+(?:AS\s+)?(\w+))?\s+ON\s+([^J]*?)(?=\bJOIN\b|$)'
            for join_match in re.finditer(join_pattern, from_clause, re.IGNORECASE | re.DOTALL):
                table_name = join_match.group(2)
                alias = join_match.group(3) if join_match.group(3) else None
                condition = join_match.group(4).strip()
                join_info = {'name': table_name, 'condition': condition}
                if alias:
                    join_info['alias'] = alias
                result.append(join_info)
            return result
    
    def _translate_update(self, sql: str) -> str:
        """
        翻译UPDATE语句
        """
        # 解析表名
        table_match = re.search(r'UPDATE\s+(\w+)', sql, re.IGNORECASE)
        if not table_match:
            return "# 无法解析表名"
            
        table_name = table_match.group(1)
        
        # 解析SET子句
        set_pattern = r'SET\s+(.*?)(?:WHERE|$)'
        set_match = re.search(set_pattern, sql, re.IGNORECASE | re.DOTALL)
        
        if not set_match:
            return "# 无法解析SET子句"
            
        set_clause = set_match.group(1).strip()
        
        # 分割每个赋值语句
        assignments = []
        current = ""
        in_quotes = False
        quote_char = None
        
        for char in set_clause:
            if char in ("'", '"') and (quote_char is None or char == quote_char):
                in_quotes = not in_quotes
                if in_quotes:
                    quote_char = char
                else:
                    quote_char = None
                current += char
            elif char == ',' and not in_quotes:
                assignments.append(current.strip())
                current = ""
            else:
                current += char
                
        if current.strip():
            assignments.append(current.strip())
        
        # 解析每个赋值语句
        py_assignments = {}
        for assignment in assignments:
            parts = assignment.split('=', 1)
            if len(parts) == 2:
                col_name = parts[0].strip()
                value = parts[1].strip()
                
                # 处理值的Python表示
                if value.upper() == 'NULL':
                    py_value = "None"
                elif value.startswith(("'", '"')) and value.endswith(("'", '"')):
                    py_value = value
                elif value.replace('.', '', 1).isdigit():
                    py_value = value
                else:
                    py_value = f"'{value}'"
                    
                py_assignments[col_name] = py_value
        
        # 解析WHERE子句
        where_match = re.search(r'WHERE\s+(.*?)(?:$|;)', sql, re.IGNORECASE | re.DOTALL)
        
        if not where_match:
            # 更新所有记录
            code = [
                f"# 更新表 {table_name} 中的所有记录",
                f"for row in {table_name}:"
            ]
            
            for col, val in py_assignments.items():
                code.append(f"    row['{col}'] = {val}")
        else:
            # 解析条件
            condition = where_match.group(1).strip()
            python_condition = self._translate_condition(condition)
            
            code = [
                f"# 更新表 {table_name} 中满足条件的记录",
                f"for row in {table_name}:",
                f"    if {python_condition}:"
            ]
            for col, val in py_assignments.items():
                code.append(f"        row['{col}'] = {val}")
                
        code.append("")
        return "\n".join(code)
    
    def _translate_condition(self, condition: str, is_join: bool = False) -> str:
        """
        将SQL条件转换为Python条件
        """
        # 处理JOIN条件中的字段引用
        if is_join:
            # 处理形如 table1.column = table2.column 的条件
            condition = condition.replace('=', '==')
            join_pattern = r'(\w+)\.(\w+)\s*==\s*(\w+)\.(\w+)'
            condition = re.sub(join_pattern, r"row_\1['\2'] == row_\3['\4']", condition)
        else:
            # 处理字段引用，先完成替换以避免与关键字冲突
            def replace_field(match):
                field = match.group(1)
                return f"row['{field}']"
                
            # 匹配所有可能的字段名，确保先于其他替换
            condition = re.sub(r'((?<!\w)[\w]+)(?=\s*==|\s*=|\s*!=|\s*>|\s*<|\s*>=|\s*<=|\s+is|\s+in|\s*\+|\s*\-|\s*\*|\s*\/)', replace_field, condition)
            
            # 替换运算符
            condition = condition.replace('=', '==')
        
        # 替换常见的SQL函数
        condition = re.sub(r'(?i)LOWER\s*\(\s*(\w+)\s*\)', r"\1.lower()", condition)
        condition = re.sub(r'(?i)UPPER\s*\(\s*(\w+)\s*\)', r"\1.upper()", condition)
        
        # 替换特殊关键字
        condition = re.sub(r'(?i)(\w+)\s+LIKE\s+([\'"][^\'"%]*%[^\'"]*[\'"]+)', r"\1.startswith(\2[:-1])", condition)
        condition = re.sub(r'(?i)(\w+)\s+LIKE\s+([\'"][^\'"]*%[^\'"]*[\'"]+)', r"\1.endswith(\2[1:])", condition)
        condition = re.sub(r'(?i)NOT\s+NULL', 'is not None', condition)
        condition = re.sub(r'(?i)IS\s+NULL', 'is None', condition)
        
        # 替换逻辑运算符，确保保留作为标识符一部分的AND/OR
        condition = re.sub(r'(?i)(\s+)AND(\s+)', r'\1and\2', condition)
        condition = re.sub(r'(?i)(\s+)OR(\s+)', r'\1or\2', condition)
        
        # 处理BETWEEN
        between_match = re.search(r'(\w+)\s+BETWEEN\s+(\S+)\s+AND\s+(\S+)', condition, re.IGNORECASE)
        if between_match:
            field = between_match.group(1)
            lower = between_match.group(2)
            upper = between_match.group(3)
            replacement = f"({field} >= {lower} and {field} <= {upper})"
            condition = re.sub(r'\w+\s+BETWEEN\s+\S+\s+AND\s+\S+', replacement, condition, flags=re.IGNORECASE)
        
        return condition


def main():
    translator = AdvancedSQLTranslator()
    
    print("高级SQL语句翻译器 - 将SQL语句转换为Python数组操作")
    print("支持的操作: CREATE TABLE, INSERT, DELETE, SELECT, UPDATE")
    
    # 检查命令行参数
    import sys
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = input_file.rsplit('.', 1)[0] + '.py' if len(sys.argv) <= 2 else sys.argv[2]
        
        print(f"正在翻译文件: {input_file} -> {output_file}")
        translator.translate_file(input_file, output_file)
        print(f"翻译完成，结果已保存到: {output_file}")
        return
    
    print("输入 'exit' 退出程序")
    print("输入 'file <输入文件> [输出文件]' 翻译整个SQL文件")
    print("-" * 50)
    
    exec_globals = {}
    while True:
        print("\n请输入SQL语句，支持多行输入，输入END结束：")
        lines = []
        while True:
            line = input()
            if line.strip() == 'END':
                break
            lines.append(line)
        sql = '\n'.join(lines).strip()
        if not sql:
            continue
        if sql.lower() == 'exit':
            break
        if sql.lower().startswith('file '):
            parts = sql.split(None, 2)
            input_file = parts[1] if len(parts) > 1 else None
            output_file = parts[2] if len(parts) > 2 else None
            if not input_file:
                print("错误: 请提供输入文件路径")
                continue
            if not output_file:
                output_file = input_file.rsplit('.', 1)[0] + '.py'
            try:
                translator.translate_file(input_file, output_file)
                print(f"翻译完成，结果已保存到: {output_file}")
            except Exception as e:
                print(f"翻译出错: {str(e)}")
            continue
        try:
            stmts = translator._split_sql_statements(sql)
            for stmt in stmts:
                if not stmt.strip():
                    continue
                python_code = translator.translate(stmt)
                print("\n转换后的Python代码:")
                print("-" * 50)
                print(python_code)
                print("-" * 50)
                exec(python_code, exec_globals)
        except Exception as e:
            print(f"转换出错: {str(e)}")
    print("程序已退出")


if __name__ == "__main__":
    main()
