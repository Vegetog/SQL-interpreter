-- 学生信息表
CREATE TABLE Students (
    StudentID INT PRIMARY KEY NOT NULL,
    Name TEXT NOT NULL,
    Age INT NOT NULL,
    City TEXT,
    EnrollDate TEXT -- 模拟日期字符串
);

-- 课程信息表
CREATE TABLE Courses (
    CourseID INT PRIMARY KEY NOT NULL,
    CourseName TEXT NOT NULL,
    Credits INT NOT NULL,
    Department CHAR(10)
);

-- 学生选课表 (关联 Students 和 Courses)
CREATE TABLE Enrollments (
    EnrollmentID INT PRIMARY KEY NOT NULL,
    StudentID INT NOT NULL,
    CourseID INT NOT NULL,
    Grade TEXT
);

-- 教师信息表 (用于测试 Name 和 City 的集合操作)
CREATE TABLE Teachers (
    TeacherID INT PRIMARY KEY NOT NULL,
    Name TEXT NOT NULL,
    Subject TEXT,
    City TEXT
);

-- 部门信息表 (用于测试多层 JOIN 和复杂条件)
CREATE TABLE Departments (
    DeptID CHAR(10) PRIMARY KEY NOT NULL,
    DeptName TEXT NOT NULL,
    Head TEXT
);

-- Students 表数据
INSERT INTO Students (StudentID, Name, Age, City, EnrollDate) VALUES
(1, '张三', 20, '北京', '2023-09-01'),
(2, '李四', 22, '上海', '2023-09-01'),
(3, '王五', 21, '广州', '2023-09-01'),
(4, '赵六', 23, '北京', '2024-03-01'), -- 与张三城市重复
(5, '钱七', 19, '深圳', '2023-09-01'),
(6, '孙八', 20, '北京', '2024-03-01'), -- 与张三年龄、城市重复
(7, '李四', 24, '杭州', '2023-09-01'); -- 与李四姓名重复，城市不同

-- Courses 表数据
INSERT INTO Courses (CourseID, CourseName, Credits, Department) VALUES
(101, '数据库原理', 4, 'CS'),
(102, '操作系统', 4, 'CS'),
(103, '计算机网络', 3, 'EE'),
(104, '数据结构', 5, 'CS'),
(105, '算法设计', 5, 'CS'),
(106, '人工智能', 3, 'AI'),
(107, '高等数学', 4, 'Math'); -- 未被任何学生选择

-- Enrollments 表数据
INSERT INTO Enrollments (EnrollmentID, StudentID, CourseID, Grade) VALUES
(1, 1, 101, 'A'),   -- 张三 数据库原理
(2, 2, 102, 'B+'),  -- 李四 操作系统
(3, 1, 103, 'B'),   -- 张三 计算机网络
(4, 3, 104, 'A-'),  -- 王五 数据结构
(5, 2, 105, 'A'),   -- 李四 算法设计
(6, 4, 101, 'C'),   -- 赵六 数据库原理
(7, 5, 104, 'B'),   -- 钱七 数据结构
(8, 6, 106, 'A');   -- 孙八 人工智能

-- Teachers 表数据
INSERT INTO Teachers (TeacherID, Name, Subject, City) VALUES
(201, '王老师', '数据库', '北京'),
(202, '李四', '操作系统', '上海'),   -- 姓名与学生重复，城市与学生李四重复
(203, '张老师', '数据结构', '广州'),
(204, '赵老师', '算法设计', '天津'),
(205, '王老师', '计算机网络', '北京'), -- 姓名和城市与201重复
(206, '刘五', '人工智能', '深圳');     -- 姓名与学生钱七城市重复，姓名不重复

-- Departments 表数据
INSERT INTO Departments (DeptID, DeptName, Head) VALUES
('CS', '计算机科学', '陈教授'),
('EE', '电子工程', '林教授'),
('AI', '人工智能', '张教授'),
('Math', '数学系', '李教授');

-- INSERT INTO ... VALUES ... (单行与多行)
INSERT INTO TestTable (id, name) VALUES (1, 'Test1');
INSERT INTO TestTable (id, name) VALUES (2, 'Test2'), (3, 'Test3');

-- UPDATE ... SET ... WHERE ...
UPDATE Students SET Age = 21 WHERE StudentID = 1;
UPDATE Students SET City = '未知' WHERE StudentID = 7; -- 更新已存在的行
UPDATE Students SET EnrollDate = '2025-01-01' WHERE StudentID = 99; -- 不存在的行，应影响0行

-- DELETE FROM ... WHERE ...
DELETE FROM TestTable WHERE id = 1;
DELETE FROM TestTable; -- 删除所有数据

-- DROP TABLE
DROP TABLE TestTable;

-- SELECT * 和多列
SELECT * FROM Students;
SELECT StudentID, Name, City FROM Students WHERE Age > 20 AND City = '北京';

