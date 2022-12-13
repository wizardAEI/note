### MongoDB

show dbs    //查看整体的使用内存情况
use   数据库    // 新建/切换库
db                    //查看当前库
 show collections //查看集合
db.表.insert({})   //插入集合（模型）
db.表.insert([{},{}])      //插入多个集合
show tables/show collections   //查看集合
db.表.drop()   //删除集合
db.dropDatabase()  //删除数据库
db.表.find({条件1},{条件2})  //查询（多个条件写数组形式，默认与逻辑）
db.表.find($or:[{条件1},{条件2}])//或逻辑

条件： 
例

  db.user.find({age:{$gt:5}})    >
                       age:{$gte:5}    >=
                       age:{$lt:5}       <
                       age{$lte:5}      <=
                       age{$ne:5}       !=
                       age{$in:[1,2,3]}    in 集合

               find({字段名:/正则/i}) 

### 统计

db.user.count()

db.user.find().count()



### 排序  1 升序  -1降序   注意排序的时候一定加find()

db.user.find().sort({age:1})  // 顺序age显示user表

### 分页

db.user.find().limit(3).skip(4)  //分页显示

### 更新

db.表名.updateOne({key:value},{$set:{key:value}})   //多个符合条件修改第一个
db.表名.updateMany({key:value},{$set:{key:value}})  //多个符合条件修改多个

### 字段值的自增和自减

db.表名.updateOne({key:value},{$inc:{key:1}})  //自增
db.表名.updateOne({key:value},{$inc:{key:-1}})  //自减

### 真删除

但实际开发中，常用逻辑上的删除，及对数据库进行修改
db.表名.deleteOne({key:value})
db.表名.deleteMany({key:value})