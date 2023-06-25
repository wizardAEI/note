## 为什么需要 Redis

- 数据量增长；
- 读写数据压力不断增加；
- 数据从表单，演进成了分库分表；
- MySQL从单机演进成了集群。

在高数据量，高 QPS 下，数据的读取压力变大，我们可以使用这样的思路来解决问题：

- 数据分冷热，热数据为经常被访问到的数据；
- 将热数据缓存到内存中，访问时无需再去数据库磁盘中访问；
- 内存从磁盘中更新数据。

## Redis 基本原理

现在的问题是，如果我们将数据直接存在内存中，那么如果该程序的进程结束了或者宕机，可能就会出现数据丢失的情况。

Redis 通过**给写命令追加到 AOF 文件**的方式来使得数据可以持久化。AOF 文件位于磁盘中，是持久化的。Redis 每次重启时，都会去找到该文件来得到增量数据实现数据持久化的效果。

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20230215125416.png)

## Redis 应用案例

### 连续签到案例（ String ）

用户每日有一次签到的机会，如果断签，连续签到计数将归0（必须在每天的24点前签到）。

我们设计一个数据结构（Claim）：

- Key： cc_uid_123123123123
- value: 252  // 代表连续签到252天
- expireAt: 后天的零点 // 过期时间

这个案例下，我们可以 String 数据结构作为 value，并且配合 expire 来使用。

redis 中的 String 数据结构：

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20230215132416.png)

案例核心代码：

```go
// addContinuesDays 为用户签到续期
func addContinuesDays(ctx context.Context, userID int64) {
	key := fmt.Sprintf(continuesCheckKey, userID)
	// 1. 连续签到数+1
	err := RedisClient.Incr(ctx, key).Err()
	if err != nil {
		fmt.Errorf("用户[%d]连续签到失败", userID)
	} else {
		expAt := beginningOfDay().Add(48 * time.Hour)
		// 2. 设置签到记录在后天的0点到期
		if err := RedisClient.ExpireAt(ctx, key, expAt).Err(); err != nil {
			panic(err)
		} else {
			// 3. 打印用户续签后的连续签到天数
			day, err := getUserCheckInDays(ctx, userID)
			if err != nil {
				panic(err)
			}
			fmt.Printf("用户[%d]连续签到：%d(天), 过期时间:%s", userID, day, expAt.Format("2006-01-02 15:04:05"))
		}
	}
}

// getUserCheckInDays 获取用户连续签到天数
func getUserCheckInDays(ctx context.Context, userID int64) (int64, error) {
	key := fmt.Sprintf(continuesCheckKey, userID)
	days, err := RedisClient.Get(ctx, key).Result()
	if err != nil {
		return 0, err
	}
	if daysInt, err := strconv.ParseInt(days, 10, 64); err != nil {
		panic(err)
	} else {
		return daysInt, nil
	}
}

// beginningOfDay 获取今天0点时间
func beginningOfDay() time.Time {
	now := time.Now()
	y, m, d := now.Date()
	return time.Date(y, m, d, 0, 0, 0, 0, time.Local)
}
```



### 消息通知（ List ）

例如我们写文章后网站会发送消息进行通知。这里我们使用 list 作为消息队列的数据结构。

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20230215155739.png)

案例核心代码：

```go
RedisClient.LPush(ctx, "msg", "xiaoxi")

// 并发的去读取
for {
    RedisClient.BRPop(ctx, 0, list) // pop并返回，如果读不到就阻塞
}
```

Redis 的 List 是由一个双向链表和 listpack 实现的。其中双向链表来实现前后迭代，listpack 用来存储多个数据（为了节省内存）。也就是在一个节点可能存储多个 key-value

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20230215162116.png)

### 多指标计数（ Hash ）

对于一个用户来说，可能会有很多计数指标，例如点赞数，关注数，收藏数等等。我们可以通过一个 hash 表来把一个人的这些数据全部存储起来。

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20230215162920.png)

案例核心代码：

```go
// 每次加进去的 hashmap 不一定要一样
RedisClient.HSet(ctx, key, map[string]interface{}{
    "user_id": "a",
    "xx_counr": 19,
})

RedisClient.HGet(ctx, key, field).Result() // 获取对应 hashmap 对应域的值
RedisClient.HGetAll(ctx, key).Result() // 获取对应 hashmap 中的全部域和值
RedisClient.HIncrBy(ctx, key, field, incr).Result() // 给对应的域值 + incr, 增量可以为负
```

