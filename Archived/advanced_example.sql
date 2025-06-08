-- 创建学生表
CREATE TABLE students (
    student_id INT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    age INT NOT NULL,
    gender CHAR(1),
    grade FLOAT,
    enrollment_date DATE
);

-- 创建课程表
CREATE TABLE courses (
    course_id INT PRIMARY KEY NOT NULL,
    title TEXT NOT NULL,
    credits INT NOT NULL,
    teacher_name TEXT
);

-- 创建学生-课程关系表
CREATE TABLE enrollments (
    enrollment_id INT PRIMARY KEY NOT NULL,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    semester TEXT NOT NULL,
    score FLOAT,
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

-- 插入学生数据
INSERT INTO students (student_id, name, age, gender, grade, enrollment_date)
VALUES (1, 'Alice', 20, 'F', 3.8, '2022-09-01');

INSERT INTO students (student_id, name, age, gender, grade, enrollment_date)
VALUES (2, 'Bob', 19, 'M', 3.5, '2022-09-01');

INSERT INTO students (student_id, name, age, gender, grade, enrollment_date)
VALUES (3, 'Charlie', 21, 'M', 3.2, '2021-09-01');

-- 插入课程数据
INSERT INTO courses (course_id, title, credits, teacher_name)
VALUES (101, 'Introduction to Computer Science', 3, 'Dr. Smith');

INSERT INTO courses (course_id, title, credits, teacher_name)
VALUES (102, 'Database Systems', 4, 'Dr. Johnson');

INSERT INTO courses (course_id, title, credits, teacher_name)
VALUES (103, 'Algorithms', 4, 'Dr. Williams');

-- 插入选课数据
INSERT INTO enrollments (enrollment_id, student_id, course_id, semester, score)
VALUES (1, 1, 101, 'Fall 2022', 92.5);

INSERT INTO enrollments (enrollment_id, student_id, course_id, semester, score)
VALUES (2, 1, 102, 'Fall 2022', 88.0);

INSERT INTO enrollments (enrollment_id, student_id, course_id, semester, score)
VALUES (3, 2, 101, 'Fall 2022', 90.0);

INSERT INTO enrollments (enrollment_id, student_id, course_id, semester, score)
VALUES (4, 3, 103, 'Spring 2022', 91.5);

-- 查询所有学生信息
SELECT * FROM students;

-- 查询指定条件的学生
SELECT name, age, grade FROM students WHERE gender = 'F' AND grade > 3.5;

-- 查询选修了特定课程的学生
SELECT s.student_id, s.name, c.title, e.score
FROM students s
JOIN enrollments e ON s.student_id = e.student_id
JOIN courses c ON e.course_id = c.course_id
WHERE c.title = 'Database Systems';

-- 删除特定学生的选课记录
DELETE FROM enrollments WHERE student_id = 3;

-- 删除不及格的选课记录
DELETE FROM enrollments WHERE score < 60;
