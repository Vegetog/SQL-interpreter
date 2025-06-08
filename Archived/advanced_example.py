# 自动生成的Python代码 - 由SQL翻译器生成
# 原始SQL文件: advanced_example.sql

# 初始化数据结构

# --------------------------------------------------
# CREATE TABLE students (
#     student_id INT PRIMARY KEY NOT NULL,
#     name TEXT NOT NULL,
#     age INT NOT NULL,
#     gender CHAR(1),
#     grade FLOAT,
#     enrollment_date DATE
# )
# 创建表: students
students = []  # 每次建表自动清空表数据
students_schema = {
    "student_id": "int",
    "name": "str",
    "age": "int",
    "gender": "str",
    "grade": "float",
    "enrollment_date": "str"
}

# --------------------------------------------------
# CREATE TABLE courses (
#     course_id INT PRIMARY KEY NOT NULL,
#     title TEXT NOT NULL,
#     credits INT NOT NULL,
#     teacher_name TEXT
# )
# 创建表: courses
courses = []  # 每次建表自动清空表数据
courses_schema = {
    "course_id": "int",
    "title": "str",
    "credits": "int",
    "teacher_name": "str"
}

# --------------------------------------------------
# CREATE TABLE enrollments (
#     enrollment_id INT PRIMARY KEY NOT NULL,
#     student_id INT NOT NULL,
#     course_id INT NOT NULL,
#     semester TEXT NOT NULL,
#     score FLOAT,
#     FOREIGN KEY (student_id) REFERENCES students(student_id),
#     FOREIGN KEY (course_id) REFERENCES courses(course_id)
# )
# 创建表: enrollments
enrollments = []  # 每次建表自动清空表数据
enrollments_schema = {
    "enrollment_id": "int",
    "student_id": "int",
    "course_id": "int",
    "semester": "str",
    "score": "float"
}

# 定义外键关系
enrollments_foreign_keys = [
    {
        "local_column": "student_id",
        "ref_table": "students",
        "ref_column": "student_id"
    },
    {
        "local_column": "course_id",
        "ref_table": "courses",
        "ref_column": "course_id"
    }
]

# --------------------------------------------------
# INSERT INTO students (student_id, name, age, gender, grade, enrollment_date)
# VALUES (1, 'Alice', 20, 'F', 3.8, '2022-09-01')
# 向表 students 插入一条记录
new_row = {'student_id': 1, 'name': 'Alice', 'age': 20, 'gender': 'F', 'grade': 3.8, 'enrollment_date': '2022-09-01'}
students.append(new_row)

# --------------------------------------------------
# INSERT INTO students (student_id, name, age, gender, grade, enrollment_date)
# VALUES (2, 'Bob', 19, 'M', 3.5, '2022-09-01')
# 向表 students 插入一条记录
new_row = {'student_id': 2, 'name': 'Bob', 'age': 19, 'gender': 'M', 'grade': 3.5, 'enrollment_date': '2022-09-01'}
students.append(new_row)

# --------------------------------------------------
# INSERT INTO students (student_id, name, age, gender, grade, enrollment_date)
# VALUES (3, 'Charlie', 21, 'M', 3.2, '2021-09-01')
# 向表 students 插入一条记录
new_row = {'student_id': 3, 'name': 'Charlie', 'age': 21, 'gender': 'M', 'grade': 3.2, 'enrollment_date': '2021-09-01'}
students.append(new_row)

# --------------------------------------------------
# INSERT INTO courses (course_id, title, credits, teacher_name)
# VALUES (101, 'Introduction to Computer Science', 3, 'Dr. Smith')
# 向表 courses 插入一条记录
new_row = {'course_id': 101, 'title': 'Introduction to Computer Science', 'credits': 3, 'teacher_name': 'Dr. Smith'}
courses.append(new_row)

# --------------------------------------------------
# INSERT INTO courses (course_id, title, credits, teacher_name)
# VALUES (102, 'Database Systems', 4, 'Dr. Johnson')
# 向表 courses 插入一条记录
new_row = {'course_id': 102, 'title': 'Database Systems', 'credits': 4, 'teacher_name': 'Dr. Johnson'}
courses.append(new_row)

# --------------------------------------------------
# INSERT INTO courses (course_id, title, credits, teacher_name)
# VALUES (103, 'Algorithms', 4, 'Dr. Williams')
# 向表 courses 插入一条记录
new_row = {'course_id': 103, 'title': 'Algorithms', 'credits': 4, 'teacher_name': 'Dr. Williams'}
courses.append(new_row)

