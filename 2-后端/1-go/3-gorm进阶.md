## 前传：database/sql

### 基础概述

`database/sql`包为go实现了一套统一的抽象的**接口**，用来连接数据库和类数据库

由于他只是提供了一套统一的抽象接口，具体实现还是要引用到各个数据库实现的driver来实际实现连接数据库。

例如，我们如果要连接mysql数据库：

```go
import (
	"database/sql"
	"time"

	_ "github.com/go-sql-driver/mysql"
)

// ...
// 连接数据库
db, err := sql.Open("mysql", "user:password@/dbname")
if err != nil {
	panic(err)
}

// ...
// 查询数据库,最终释放链接
rows, err := sql.Query("select id, name from users where id = ?", 1) // rows为得到的记录游标
defer rows.Close()

// 得到所有符合查询语句的记录, 这里我们一直去向后查询游标，直到没有记录了  tips: 这里没有处理错误，正式使用中一定要及时处理
for rows.Next() {
    var user User
    _ := rows.Scan(&user.ID, &use.Name)
    users = append(users, user)
}
```

### 设计原理

database/sql 作为一个连接上层应用程序和底层的数据库之间的框架，它对上实现了一个**操作接口**，让我们可以对不同的sql库使用一套操作接口；对下它实现了连接接口和操作接口，让不同的数据库实现自己的 driver 来适配 database/sql。它本身则实现了一个连接池，用来适应大连接量操作。

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20230207213801.png)

## GORM

### 基础概念

GORM 是一个设计简介，功能强大，自由扩展的全功能 ORM。GORM 是为了避免 database/sql 需要写大量的sql语句，通过封装 database/sql 并且加入了很多实用性扩展实现的一个框架。

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20230207224450.png)

