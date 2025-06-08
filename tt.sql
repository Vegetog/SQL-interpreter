-- Students 表
CREATE TABLE Students (
    StudentID INT PRIMARY KEY NOT NULL,
    Name TEXT NOT NULL,
    Age INT NOT NULL,
    City TEXT
);

-- Teachers 表
CREATE TABLE Teachers (
    TeacherID INT PRIMARY KEY NOT NULL,
    Name TEXT NOT NULL,
    Subject TEXT,
    City TEXT
);

-- Courses 表
CREATE TABLE Courses (
    CourseID INT PRIMARY KEY NOT NULL,
    CourseName TEXT NOT NULL,
    Dept TEXT
);

-- Students 表数据
INSERT INTO Students (StudentID, Name, Age, City) VALUES
(1, '张三', 20, '北京'),
(2, '李四', 22, '上海'),
(3, '王五', 21, '广州'),
(4, '赵六', 23, '北京'),
(5, '钱七', 19, '深圳'),
(6, '李四', 25, '上海');

-- Teachers 表数据
INSERT INTO Teachers (TeacherID, Name, Subject, City) VALUES
(101, '王老师', '数据库', '北京'),
(102, '李四', '操作系统', '广州'),
(103, '张老师', '数据结构', '上海'),
(104, '赵老师', '算法设计', '天津'),
(105, '王老师', '计算机网络', '北京');

-- Courses 表数据
INSERT INTO Courses (CourseID, CourseName, Dept) VALUES
(1001, '数据库原理', 'CS'),
(1002, '操作系统', 'CS'),
(1003, '计算机网络', 'EE'),
(1004, '数据结构', 'CS'),
(1005, '算法设计', 'CS'),
(1006, '机器学习', 'AI');

INSERT INTO Students (StudentID, Name, Age, City) VALUES (7, '周九', 28, '成都');
UPDATE Students SET Age = 21 WHERE StudentID = 2;
DELETE FROM Students WHERE StudentID = 5;

SELECT * FROM Students;
SELECT Name, City FROM Students WHERE Age > 20 AND City = '北京';
SELECT Name FROM Students WHERE (Age = 20 OR Age = 21) AND NOT City = '北京';

SELECT Name, Age FROM Students ORDER BY Age DESC;
SELECT Name, Age FROM Students ORDER BY Age DESC LIMIT 3;

INSERT INTO Students (StudentID, Name, Age, City) VALUES (1, '新张三', 20, '天津');
INSERT INTO Students (StudentID, Name, Age, City) VALUES (8, NULL, 30, '南京');

SELECT Students.Name, Teachers.Name FROM Students INNER JOIN Teachers ON Students.Name = Teachers.Name;
SELECT Students.Name, Teachers.Name FROM Students LEFT JOIN Teachers ON Students.Name = Teachers.Name;
SELECT Students.Name, Teachers.Name FROM Students RIGHT JOIN Teachers ON Students.Name = Teachers.Name;
SELECT Students.Name, Teachers.Name FROM Students FULL JOIN Teachers ON Students.Name = Teachers.Name;
SELECT Students.Name, Teachers.Name FROM Students CROSS JOIN Teachers;

SELECT Name FROM Students
UNION ALL
SELECT Name FROM Teachers;

SELECT Name FROM Students
UNION
SELECT Name FROM Teachers;

SELECT Name FROM Students
INTERSECT
SELECT Name FROM Teachers;

SELECT City FROM Students
EXCEPT
SELECT City FROM Teachers;
/*
优先级：
-- union = except < intersect
*/
SELECT Name FROM Students
UNION
SELECT Name FROM Teachers
INTERSECT
SELECT CourseName FROM Courses;

(SELECT Name FROM Students
UNION
SELECT Name FROM Teachers)
INTERSECT
SELECT CourseName FROM Courses;

DROP TABLE Students;