# 迷你SQL解释器（Python实现）

https://github.com/Vegetog/SQL-interpreter

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

### 5. 集合操作（UNION/INTERSECT/EXCEPT）

- 支持 `UNION`（并集）、`INTERSECT`（交集）、`EXCEPT`（差集）三种集合操作。
- 语法示例：
  - `SELECT ... FROM ... UNION [ALL] SELECT ... FROM ...`（可多重UNION，ALL为不去重）
  - `SELECT ... FROM ... INTERSECT SELECT ... FROM ...`（可多重INTERSECT）
  - `SELECT ... FROM ... EXCEPT SELECT ... FROM ...`（可多重EXCEPT）
- 所有集合操作都严格用输出列做key，支持`SELECT *`及任意列顺序。
- `UNION`/`INTERSECT`/`EXCEPT`（非ALL）结果自动去重，即使原表有重复，输出也不会有重复。
- 差集/交集/并集的唯一性判断只基于SELECT输出的列，完全符合SQL标准。

### 6. 支持SQL注释
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

### 7. 自动去重与唯一性说明
- EXCEPT/INTERSECT/UNION（非 ALL）结果自动去重，即使原表有重复，输出也不会有重复。
- 差集/交集/并集的唯一性判断只基于 SELECT 输出的列。

### 8. 其他特性
- 支持多行SQL输入（以分号`;`结尾）
- 所有错误信息高亮为红色，便于调试
- 自动记录所有表的结构信息（`_schemas`）
- 运行时可随时查看所有表及其内容
