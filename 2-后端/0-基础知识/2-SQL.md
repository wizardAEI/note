# SQL语句

## 基础

SQL是用于访问和处理数据库的标准的计算机语言，SQL是Structured Query Language的缩写，是指结构化查询语言。

特点：

- 简单易学
- 功能强大
- 只说明要做什么，不说明如何做
- 标准化，几乎所有的关系型数据库都通用
- 不区分大小写

## 创建表

`create table xxx(...)`

例子：

```sql
# 创建一个部门表
CREATE TABLE dept(
	deptno INT PRIMARY KEY, # 部门编号 int类型 主键
	dname VARCHAR(9), # 部门名称 长度可变的字符串 最长为9
	loc VARCHAR(10) # 部门位置 长度可变的字符串 最长为 10
);
# 创建一个员工表
CREATE TABLE employees(
	empno INT PRIMARY KEY, # 员工号 int类型 主键
	`name` VARCHAR(10) NOT NULL, # 名称 长度可变的字符串 最长为10 不能为空
	deptno INT, # 所属部门
	manager INT, # 所属部门经理是谁（员工号）
	hiredate DATE, # 雇佣时间
	salary NUMERIC(7,2) # 薪水 类型为长度为7，小数点2位的数字 例如4400.00 多余就四舍五入
);
# 创建一个经理表
CREATE TABLE managers(
	empno INT PRIMARY KEY, # 员工号
	title VARCHAR(16) # 头衔
); 
```

### 主键

主键的全称是主键约束，表的主键由表中的一个字段或多字段组成，主键唯一代表表中一条记录，关系数据库中通常每个表都有一个主键，没有主见的表通常是不严谨的设计产物。

主键特点：

- 每个表只能定义一个主键
- 主键值必须唯一标识表中的每一条记录，且不能为null，即表中不可能存在由相同主键值的两条记录。
- 一个字段名只能在联合主键字段中出现一次
- 联合主键不能包含不必要的多余字段。当把联合主键的某一字段删除后，剩下的字段不能唯一代表一条记录。

## 插入记录

写法1:

这种写法需要保证值的顺序和表中字段顺序相同

`insert into 表名 values (字段1的值, 字段2的值, 字段3的值, ...)`

写法2：

`insert into 表名(字段1,字段2,字段3,...) values (字段1的值, 字段2的值, 字段3的值, ...)`

例子：

```sql
# 写法一
INSERT INTO employees VALUES(1,'张三',1,2,'2011-03-03',4400.00)
# 写法二
INSERT INTO employees(empno,`name`,salary) VALUES(5,'赵七',4000.00)

# 连续插入4条
INSERT INTO managers VALUES(2,'技术部经理');
INSERT INTO managers VALUES(4,'销售部经理');
INSERT INTO managers VALUES(5,'行政部经理');
INSERT INTO managers VALUES(99,'总裁')

# 一条语句连续插入4条
INSERT INTO managers VALUES(2,'技术部经理'),(4,'销售部经理'),(5,'行政部经理'),(99,'总裁')
```



## 删除记录

`delete`语句用于删除表中的记录。语法如下：

delete from 表名 where子句；

注意：where子句用于指定哪些记录需要删除。如果省略where子句，表中的所有记录都将被删除！

```sql
DELETE FROM employees WHERE `name`='张三'
```



## 更新记录

`update`语句用于更新表中的记录。语法如下：

`update 表名 set 字段1=值1,字段2=值2,...where子句`

where子句用于指定哪些记录需要更新。如果省略where子句，表中所有的记录都将被更新。

例子：

```sql
# 更新名称
UPDATE employees SET `name`='孙五',deptno=3 WHERE empno=4

# 工资增加10%
UPDATE employees SET salary=1.1*salary WHERE empno=4
```



## 查询记录

使用`select`进行查询

写法一：

查询表中的所有字段：

`select * from 表名`

例子：

```sql
SELECT * FROM employees
```

查询表中指定的字段：

`select 字段一,字段二 from 表名`

例子：

```sql
SELECT `name`,deptno FROM employees
```



## distinct 去除重复值

同一字段中可能会出现重复值，使用关键字`distinct`可以去除掉重复值，用法如下：