Redis 的 Hash 和常规 hash 表不同的是在扩容时采用了渐进式迁移数据。将数据一部分一部分迁移，保证效率和用户无感。迁移后在将访问地址指向对应内存，让用户去访问迁移后的内存。

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20230215164840.png)

### 排行榜

针对大流量和 QPS 的访问排序结果，例如实时排行榜，Redis 实现了一个 SortedSet 来进行快速排序查询。

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20230215165819.png)

案例核心代码：

```go
RedisClient.ZAdd() // 在有续集中添加成员
RedisClient.ZIncrBy(ctx, key, increment, member) // 为有序集 key 的成员 member 的 score 值加上增量 increment (可以为负)。
RedisClient.ZScore() // 返回某个成员的排行
RedisClient.ZRange() // 返回指定区间的成员和排行
```

Redis 实现 Zset（也就是有顺序的集合）使用的是跳跃表 SkipList 和 词典 dict。

跳跃表将一个链分成很多子链，通过不同跳跃程度的链来实现快速找到节点（优化迭代）。

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20230215170925.png)

而 Redis 加上了在每一个节点中加入了字典来存储除了节点之外的分值信息。

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20230215171242.png)

### 限流

要求1秒内放行的请求为 N ，超过 N 则禁止访问。我们实现这个限流，也可以通过 Redis 去实现。

我们可以构建一个 key ，例如：`xx_req_time_1671356046`，这个 key 记录了当前xx请求的最后一次时间戳，对这个 key 调用incr，超过限制就禁止访问。这里使用的 Redis 数据结构为 String。

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20230215171605.png)

核心代码：

```go
RedisClient.Incr(ctx, key)
```

## Redis 使用注意事项

### 避免大Key，热Key

大key定义：

- 对于 String 类型，value 的字节数大于 10KB 。
- Hash / Set / Zset / List 等复杂数据结构：元素个数大于 500 个或总 value 字节数大于 10MB。

由于 Redis 是单线程的，所以大key会导致读取，更改成本过高，导致主从复制异常，服务阻塞等。在业务侧会表现为超时报错。

业务设计时要避免大key，或者将大key拆分和压缩。

业务侧实现：

1. 将长 String 拆分成多个 String；
2. 使用压缩算法压缩数据；
3. 使用 hash 算法将 key 拆分再存；
4. 区分冷热数据，例如只缓存前10页数据，后续走DB。

热key定义：

某个Key的 QPS （例如大于500）特别高，即使采用了分片，也会导致负载过高等。

解决热key的方法：

1. 业务侧服务设置 LocalCache（本地缓存），降低反复访问服务器的Redis带来的QPS。（例如Go的Bigcache）；

2. 拆分热key：用不同的 key 存一个 value 值，并且保存在不同的实例中来降低负载；

3. 使用 Redis 代理，实现热key承载能力。本质上是 热key发现 + LocalCache。

   我们再客户端访问 Redis 中间加一个代理，代理去统计 Key 的访问频率，如果较高就认为是热key，然后再自己的服务器上缓存，再请求直接返回。

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/image-20230215175124735.png)

### 慢查询

慢查询也容易导致访问数据过慢，甚至服务崩溃。

以下操作会导致慢查询：

- 单次批量操作（建议单次批量操作不要超过100）
- zset的大部分命令复杂度是O(log(n)),所以其中不要存太多数据（5K以内）
- 使用大Key

### 缓存穿透，缓存雪崩

缓存穿透：热点数据查询绕过缓存，直接去查询数据库（例如Redis宕机时，或者黑客/误操作去查询一个不存在的key）。缓存穿透容易导致db响应慢甚至宕机。

缓存雪崩：大量缓存**同时**过期。这样大量的请求会落到DB上。

解决办法：

- 针对上面的`黑客/误操作去查询一个不存在的key`，我们可以缓存空key，下次再来请求这样的key我们就直接返回一个空值；或者通过`布隆过滤器`来过滤非法Key。
- 对于缓存雪崩，我们可以对不同的 Key 设置不同的过期时间，例如分别设置10分1秒，10分23秒，10分8秒。
- 使用缓存集群，避免单机宕机和缓存雪崩（不同的节点由于拉取缓存时间不同，过期时间也一般不同）。



## 相关文档

> [Go Redis 客户端 (uptrace.dev)](https://redis.uptrace.dev/zh/guide/)
>
> [redis 命令手册](https://redis.com.cn/commands.html)