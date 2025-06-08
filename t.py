tables = {}  # 初始化表字典
# 错误: 字段定义后多余内容: PRIMARY
tables['f'].append({'id': 101, 'i': 'Hello SQL', 'j': 2025, 'k': 'MacOS', 'm': 3.14})
if 'f' in tables:
    del tables['f']
    # 可选：同步删除表结构
    if '_schemas' in tables and 'f' in tables['_schemas']:
        del tables['_schemas']['f']
# 错误: 字段定义后多余内容: PRIMARY
tables['Students'].append({'StudentID': 1, 'Name': '张三', 'Age': 20})
tables['Students'].append({'StudentID': 2, 'Name': '李四', 'Age': 22})
tables['Students'].append({'StudentID': 3, 'Name': '王五', 'Age': 21})
tables['Students'].append({'StudentID': 4, 'Name': '赵六', 'Age': 23})
tables['Students'].append({'StudentID': 5, 'Name': '钱七', 'Age': 19})
# 错误: 字段定义后多余内容: PRIMARY
tables['Courses'].append({'CourseID': 101, 'CourseName': '数据库原理', 'StudentID': 1, 'Grade': 'A'})
tables['Courses'].append({'CourseID': 102, 'CourseName': '操作系统', 'StudentID': 2, 'Grade': 'B+'})
tables['Courses'].append({'CourseID': 103, 'CourseName': '计算机网络', 'StudentID': 1, 'Grade': 'B'})
tables['Courses'].append({'CourseID': 104, 'CourseName': '数据结构', 'StudentID': 3, 'Grade': 'A-'})
tables['Courses'].append({'CourseID': 105, 'CourseName': '算法设计', 'StudentID': 2, 'Grade': 'A'})
tables['Courses'].append({'CourseID': 106, 'CourseName': '人工智能', 'StudentID': 'NULL', 'Grade': 'NULL'})
result = [{'S.Name': row['S.Name'], 'C.CourseName': row['C.CourseName']} for row in tables['Students'] if True]
print('查询结果:')
for row in result:
    print(row)
result = [{'Students.Name': row['Students.Name'], 'Courses.CourseName': row['Courses.CourseName']} for row in tables['Students'] if True]
print('查询结果:')
for row in result:
    print(row)
result = [{'Students.Name': row['Students.Name'], 'Courses.CourseName': row['Courses.CourseName']} for row in tables['Students'] if True]
print('查询结果:')
for row in result:
    print(row)
# INTERSECT
results = []
sub_result = []
result = [{'Name': row['Name']} for row in tables['Students'] if True]
print('查询结果:')
for row in result:
    print(row)
results.append(sub_result)
sub_result = []
result = [{'Name': row['Name']} for row in tables['Teachers'] if True]
print('查询结果:')
for row in result:
    print(row)
results.append(sub_result)
if results:
    columns = list(results[0][0].keys()) if results[0] else []
    sets = [set(tuple(row.get(col) for col in columns) for row in r) for r in results]
    common = set.intersection(*sets) if sets else set()
    seen = set()
    result = []
    for row in results[0]:
        k = tuple(row.get(col) for col in columns)
        if k in common and k not in seen:
            seen.add(k)
            result.append(row)
else:
    result = []
print('查询结果:')
for row in result:
    print(row)