# --------------------------------------------------
# INSERT INTO enrollments (enrollment_id, student_id, course_id, semester, score)
# VALUES (1, 1, 101, 'Fall 2022', 92.5)
# 向表 enrollments 插入一条记录
new_row = {'enrollment_id': 1, 'student_id': 1, 'course_id': 101, 'semester': 'Fall 2022', 'score': 92.5}
enrollments.append(new_row)

# 验证外键约束
# 检查 student_id 是否存在于 students.student_id 中
# 这里只是注释，实际项目中可以实现外键约束检查
# 检查 course_id 是否存在于 courses.course_id 中
# 这里只是注释，实际项目中可以实现外键约束检查

# --------------------------------------------------
# INSERT INTO enrollments (enrollment_id, student_id, course_id, semester, score)
# VALUES (2, 1, 102, 'Fall 2022', 88.0)
# 向表 enrollments 插入一条记录
new_row = {'enrollment_id': 2, 'student_id': 1, 'course_id': 102, 'semester': 'Fall 2022', 'score': 88.0}
enrollments.append(new_row)

# 验证外键约束
# 检查 student_id 是否存在于 students.student_id 中
# 这里只是注释，实际项目中可以实现外键约束检查
# 检查 course_id 是否存在于 courses.course_id 中
# 这里只是注释，实际项目中可以实现外键约束检查

# --------------------------------------------------
# INSERT INTO enrollments (enrollment_id, student_id, course_id, semester, score)
# VALUES (3, 2, 101, 'Fall 2022', 90.0)
# 向表 enrollments 插入一条记录
new_row = {'enrollment_id': 3, 'student_id': 2, 'course_id': 101, 'semester': 'Fall 2022', 'score': 90.0}
enrollments.append(new_row)

# 验证外键约束
# 检查 student_id 是否存在于 students.student_id 中
# 这里只是注释，实际项目中可以实现外键约束检查
# 检查 course_id 是否存在于 courses.course_id 中
# 这里只是注释，实际项目中可以实现外键约束检查

# --------------------------------------------------
# INSERT INTO enrollments (enrollment_id, student_id, course_id, semester, score)
# VALUES (4, 3, 103, 'Spring 2022', 91.5)
# 向表 enrollments 插入一条记录
new_row = {'enrollment_id': 4, 'student_id': 3, 'course_id': 103, 'semester': 'Spring 2022', 'score': 91.5}
enrollments.append(new_row)

# 验证外键约束
# 检查 student_id 是否存在于 students.student_id 中
# 这里只是注释，实际项目中可以实现外键约束检查
# 检查 course_id 是否存在于 courses.course_id 中
# 这里只是注释，实际项目中可以实现外键约束检查

# --------------------------------------------------
# SELECT * FROM students
# 从表 students 中查询数据
result = students.copy()
print(result)

# --------------------------------------------------
# SELECT name, age, grade FROM students WHERE gender = 'F' AND grade > 3.5
# 从表 students 中查询数据
result = students.copy()
result = [row for row in result if row['gender'] == 'F' and row['grade'] > 3.5]
result = [{'name': row['name'], 'age': row['age'], 'grade': row['grade']} for row in result]
print(result)

# --------------------------------------------------
# SELECT s.student_id, s.name, c.title, e.score
# FROM students s
# JOIN enrollments e ON s.student_id = e.student_id
# JOIN courses c ON e.course_id = c.course_id
# WHERE c.title = 'Database Systems'
# 从表 students, enrollments, courses 中查询数据
for row_s in students:
    for row_e in enrollments:
        if row_s['student_id'] == row_e['student_id']:
            for row_c in courses:
                if row_e['course_id'] == row_c['course_id']:
                    if row_c['title'] == 'Database Systems':
                        joined_row = {'student_id': row_s['student_id'], 'name': row_s['name'], 'title': row_c['title'], 'score': row_e['score']}
                        result.append(joined_row)
print(result)

# --------------------------------------------------
# DELETE FROM enrollments WHERE student_id = 3
# 删除表 enrollments 中满足条件的记录
enrollments = [row for row in enrollments if not (row['student_id'] == 3)]

# --------------------------------------------------
# DELETE FROM enrollments WHERE score < 60
# 删除表 enrollments 中满足条件的记录
enrollments = [row for row in enrollments if not (row['score'] < 60)]
