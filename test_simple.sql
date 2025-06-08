-- simple_schema.sql
-- 用户信息表
CREATE TABLE Users (
    UserID INT PRIMARY KEY NOT NULL,
    UserName TEXT NOT NULL,
    Age INT
);

-- 产品信息表
CREATE TABLE Products (
    ProductID INT PRIMARY KEY NOT NULL,
    ProductName TEXT NOT NULL,
    Price REAL NOT NULL
);

-- 订单信息表 (可选，用于JOIN测试)
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY NOT NULL,
    UserID INT NOT NULL,
    ProductID INT NOT NULL,
    OrderDate TEXT
);

-- simple_data.sql
-- Users 表数据
INSERT INTO Users (UserID, UserName, Age) VALUES
(1, 'Alice', 30),
(2, 'Bob', 25),
(3, 'Charlie', 35); -- Charlie 可能没有订单

-- Products 表数据
INSERT INTO Products (ProductID, ProductName, Price) VALUES
(101, 'Laptop', 1200.00),
(102, 'Mouse', 25.00),
(103, 'Keyboard', 75.00),
(104, 'Monitor', 300.00); -- Monitor 可能没有被订购

-- Orders 表数据
INSERT INTO Orders (OrderID, UserID, ProductID, OrderDate) VALUES
(1, 1, 101, '2025-05-10'), -- Alice 买了 Laptop
(2, 2, 102, '2025-05-11'), -- Bob 买了 Mouse
(3, 1, 103, '2025-05-12'); -- Alice 买了 Keyboard

-- CREATE TABLE (已在上面定义)

-- INSERT INTO ... VALUES ... (单行与多行)
INSERT INTO Users (UserID, UserName, Age) VALUES (4, 'David', 40);
INSERT INTO Products (ProductID, ProductName, Price) VALUES (105, 'Webcam', 50.00), (106, 'Headphones', 80.00);

-- UPDATE ... SET ... WHERE ...
UPDATE Users SET Age = 31 WHERE UserID = 1;
UPDATE Products SET Price = 20.00 WHERE ProductName = 'Mouse';

-- DELETE FROM ... WHERE ...
DELETE FROM Orders WHERE OrderID = 3; -- 删除 Alice 的 Keyboard 订单
DELETE FROM Products WHERE ProductID = 106; -- 删除 Headphones

-- DROP TABLE
-- DROP TABLE Users; -- 答辩时可能不需要演示，因为会删除所有数据