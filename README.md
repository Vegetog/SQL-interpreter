# 迷你SQL解释器（Python实现）

## 功能概述

本项目实现了一个基于词法分析、语法分析、AST的迷你SQL解释器，支持在内存中操作表数据，主要功能如下：

### 1. 基本SQL语句支持
- `CREATE TABLE`：支持多字段、类型、NOT NULL、PRIMARY KEY等约束的建表语句
- `DROP TABLE`：支持删除表及其结构定义
- `INSERT INTO ... VALUES ...`：支持单行和多行（批量）插入，类型和约束检查
- `SELECT ... FROM ...`：支持多列、`*`、WHERE、ORDER BY、LIMIT、多表JOIN（见下）
- `UPDATE ... SET ... WHERE ...`：支持类型和约束检查
- `DELETE FROM ... WHERE ...`

### 2. 多表JOIN支持
- 支持 `INNER JOIN`、`LEFT JOIN`/`LEFT OUTER JOIN`、`RIGHT JOIN`/`RIGHT OUTER JOIN`、`FULL JOIN`/`FULL OUTER JOIN`、`CROSS JOIN`
- 支持 `ON` 条件，自动处理字段命名冲突（输出为"表.字段"）
- 支持 SELECT *、ORDER BY、LIMIT 等与 JOIN 结合使用

### 3. WHERE 条件
- 支持复杂条件表达式：`AND`、`OR`、`NOT`、括号嵌套
- 支持常见比较操作符：`=`, `!=`, `<>`, `>`, `<`, `>=`, `<=`

### 4. 字段类型与约束
- 支持字段类型：`INT`、`REAL`、`TEXT`、`CHAR(n)`
- 支持 `NOT NULL` 约束（插入/更新时强制检查）
- 支持 `PRIMARY KEY` 约束（唯一性和非空性检查）
- 解析并记录但暂未强制检查：`UNIQUE`、`FOREIGN KEY` 等

### 5. 其他特性
- 支持多行SQL输入（以分号`;`结尾）
- 所有错误信息高亮为红色，便于调试
- 自动记录所有表的结构信息（`_schemas`）
- 运行时可随时查看所有表及其内容

## 新增特性

### 1. 支持 EXCEPT 差集
- 语法：`SELECT ... FROM ... EXCEPT SELECT ... FROM ...`，可多重 EXCEPT。
- 结果为第一个 SELECT 有、后续 SELECT 没有的唯一行（自动去重）。
- 差集判断只用输出列做 key，完全符合 SQL 标准。

### 2. 支持 INTERSECT 交集
- 语法：`SELECT ... FROM ... INTERSECT SELECT ... FROM ...`，可多重 INTERSECT。
- 结果为所有 SELECT 都有的唯一行（自动去重）。
- 交集判断只用输出列做 key。

### 3. 支持多重 UNION/INTERSECT/EXCEPT
- 可连续写多个 SELECT ... UNION ... UNION ... 或 INTERSECT/EXCEPT。
- UNION 支持 ALL（不去重），INTERSECT/EXCEPT 只支持去重。
- 所有集合操作都严格用输出列做 key，支持 SELECT * 及任意列顺序。

### 4. 支持SQL注释
- 支持 `-- 单行注释`，如：`-- 这是一个注释`
- 支持 `/* 多行注释 */`，如：
  ```sql
  /*
    这是多行注释
    可以写多行
  */
  SELECT * FROM Students;
  ```
- 注释内容会被自动忽略，不影响SQL解析和执行。

### 5. 自动去重与唯一性说明
- EXCEPT/INTERSECT/UNION（非 ALL）结果自动去重，即使原表有重复，输出也不会有重复。
- 差集/交集/并集的唯一性判断只基于 SELECT 输出的列。

### 6. 调试建议
- 如遇集合操作结果异常，可在 executor.py 的相关分支加 print 或写日志，排查 key 生成与集合逻辑。
- parser.py/lexer.py 关键字需与 SQL 语法保持同步。

## 示例

```sql
-- 差集
SELECT City FROM Students
EXCEPT
SELECT City FROM Teachers;

-- 交集
SELECT Name FROM Students
INTERSECT
SELECT Name FROM Teachers;

-- 多重并集
SELECT Name FROM A
UNION
SELECT Name FROM B
UNION
SELECT Name FROM C;
```

## 使用方法

1. 运行 `main.py`
2. 按提示选择输入模式：
   - 1. 交互输入：手动输入SQL（支持多行，末尾加分号`;`）
   - 2. 文件输入：输入SQL文件路径，批量执行文件中的所有SQL语句
   - 3. 文件翻译：输入SQL文件路径，自动生成同名Python文件（如`test.sql`→`test.py`），每条SQL语句翻译为等价Python操作

3. 支持的SQL示例：

```sql
CREATE TABLE Song (id INT, name TEXT, albumId INT);
CREATE TABLE Album (id INT, title TEXT);
INSERT INTO Song (id, name, albumId) VALUES (1, 'A', 10), (2, 'B', 20), (3, 'C', 10);
INSERT INTO Album (id, title) VALUES (10, 'Alpha'), (20, 'Beta');
SELECT * FROM Song JOIN Album ON Song.albumId = Album.id;
SELECT * FROM Song LEFT JOIN Album ON Song.albumId = Album.id;
SELECT * FROM Song RIGHT JOIN Album ON Song.albumId = Album.id;
SELECT * FROM Song FULL JOIN Album ON Song.albumId = Album.id;
SELECT * FROM Song CROSS JOIN Album;
```

## 约束与类型检查示例
- 插入/更新时类型不符、主键重复、NOT NULL 违例等都会报错并高亮显示
- 多行INSERT会批量插入所有数据

## SQL文件翻译为Python文件
- 选择模式3，输入SQL文件路径，自动生成同名.py文件
- 每条SQL语句会被翻译为等价的Python操作（如对tables的增删查改）
- 支持所有已实现SQL语法（CREATE/INSERT/SELECT/UPDATE/DELETE/DROP/WHERE/ORDER BY/LIMIT/复杂条件、多行INSERT、多表JOIN等）
- 生成的Python代码可读、可运行（假设有tables变量）

## 扩展建议
- 可继续扩展 UNIQUE、FOREIGN KEY、聚合、NATURAL JOIN、事务等高级SQL特性

---
如有问题或建议，欢迎反馈！ 