`select distinct 字段名 from 表名`

例子：

```sql
SELECT `name` FROM employees
```

查询出：

| 张三 |
| ---- |
| 王五 |
| 张三 |
| 赵六 |



```sql
SELECT DISTINCT `name` FROM employees
```

查询出：

| 张三 |
| ---- |
| 王五 |
| 赵六 |



## where

### where可以搭配运算符来查询记录：

| 运算符                    | 说明                 |
| ------------------------- | -------------------- |
| =                         | 等于                 |
| <> 或 !=                  | 不等于               |
| > , <                     | 大于, 小于           |
| <= , >=                   | 小于等于，大于等于   |
| =                         | 等于                 |
| BETWEEN value1 AND value2 | 在某个范围内         |
| LIKE                      | 搜索匹配的字符串模式 |

### and和or运算符

abd和or可以用在where子句中把两个或者多个条件结合起来。and运算符要求两个条件都成立；or运算符要求两个条件中只要有一个成立即可。语法如下：

`select 字段名 from 表名 where 字段n 运算符 值n and|or 字段m 运算符 值m`

```sql
# 查询 empno大于4或小于2的所有记录的名字
SELECT DISTINCT `name` FROM employees WHERE empno < 2  OR empno > 4
# 以赵开头的名字的记录
SELECT * FROM employees WHERE `name` LIKE '赵%'
```

### in运算符

in运算符是在where子句中指定多个搜索条件可以匹配的值。in运算符实际是多个or条件的合并。语法如下：

`select 字段名 from 表名 where 字段名 in （值1,值2,值3,...）`

例子：

```sql
SELECT * FROM employees WHERE `name` IN ('张三','李四','王五')
```

`not in`作为`in`的否定形式可以查询不在范围内的记录：

```sql
SELECT * FROM employees WHERE `name` NOT IN ('张三','李四','王五')
```

### 子查询

使用子查询的结果来作为主查询`where`的条件:

语法：

`select 字段1,字段2,... from 表名 where 字段名 操作符 (子查询)`

```sql
# 查询所有办公地点以一楼开头的部门编号对应的所有员工名
SELECT `name` from employees WHERE deptno in (SELECT deptno FROM dept WHERE loc like '一楼%')
```

## oder by 排序

`oder by`用于对结果集进行排序，默认俺升序(asc)进行排序，也可以指定按降序对结果进行排序。语法如下：

`select 字段名 from 表名 order by 字段1,字段2，...asc|desc`

例子：

```sql
# 按编号降序排序
SELECT * from employees ORDER BY empno DESC
```



## index 索引

索引可以提高访问数据的速度。创建索引的语法如下：

create index 索引名 on 表名(字段1,字段2,...)

使用索引时SQL语句的语法和不使用索引没有任何不同，SQL语句会自动使用索引提高访问数据的速度。

例子：

```sql
# 在employees的name上创建索引
CREATE INDEX in_name on employees(`name`)
```



## view 视图

视图是基于SQL语句的结果集的可视化表，视图中的字段就是来自一个或多个数据库中的真实的表中的字段。

视图总是显示当前的数据。每当用户查询视图时，数据库引擎通过SQL语句来重建视图。

创建视图的语法：

`create view 视图名 as select语句`

例子：

```sql
CREATE VIEW employees_2015 as SELECT `name`,salary FROM employees WHERE hiredate < '2015-01-01'
```

修改视图也会更改底层数据库的值。



## null值

`NULL`值代表遗漏的位置数据，它的作用是为止的或不适用的值的占位符。

如果表中的某个列是可选的，那么我们可以在不向该列添加值的情况下插入新记录或者更新已有记录。这意味着该字段将以NULL值保存。

字段值是否是`NULL`不可以用`<>`或`=`判断，要用`IS NOT NULL`或`IS NULL`判断。

```sql
SELECT * from employees WHERE deptno IS NULL
```



## 别名

在SQL语句中可以为表名或者字段名指定临时使用的别名（Alias），别名旨在当前的SQL语句中生效，它通常比字段名更具有可读性。

别名语法：

`select 字段名 as 别名 from 表名 as 别名`

其中`as`可以省略。

例子：

