# 高级SQL转Python翻译器

本项目实现了一个**高级SQL语句翻译器**，可将常见SQL语句（包括多表JOIN、条件查询、插入、删除、更新等）自动转换为等价的Python数据结构操作代码。

## TODO

- KMP优化

- 文件输出的注释问题

## 当前未支持的SQL功能
- 聚合函数（如 COUNT、SUM、AVG、MIN、MAX）
- GROUP BY、HAVING 子句
- ORDER BY、LIMIT 子句
- 子查询（SELECT ... FROM (SELECT ...)）
- UNION、INTERSECT、EXCEPT 等集合操作
- INSERT/UPDATE/DELETE 的多行批量操作
- 复杂表达式（如 CASE WHEN、数学函数等）
- 视图（VIEW）、索引（INDEX）、触发器（TRIGGER）等高级对象
- 事务控制（BEGIN、COMMIT、ROLLBACK）
- 存储过程、函数、自定义类型
- 复杂的外键/唯一/检查约束的强制执行
- 复杂的SQL注入防护与安全机制

## 主要功能
- 支持 `CREATE TABLE`、`INSERT`、`DELETE`、`SELECT`、`UPDATE` 等SQL语句
- 支持多表JOIN、表别名、WHERE条件、字段类型自动推断
- 自动将SQL中的数据类型转换为Python原生类型
- 支持SQL注释（--、/* ... */）的自动忽略
- 支持交互式输入和SQL文件批量翻译

## 支持的SQL语法
- 单表/多表建表、插入、删除、更新
- 多表JOIN（支持链式JOIN和ON条件）
- WHERE条件过滤、AND/OR复合条件
- 字段类型：int、float、str、bool、date等
- 外键约束（仅注释提示，不做强制检查）

## 使用方法

### 1. 交互式模式
```bash
python advanced_translator.py
```
- 按提示输入多行SQL，输入`END`结束，自动翻译并执行。
- 输入`exit`退出。
- 输入`file <输入SQL文件> [输出Python文件]`可批量翻译整个SQL文件。

### 2. 文件批量翻译
```bash
python advanced_translator.py your_sql_file.sql [output_file.py]
```
- 自动将SQL文件翻译为Python代码，保存到指定输出文件。

## 依赖环境
- Python 3.7+
- 无需第三方库（仅用标准库）

## 示例

**输入SQL：**
```sql
CREATE TABLE students (
    student_id INT PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    age INT NOT NULL,
    gender CHAR(1),
    grade FLOAT,
    enrollment_date DATE
);

INSERT INTO students (student_id, name, age, gender, grade, enrollment_date)
VALUES (1, 'Alice', 20, 'F', 3.8, '2022-09-01');

SELECT name, age, grade FROM students WHERE gender = 'F' AND grade > 3.5;
```

**自动生成并执行的Python代码：**
```python
students = []
students_schema = {"student_id": "int", "name": "str", ...}
new_row = {'student_id': 1, 'name': 'Alice', 'age': 20, ...}
students.append(new_row)
result = students.copy()
result = [row for row in result if row['gender'] == 'F' and row['grade'] > 3.5]
result = [{'name': row['name'], 'age': row['age'], 'grade': row['grade']} for row in result]
print(result)
# 输出: [{'name': 'Alice', 'age': 20, 'grade': 3.8}]
```

---

如需扩展或有问题，欢迎反馈！ 