[GORM 指南](https://gorm.io/zh_CN/docs/index.html)中对GORM的功能介绍和基本使用都已经非常完善了，这里不再赘述。

### GORM 设计原理

#### sql 是怎么生成的？

对于一般的 SQL 语句，以查询语句为例，可能会具有 SELECT Clause，FROM Clause，WHERE Clause，ORDER BY Clause，LIMIT Clause，FOR Clause ：

```sql
SELECT `name` FROM `USER` WHERE age > 35 AND role <> `manager` ORDER BY age DESC LIMIT 10 OFFSET 10 FOR UPDATE
```

 对应我们的 gorm 代码：

```go
db.Where("role <> ?", "manager").Where("age > ?", 35).Limit(100).Order("age desc").Find(&user)
```

其中，Where 函数，Limit 函数和 Order 函数对应的都是 Chain Method，最终的 Find 函数则是一个 Finisher Method。

**Chain Method 的作用在于给 gorm 添加子句，而最终的 Finisher Method 的作用则是指定类型和执行。**

例如，这里我们的 Finisher Method 是 Find 方法，那么 gorm 在生成 SQL 时，会首先添加进来 SELECT  FROM 指令。而我后面的Chain Method 则是对应添加 WHERE Clause，ORDER BY Clause，LIMIT Clause 等子句。

以 WHERE 为例，其源代码为：

```go
func (db *DB) Where(query interface{}, args ...interface{}) (tx *DB) {
	tx = db.getInstance()
	if conds := tx.Statement.BuildCondition(query, args...); len(conds) > 0 {
		tx.Statement.AddClause(clause.Where{Exprs: conds})
	}
	return
}
```

可以比很清楚的看到，其中的 `AddClause` 方法将我们的给出的条件都作为一个个的子句中的表达式添加到了 WHERE Clause 中。

而对于 Finisher Method 而言，我们以 First 为例（此处默认第二个参数条件没有填，下面代码也会省略相应部分）：

```go
func (db *DB) First(dest interface{}, conds ...interface{}) (tx *DB) {
    tx = db.getInstance() // 这里后期有改动，但核心逻辑还是创建了一个数据库实例
	// ...
	tx.Statement.Dest = dest 
	return tx.callbacks.Query().Execute(tx)
}
```

在 gorm 中，我们也可以显式地去调用 Claus() 去拓展 各部分的 SQL 子句：[高级查询 | GORM - The fantastic ORM library for Golang, aims to be developer friendly.](https://gorm.io/zh_CN/docs/advanced_query.html#优化器、索引提示)

#### 插件系统

当我们的 Finisher Method 执行之后，gorm 的插件系统开始执行一系列动作：首先分析 Finisher Method，得到 Statement 类型，例如 SELECT，UPDATE 等，并且根据其类型，执行对应的回调方法，生成 SQL 语句并执行。

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20230208183402.png)

例如，对于一个 Create 方法，我们分析处他的 Statement 类型后去执行对应 Callback:

```go
// 对应的db.Create()
func (db *DB) Create(value interface{}) (tx *DB) {
    return tx.callbacks.Create().Execute(tx) // 核心代码 这里去找 callbacks.Create() 的相关方法去执行
}
// 对应callbacks.Create()
func (cs *callbacks) Create() *processor {
	return cs.processors["create"] // 返回记录下来的所有相关 callback，这里使用map保存
}
// Execute() 执行callback
func (p *processor) Execute(db *DB) *DB {
    // ...
	for _, f := range p.fns {
		f(db)
	}
}
```

当然，我们也可以去扩展插件来让每次执行 Create，Update 等方法时，可以工作我们自己的插件：

```go
// 注册新的插件
db.Callback().Create().Register("mypligin", func(*gorm.DB) {})
// 删除
db.Callback().Create().Remove("myplugin")
// 替换
db.MysqlDB.Callback().Create().Replace("myplugin", func(db *gorm.DB) {})
// 指定顺序
db.Callback().Create().Before("gorm:create").After("gorm:after_create").Register("myplugin", func(db *gorm.DB) {})
// 注册到最前面
db.Callback().Create().Before("*").Register("myplugin", func(db *gorm.DB) {})
```

更多内容：[编写插件 | GORM - The fantastic ORM library for Golang, aims to be developer friendly.](https://gorm.io/zh_CN/docs/write_plugins.html)

gorm 插件可以实现多种功能，例如多数据库的读写分离：

[DBResolver | GORM - The fantastic ORM library for Golang, aims to be developer friendly.](https://gorm.io/zh_CN/docs/dbresolver.html#读写分离)

### ConnPool

ConnPool 是 gorm 定义的一个接口层，并且使用 database/sql 包去实现这些接口从而使用 ConnPool 作为新的连接池层。

这样的设计可以使我们实际和数据库进行交互的**连接池层和 DB Connect 层解耦**，在需要使用不同的数据库存储数据库或者需要进行读写分离时可以更加方便。

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20230208215826.png)



## 最佳实践

### 数据序列化与SQL表达式

当我们使用不同的数据库时，难免会遇到一些复杂的数据结构序列化放入、查询数据库的情况。

对于创建和查询来说，GORM 允许使用 SQL 表达式插入数据，有两种方法实现这个目标。根据 `map[string]interface{}` 或 [自定义数据类型](https://gorm.io/zh_CN/docs/data_types.html#gorm_valuer_interface) 创建或查询：

```go
// 通过 map 创建记录
db.Model(User{}).Create(map[string]interface{}{
  "Name": "jinzhu",
  "Location": clause.Expr{SQL: "ST_PointFromText(?)", Vars: []interface{}{"POINT(100 100)"}},
})
// INSERT INTO `users` (`name`,`location`) VALUES ("jinzhu",ST_PointFromText("POINT(100 100)"));
```

自定义数据类型要求我们去自定义结构和实现 `GORMValuer` 方法：

```go
type Location struct {
    X, Y int
}

func (loc Location) GormValue(ctx context.Context, db *gorm.DB) clause.Expr {
  return clause.Expr{
    SQL:  "ST_PointFromText(?)",
    Vars: []interface{}{fmt.Sprintf("POINT(%d %d)", loc.X, loc.Y)},
  }
}

db.Create(&User{
  Name:     "jinzhu",
  Location: Location{X: 100, Y: 100},
})
db.Model(&user).Update("Location", Location{X: 100, Y: 100})                
```

查询方式，我们也可以使用类似的方法:

```go
// 方法1：使用gorm.Expr
tx := db.Where("location = ?", gorm.Expr("ST_PointFromText(?)", "POINT(100 100)")).First(&user)
// 方法2：GORMValuer
func (loc Location) GormValue(ctx context.Context, db *gorm.DB) clause.Expr {
    return gorm.Expr("ST_PointFromText(?)", fmt.Sprintf("POINT(100 100)", loc.X, loc.Y))
}
tx := db.Where("location = ?", Location{X: 100, Y: 100})
// 方法3：自定义查询 SQL 实现接口 clause.Expression 例子：https://github.com/go-gorm/gorm/blob/master/clause/where.go
// 方法3可以让我们更加灵活的书写sql，这种写法可以让我们在不同的数据库使用不同的sql查询方式
```

上面是对于一些数据库独有数据结构如何去存储，对于业务层面的复杂结构，我们也会需要去进行序列化操作。

常见的序列化问题包括：

- 一个复杂的结构体，将其转为json保存在数据库中
- 将int作为日期时间保存在数据库
- 自定义需求，如将密码保存在数据库时，在最后序列化阶段完成加密操作

这时我们可以使用到 GORM 的 Serializer，它允许自定义如何使用数据库对数据进行序列化和反序列化

GORM 提供了一些默认的序列化器：json、gob、unixtime，这里有一个如何使用它的快速示例: [序列化 | GORM ](https://gorm.io/zh_CN/docs/serializer.html)

如果需要自定义序列化器，我们需要去实现以下接口：

```go
import "gorm.io/gorm/schema"

type SerializerInterface interface {
    Scan(ctx context.Context, field *schema.Field, dst reflect.Value, dbValue interface{}) error
    SerializerValuerInterface
}

type SerializerValuerInterface interface {
    Value(ctx context.Context, field *schema.Field, dst reflect.Value, fieldValue interface{}) (interface{}, error)
}
```

### 批量数据创建/查询

批量创建，我们可以使用到`Create`，`CreateInBatches`

[创建 | GORM - The fantastic ORM library for Golang, aims to be developer friendly.](https://gorm.io/zh_CN/docs/create.html#批量插入)

批量查询，我们可以使用 `Rows` 方法。该方法会返回一个迭代器:

```go
rows, err := db.Model(&User{}).Where("role = ？"， "admin").Rows()
for rows.Next() {
	rows.Scan(&name, &age, &email) //或 db.ScanRows(rows, &user)
}
```

或者也可以使用 `FindInBatches` 方法批量查询（适用于有很多条，防止查询出错时）。

**tips:**

批量查询时难免会遇到速度问题，我们可以使用以下几种方法加速：

1. 从 整体级别 或 会话级别 关闭默认事务（ `SkipDefaultTransaction` ），来提速批量新增和修改更加快速；

2. 默认批量增加会调用 Hooks 方法，使用 `SkipHooks` 跳过（在进行批量导入数据时，某些钩子并不是很重要）：

   ```go
   DB.Session(&gorm.Session{SkipHooks: true}).CreateInBatches(users, 1000)
   ```

3. 开启 sql 预编译缓存

4. 混合使用：

   ```go
   // 会话级别
   tx := db.Session(&gorm.Session{
       SkipHooks: true, SkipDefaultTransaction: true, PrepareStmt: true, CreateBatchSize: 1000,
   })
   tx.Create(&users) // 会自动每1000条一次创建
   ```

### 代码复用

gorm 支持将一些代码逻辑抽离出来，并使用 `Scopes` 方法进行代码复用。[Scopes ](https://gorm.io/zh_CN/docs/scopes.html)

**分页**逻复用使用实例：[分页](https://gorm.io/zh_CN/docs/scopes.html#分页)

在同一个连接下，我们有时会进行分库分表，scope 也可以实现**分库分表**（动态表）：[动态表](https://gorm.io/zh_CN/docs/scopes.html#动态表)

### Sharding

Sharding 是一个高性能的 Gorm 分表中间件。它基于 Conn 层做 SQL 拦截、AST 解析、分表路由、自增主键填充，带来的额外开销极小。

例如上面的分库分表（同一个连接下），我们可以使用 Sharding 为其创建一些固定的逻辑和策略来支持动态表：[Sharding](https://gorm.io/zh_CN/docs/sharding.html)

### 混沌工程/压测

为了测试系统抗压性和安全性，混沌工程和压力测试是很重要的。

**混沌工程**

实现混沌工程，我们可以在创建数据库连接时，通过编写插件的形式。通过提供一些插入，更新，查询等操作的错误更改，来查看系统本身是否可以监测并反制。

**压测**

gorm 提供了 `withContext` 来设置上下文，我们可以将一些关于数据库的配置放在上下文中，当我们进行压力测试时，根据上下文中的信息，及时切换测试数据库和正是数据库：[Context](https://gorm.io/zh_CN/docs/context.html#Chi-中间件示例)。

### Logger

详情见：[Logger](https://gorm.io/zh_CN/docs/logger.html)。

可以注意到的是，这里的Logger也是可以根据需要，切换成全局模式或者会话模式。

### 数据库迁移

gorm 可以使用结构体自动迁移数据库：

```go
db.AutoMigrate(&User{})
```

如果我们需要更多地迁移数据库的配置，那么也可以使用一些数据库版本定制，迁移工具等，例如 [gormigrate package - github.com/go-gormigrate/gormigrate/v2 - Go Packages](https://pkg.go.dev/github.com/go-gormigrate/gormigrate/v2)

gorm 本身也提供了一个 `Migrator` 的 interface，可以利用该接口实现相关方法来自定义迁移。

另外还有 `ColumnType` 接口用来获取列类型来辅助管理数据库。

### Row SQL (原生SQL）和 命名参数

我们可以利用 `Row` 和 `Exec` 方法来写原生 sql 语句。[SQL 构建器](https://gorm.io/zh_CN/docs/sql_builder.html#原生-SQL)

gorm 同时提供了命名参数来支持 [`sql.NamedArg`](https://tip.golang.org/pkg/database/sql/#NamedArg)、`map[string]interface{}{}` 或 struct 形式的命名参数： [命名参数](https://gorm.io/zh_CN/docs/sql_builder.html#命名参数)

### 代码生成 Gen

对于上面的原生SQL书写，我们也可以将其抽离出来，包装成一个函数并生成自己的代码使用：

[Gen Guides | GORM - The fantastic ORM library for Golang, aims to be developer friendly.](https://gorm.io/zh_CN/gen/index.html)

### 安全问题

gorm 默认使用参数的方式传入数据，这样的写法不会产生sql注入问题。

但是如果我们将用户的输入来直接拼接到查询中，这样可能会出现sql注入问题：

```go
sql := fmt.Sprintf("name = %v", userInput)
db.where(sql).First(&user) // 可能产生注入
```

### 更高的性能

通过 GORM 会增加 ORM 语句解析成 sql 语句的消耗，可以通过开启 statement 预编译将使用过的解析语句缓存起来，加快执行速度。

另一方面，我们可以使用关闭默认事务配置 `SkipDefaultTransaction: true` 让 gorm 中的写操作跳过内置的默认封装事务过程来提高性能。

```go
全局模式：
db, err := gorm.Open(sqlite.Open("gorm.db"), &gorm.Config{
    PrepareStmt: true,
    SkipDefaultTransaction: true
})
会话模式：
tx := db.Session(&Session{PrepareStmt: true})
```

此外，还可以在 DSN 中加入 `interpolateParams=false` 这一设置，默认为true是为了防止传统字符集下 sql 注入的问题，但是这个设置会导致我们请求次数增加（一次请求变成了 执行前预编译 -> 调用预编译 -> 关闭预编译 三个请求），但现在使用 UTF-8编码 的情况下，已经不需要这一功能了，将其设为 false 性能更高。

