CREATE TABLE Students (
    StudentID INT PRIMARY KEY NOT NULL,
    Name TEXT NOT NULL,
    Age INT NOT NULL,
    City TEXT,
    EnrollDate TEXT 
);
CREATE TABLE Courses (
    CourseID INT PRIMARY KEY NOT NULL,
    CourseName TEXT NOT NULL,
    Credits INT NOT NULL,
    Department CHAR(10)
);
CREATE TABLE Enrollments (
    EnrollmentID INT PRIMARY KEY NOT NULL,
    StudentID INT NOT NULL,
    CourseID INT NOT NULL,
    Grade TEXT
);
CREATE TABLE Teachers (
    TeacherID INT PRIMARY KEY NOT NULL,
    Name TEXT NOT NULL,
    Subject TEXT,
    City TEXT
);
CREATE TABLE Departments (
    DeptID CHAR(10) PRIMARY KEY NOT NULL,
    DeptName TEXT NOT NULL,
    Head TEXT
);
CREATE TABLE TestTable (
    id INT PRIMARY KEY NOT NULL,
    name TEXT
);

INSERT INTO Students (StudentID, Name, Age, City, EnrollDate) VALUES
(1, '张三', 20, '北京', '2023-09-01'),
(2, '李四', 22, '上海', '2023-09-01'),
(3, '王五', 21, '广州', '2023-09-01'),
(4, '赵六', 23, '北京', '2024-03-01'), 
(5, '钱七', 19, '深圳', '2023-09-01'),
(6, '孙八', 20, '北京', '2024-03-01'), 
(7, '李四', 24, '杭州', '2023-09-01'); 
INSERT INTO Courses (CourseID, CourseName, Credits, Department) VALUES
(101, '数据库原理', 4, 'CS'),
(102, '操作系统', 4, 'CS'),
(103, '计算机网络', 3, 'EE'),
(104, '数据结构', 5, 'CS'),
(105, '算法设计', 5, 'CS'),
(106, '人工智能', 3, 'AI'),
(107, '高等数学', 4, 'Math'); 
INSERT INTO Enrollments (EnrollmentID, StudentID, CourseID, Grade) VALUES
(1, 1, 101, 'A'),   
(2, 2, 102, 'B+'),  
(3, 1, 103, 'B'),   
(4, 3, 104, 'A-'),  
(5, 2, 105, 'A'),   
(6, 4, 101, 'C'),   
(7, 5, 104, 'B'),   
(8, 6, 106, 'A');   
INSERT INTO Teachers (TeacherID, Name, Subject, City) VALUES
(201, '王老师', '数据库', '北京'),
(202, '李四', '操作系统', '上海'),   
(203, '张老师', '数据结构', '广州'),
(204, '赵老师', '算法设计', '天津'),
(205, '王老师', '计算机网络', '北京'), 
(206, '刘五', '人工智能', '深圳');     
INSERT INTO Departments (DeptID, DeptName, Head) VALUES
('CS', '计算机科学', '陈教授'),
('EE', '电子工程', '林教授'),
('AI', '人工智能', '张教授'),
('Math', '数学系', '李教授');
INSERT INTO TestTable (id, name) VALUES (1, 'Test1');
INSERT INTO TestTable (id, name) VALUES (2, 'Test2'), (3, 'Test3');
UPDATE TestTable SET name = 'UpdatedTest1' WHERE id = 1;
SELECT * FROM TestTable; 
DELETE FROM TestTable WHERE id = 2;
SELECT * FROM TestTable; 
DELETE FROM TestTable;
SELECT * FROM TestTable; 
DROP TABLE TestTable;
UPDATE Students SET Age = 21 WHERE StudentID = 1; 
UPDATE Students SET City = '未知' WHERE StudentID = 7; 
UPDATE Students SET EnrollDate = '2025-01-01' WHERE StudentID = 99; 
DELETE FROM Enrollments WHERE Grade = 'C'; 
SELECT * FROM Students;
SELECT StudentID, Name, City FROM Students WHERE Age > 20 AND City = '北京';
SELECT Name, Age FROM Students WHERE (Age < 22 AND City = '上海') OR (Age = 20 AND NOT Name = '张三');
SELECT CourseName FROM Courses WHERE NOT (Credits = 3 OR Department = 'AI');
SELECT Name FROM Students WHERE Age >= 22;
SELECT CourseName FROM Courses WHERE Credits <> 4; 
SELECT Name FROM Teachers WHERE Subject = '数据库';
SELECT Name, Age FROM Students ORDER BY Age DESC, Name ASC;
SELECT CourseName, Credits FROM Courses ORDER BY Credits ASC;
SELECT Name FROM Students LIMIT 3;
SELECT Name FROM Students ORDER BY Age DESC LIMIT 2 OFFSET 1; 
INSERT INTO Students (StudentID, Name, Age, City) VALUES (1, '新学生', 25, '重庆');
INSERT INTO Students (StudentID, Name, Age, City) VALUES (8, '测试学生', NULL, '南京');
UPDATE Students SET Name = NULL WHERE StudentID = 1;
SELECT Students.Name, Enrollments.Grade, Courses.CourseName
FROM Students
INNER JOIN Enrollments ON Students.StudentID = Enrollments.StudentID
INNER JOIN Courses ON Enrollments.CourseID = Courses.CourseID;
SELECT Students.Name, Enrollments.Grade, Courses.CourseName
FROM Students
LEFT JOIN Enrollments ON Students.StudentID = Enrollments.StudentID
LEFT JOIN Courses ON Enrollments.CourseID = Courses.CourseID;
SELECT Students.Name, Courses.CourseName
FROM Courses
LEFT JOIN Enrollments ON Courses.CourseID = Enrollments.CourseID
LEFT JOIN Students ON Enrollments.StudentID = Students.StudentID;
SELECT Students.Name, Courses.CourseName
FROM Students LEFT JOIN Enrollments ON Students.StudentID = Enrollments.StudentID LEFT JOIN Courses ON Enrollments.CourseID = Courses.CourseID
UNION ALL
SELECT Students.Name, Courses.CourseName
FROM Courses LEFT JOIN Enrollments ON Courses.CourseID = Enrollments.CourseID LEFT JOIN Students ON Enrollments.StudentID = Students.StudentID
WHERE Students.StudentID IS NULL;
SELECT Students.Name, Teachers.Name FROM Students CROSS JOIN Teachers LIMIT 10;
SELECT Students.Name, Courses.CourseName, Departments.DeptName
FROM Students
INNER JOIN Enrollments ON Students.StudentID = Enrollments.StudentID
INNER JOIN Courses ON Enrollments.CourseID = Courses.CourseID
INNER JOIN Departments ON Courses.Department = Departments.DeptID
WHERE Students.Age > 20 AND Departments.DeptName = '计算机科学'
ORDER BY Students.Name;
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
SELECT City FROM Teachers
EXCEPT
SELECT City FROM Students;
SELECT Name FROM Students
UNION
SELECT Name FROM Teachers
UNION
SELECT Head FROM Departments;
SELECT Name FROM Students
INTERSECT
SELECT Name FROM Teachers
INTERSECT
SELECT Head FROM Departments;
SELECT City FROM Students
EXCEPT
SELECT City FROM Teachers
EXCEPT
SELECT DeptName FROM Departments;