-- WHERE 条件 (AND, OR, NOT, 括号嵌套)
SELECT Name, Age FROM Students WHERE (Age < 22 AND City = '上海') OR (Age = 20 AND NOT Name = '张三');
SELECT CourseName FROM Courses WHERE NOT (Credits = 3 OR Department = 'AI');

-- 常见比较操作符
SELECT Name FROM Students WHERE Age >= 22;
SELECT CourseName FROM Courses WHERE Credits <> 4; -- 或 !=
SELECT Name FROM Teachers WHERE Subject = '数据库';

-- ORDER BY
SELECT Name, Age FROM Students ORDER BY Age DESC, Name ASC;
SELECT CourseName, Credits FROM Courses ORDER BY Credits ASC;

-- LIMIT
SELECT Name FROM Students LIMIT 3;
SELECT Name FROM Students ORDER BY Age DESC LIMIT 2 OFFSET 1; -- 获取年龄第二大的学生

-- PRIMARY KEY 冲突 (应报错)
INSERT INTO Students (StudentID, Name, Age) VALUES (1, '新学生', 25);

-- NOT NULL 约束失败 (应报错)
INSERT INTO Students (StudentID, Name, Age, City) VALUES (8, '空姓名', NULL, '南京'); -- Name 是 NOT NULL

-- UPDATE 时 NOT NULL 约束失败 (应报错)
UPDATE Students SET Name = NULL WHERE StudentID = 1;

-- INNER JOIN
SELECT S.Name, E.Grade, C.CourseName
FROM Students AS S
INNER JOIN Enrollments AS E ON S.StudentID = E.StudentID
INNER JOIN Courses AS C ON E.CourseID = C.CourseID;

-- LEFT JOIN
SELECT S.Name, E.Grade, C.CourseName
FROM Students AS S
LEFT JOIN Enrollments AS E ON S.StudentID = E.StudentID
LEFT JOIN Courses AS C ON E.CourseID = C.CourseID; -- 钱七、李四（7号）应该有 NULL

-- RIGHT JOIN (模拟)
SELECT S.Name, C.CourseName
FROM Courses AS C
LEFT JOIN Enrollments AS E ON C.CourseID = E.CourseID
LEFT JOIN Students AS S ON E.StudentID = S.StudentID; -- 人工智能、高等数学的学生名称应为 NULL

-- FULL JOIN (模拟)
SELECT S.Name, C.CourseName
FROM Students AS S LEFT JOIN Enrollments AS E ON S.StudentID = E.StudentID LEFT JOIN Courses AS C ON E.CourseID = C.CourseID
UNION ALL
SELECT S.Name, C.CourseName
FROM Courses AS C LEFT JOIN Enrollments AS E ON C.CourseID = E.CourseID LEFT JOIN Students AS S ON E.StudentID = S.StudentID
WHERE S.StudentID IS NULL; -- 包含所有学生和所有课程

-- CROSS JOIN
SELECT S.Name, T.Name FROM Students AS S CROSS JOIN Teachers AS T LIMIT 10; -- 仅显示部分结果

-- 多层 JOIN
SELECT S.Name, C.CourseName, D.DeptName
FROM Students AS S
JOIN Enrollments AS E ON S.StudentID = E.StudentID
JOIN Courses AS C ON E.CourseID = C.CourseID
JOIN Departments AS D ON C.Department = D.DeptID
WHERE S.Age > 20 AND D.DeptName = '计算机科学'
ORDER BY S.Name;

-- UNION ALL (不带去重)
SELECT Name FROM Students
UNION ALL
SELECT Name FROM Teachers; -- 会看到两个 '李四'，两个 '王老师'

-- UNION (自动去重)
SELECT Name FROM Students
UNION
SELECT Name FROM Teachers; -- '李四', '王老师' 各一个

-- INTERSECT (交集)
SELECT Name FROM Students
INTERSECT
SELECT Name FROM Teachers; -- 应该返回 '李四'

-- EXCEPT (差集)
SELECT City FROM Students
EXCEPT
SELECT City FROM Teachers; -- 应该返回 '深圳', '杭州'

SELECT City FROM Teachers
EXCEPT
SELECT City FROM Students; -- 应该返回 '天津'

-- 多重 UNION
SELECT Name FROM Students
UNION
SELECT Name FROM Teachers
UNION
SELECT Head FROM Departments; -- 多个来源的唯一名称

-- 多重 INTERSECT
SELECT Name FROM Students
INTERSECT
SELECT Name FROM Teachers
INTERSECT
SELECT Head FROM Departments; -- 理论上返回空集，因为没有交集

-- 多重 EXCEPT (左结合)
SELECT City FROM Students
EXCEPT
SELECT City FROM Teachers
EXCEPT
SELECT DeptName FROM Departments; -- (Students.City EXCEPT Teachers.City) EXCEPT Departments.DeptName