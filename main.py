import os
import sys
from lexer import tokenize
from parser import Parser
from executor import execute

if __name__ == '__main__':
    # 示例内存表
    tables = {
        # 'Students': [
        #     {'StudentID': 1, 'Name': '张三', 'Age': 20, 'City': '北京'},
        #     {'StudentID': 2, 'Name': '李四', 'Age': 22, 'City': '上海'},
        #     {'StudentID': 3, 'Name': '王五', 'Age': 21, 'City': '广州'},
        #     {'StudentID': 4, 'Name': '赵六', 'Age': 23, 'City': '北京'}, # 与张三城市重复
        #     {'StudentID': 5, 'Name': '钱七', 'Age': 19, 'City': '深圳'},
        #     {'StudentID': 6, 'Name': '李四', 'Age': 25, 'City': '上海'} # 与 StudentID=2 姓名重复
        # ],
        # 'Teachers': [ # 新增一个 Teachers 表用于更好的测试
        #     {'TeacherID': 101, 'Name': '王老师', 'Subject': '数据库', 'City': '北京'},
        #     {'TeacherID': 102, 'Name': '李四', 'Subject': '操作系统', 'City': '广州'}, # 与学生姓名重复
        #     {'TeacherID': 103, 'Name': '张老师', 'Subject': '数据结构', 'City': '上海'}, # 与学生城市重复
        #     {'TeacherID': 104, 'Name': '赵老师', 'Subject': '算法设计', 'City': '天津'},
        #     {'TeacherID': 105, 'Name': '王老师', 'Subject': '计算机网络', 'City': '北京'} # 与 TeacherID=101 姓名和城市重复
        # ],
        # 'Courses': [
        #     {'CourseID': 1001, 'CourseName': '数据库原理', 'Dept': 'CS'},
        #     {'CourseID': 1002, 'CourseName': '操作系统', 'Dept': 'CS'},
        #     {'CourseID': 1003, 'CourseName': '计算机网络', 'Dept': 'EE'},
        #     {'CourseID': 1004, 'CourseName': '数据结构', 'Dept': 'CS'},
        #     {'CourseID': 1005, 'CourseName': '算法设计', 'Dept': 'CS'},
        #     {'CourseID': 1006, 'CourseName': '机器学习', 'Dept': 'AI'}
        # ]
    }

    mode = input('请选择输入模式：1. 交互输入  2. 文件输入  [1/2]: ').strip()
    if mode == '2':
        file_path = input('请输入SQL文件路径: ').strip()
        if not os.path.isfile(file_path):
            print('\033[31m错误: 文件不存在\033[0m')
        else:
            with open(file_path, encoding='utf-8') as f:
                content = f.read()
            # 按分号分割，支持多条SQL
            stmts = [stmt.strip() for stmt in content.split(';') if stmt.strip()]
            out_path = os.path.splitext(file_path)[0] + '.txt'
            with open(out_path, 'w', encoding='utf-8') as fout:
                for sql in stmts:
                    try:
                        tokens = tokenize(sql)
                        parser = Parser(tokens)
                        ast = parser.parse()
                        result = execute(ast, tables)
                        fout.write('执行结果:\n')
                        if isinstance(result, list):
                            for row in result:
                                fout.write(str(row) + '\n')
                        else:
                            fout.write(str(result) + '\n')
                    except Exception as e:
                        fout.write(f'错误: {e}\n')
                        fout.write(f'出错SQL: {sql}\n')
                    fout.write('当前所有表:\n')
                    for tname, trows in tables.items():
                        fout.write(f'表 {tname}: {trows}\n')
            print(f'所有结果已输出到: {out_path}')
    else:
        def is_sql_complete(sql):
            return sql.count('(') == sql.count(')')
        sql_buffer = ""
        while True:
            if not sql_buffer.strip():
                print('请输入SQL语句（以分号 ; 结尾，支持多行）：')
            line = input()
            if not line.strip() and not sql_buffer.strip():
                break
            sql_buffer += line + "\n"
            if ';' in line:
                stmt = sql_buffer.split(';', 1)[0].strip()
                if not stmt:
                    sql_buffer = ""
                    continue
                if not is_sql_complete(stmt):
                    # 括号不配对，继续累积输入
                    continue
                sql_buffer = ""
                try:
                    tokens = tokenize(stmt)
                    if not tokens:
                        continue
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

     