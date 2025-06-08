CREATE TABLE f
(
    id INT PRIMARY KEY NOT NULL,
    i  TEXT            NOT NULL,
    j  INT             NOT NULL,
    k  CHAR(50),
    m  REAL
);

INSERT INTO f (id, i, j, k, m)
VALUES (101, 'Hello SQL', 2025, 'MacOS', 3.14);

DROP TABLE f;

CREATE TABLE Students (
    StudentID INT PRIMARY KEY,
    Name TEXT NOT NULL,
    Age INT
);

INSERT INTO Students (StudentID, Name, Age) VALUES
(1, '张三', 20),
(2, '李四', 22),
(3, '王五', 21),
(4, '赵六', 23),
(5, '钱七', 19); 


CREATE TABLE Courses (
    CourseID INT PRIMARY KEY,
    CourseName TEXT NOT NULL,
    StudentID INT, 
    Grade TEXT
);

INSERT INTO Courses (CourseID, CourseName, StudentID, Grade) VALUES
(101, '数据库原理', 1, 'A'),
(102, '操作系统', 2, 'B+'),
(103, '计算机网络', 1, 'B'),
(104, '数据结构', 3, 'A-'),
(105, '算法设计', 2, 'A'),
(106, '人工智能', NULL, NULL); 

SELECT S.Name, C.CourseName
FROM Students AS S
INNER JOIN Courses AS C ON S.StudentID = C.StudentID;

SELECT Students.Name, Courses.CourseName
FROM Students
INNER JOIN Courses ON Students.StudentID = Courses.StudentID;

SELECT Students.Name, Courses.CourseName
FROM Students
CROSS JOIN Courses ON Students.StudentID = Courses.StudentID;

SELECT Name FROM Students
INTERSECT
SELECT Name FROM Teachers;