```sql
SELECT `name` `姓名` from employees WHERE deptno IS NOT NULL
```



## join连接

join连接是基于多个表之间的共同字段把它们结合起来进行查询的一种方法。连接分为以下几种：

内连接（inner join）: 列出两个表中都存在的记录，默认使用内连接

左连接（left join）: 即使没有匹配也列出左表中的所有记录n 

右连接（right join）: 即使没有匹配也列出右表中所有的记录

语法：

`select 字段名 from 表1 join 表2 where子句`

例子：

```sql
SELECT dept.deptno,loc,`name` FROM dept JOIN employees WHERE dept.deptno=1 AND employees.id=2

# 左连接
SELECT dept.deptno,loc,`name` FROM dept LEFT JOIN employees ON dept.deptno=1 AND employees.id=2;
```

注意这里使用左连接时使用了`ON`关键字，它代表生成两个表的笛卡尔乘积。这里我们使用外连接时如果使用 `WHERE`会导致语法报错。



## 常用函数

### count函数

count函数统计符合条件的记录数，`count(*)`统计表中的记录总数，count(字段名)统计指定字段中不为null的记录数

```sql
# 统计所有记录
SELECT COUNT(*) FROM employees
```

### max min函数

使用`max(字段) | min(字段名)`统计该字段最大或最小的值

例子：

```sql
SELECT MIN(`hiredate`) FROM employees
```

### avg函数

返回平均值

### sum函数

返回和

## group by 分组

`group by`语句用于结合统计函数，根据一个或多个列对结果集进行分组。语法如下：

`select 字段名,统计函数 from 表名 where子句 group by 字段名`

```sql
SELECT `name`,MIN(hiredate) FROM employees GROUP BY `deptno`
```

这里显示`employees`表的记录，并根据`deptno`进行分组，显示的列为`name`和每一组中的最小的入职日期，由于name没有统计函数进行约束，所以会显示该组中的第一条记录。

结果：

| name | MIN(hiredate) |
| ---- | ------------- |
| 张三 | 2011-03-03    |
| 赵四 | (NULL)        |



## having过滤分组

having子句和where子句类似，都是对查询到结果集进行过滤。它们的过滤对象不同，where子句对被选择的列进行过滤，而having子句则对group by 子句产生的组进行过滤。

语法：

`select 字段名,统计函数 from 表名 where子句 group by 字段名 having 统计函数|字段名 运算符 值`

例子：

```sql
# 查询employees中以deptno作为分组，组内的平均值大于4000.00的组，并列出组的deptno字段和最小的工资记录
SELECT deptno,MIN(salary) FROM employees GROUP BY `deptno` HAVING AVG(salary) > 4000.00
```



## limit 限制查询

使用`limit`可以限制查询出的记录数量。

语法：

` SELECT * FROM users LIMIT 数量`

例子：

```sql
 SELECT * FROM users ORDER BY id LIMIT 1;
```



## case when语句

[(24条消息) SQL之CASE WHEN用法详解_涛声依旧叭的博客-CSDN博客_case when](https://blog.csdn.net/rongtaoup/article/details/82183743)



## sql避坑

### UNIQUE索引批量添加遇错中断

当表中有索引且其索引类型为`UNIQUE`时，我们向该表中批量添加数据，遇到有重复的该列的记录，批量添加过程会直接报错返回，不会添加数据。

例如：

```sql
INSERT INTO `foods` (`food_name`,`deleted_at`) VALUES ("xxx",NULL),("apple",NULL)
```

其中`food_name`列存在上面的索引情况，如果我们的foods表中已经存在了apple这条记录，那么此时会报以下错误，并且不会添加任何记录。

```sql
1062 - Duplicate entry 'apple' for key 'foods.idx_food_name'
```



## 实践题

### 查询最小价格：

方法1：用用 **ORDER BY** 把价格进行分组，用 **ASC** 升序排列，再用 **LIMIT** 分页获取第一条数据。

```sql
SELECT * FROM commodity ORDER BY price ASC LIMIT 1;
```

方法二：使用组合查询，先查询到最小的价格是多少，再用这个价格查出对应的数据。

```sql
SELECT * FROM commodity WHERE price = (SELECT MIN(price) FROM commodity)
```
