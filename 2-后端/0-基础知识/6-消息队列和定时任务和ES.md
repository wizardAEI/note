# 消息队列

## 消息队列概念

### 消息队列解决的问题

1. QPS不稳定，有时会很大导致服务器无法同时解决，但是买更好的服务器不划算

2. 链路耗时太长，导致响应过久

   <img src="https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20230219222251.png" style="zoom:33%;" />

3. 处理日志

对应的处理方案：

1. 将处理存入消息队列，慢慢处理（**削峰**）

2. 异步完成长链路

   ![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20230219222657.png)

3. 使用队列存储并持久化log

   ![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20230219223032.png)

### MQ是什么？

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/image-20230219223219117.png)



## Kafka理论基础

Kafka 是分布式发布-订阅消息系统。它是一个分布式的，可划分的，冗余备份的**持久性(存储在磁盘)**的日志服务。它主要用于**处理活跃的流式数据**。

### Kafka特点

- 为发布和订阅提供高吞吐量。据了解，Kafka 每秒可以生产约25万消息（50 MB），每秒处理55万消息（110 MB）。

- 可进行持久化操作。将消息持久化到磁盘，因此可用于批量消费，例如ETL，以及实时应用程序。通过将数据持久化到硬盘以及 replication（复制） 防止数据丢失。

- 分布式系统，易于向外扩展。所有的 producer、broker 和 consumer 都会有多个，均为分布式的。无需停机即可扩展机器。

- 消息被处理的状态是在 consumer 端维护，而不是由server端维护。当失败时能自动平衡。

### Kafka架构图

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20230201214157.png)

Kafka 体系架构包括若干 Producer(生产者)和Consumer(消费者)、若干 Broker(缓存代理) ，以及一个 ZooKeeper 集群，如图所示。

其中 ZooKeeper 是 Kafka 用来负责集群元数据的管理、控制器 的选举等操作的。Producer，consumer 实现 Kafka 注册的接口，数据从 producer 发送到 broker，broker承担一个中间缓存和分发的作用。broker 分发注册到系统中的 consumer 。broker 的作用类似于缓存，即活跃的数据和离线处理系统之间的缓存。

### 从设计模式来理解Kafka

对于设计模式来说，我们可以先用用发布订阅模式来解析Kafka:

- Broker 可以当作一个消息中心，用来存储消息；
- Producer 作为发布者，向消息中心发布信息，而此时Broker进行对信息中间缓存和分发注册到Consumer（也可以看作是Consumer的订阅过程）；
- Consumer 作为订阅者，在需要使用数据时，根据注册信息，在Broker中拿到信息。

当我们涉及到多个Broker即分布式时，就需要使用 ZooKeeper 集群对多个Broker进行维护。

### 主题（Topic）和分区（Partition）

Kafka 中的消息以 topic 为单位进行归类，**生产者发送到 Kafka 集群中的每一条消息都要指定一个主题**，而消费者负责订阅特定的主题并进行消费。

主题是一个逻辑上的概念，实际情况下，消息组的最小单位是一个分区（Partition）。**一个主题可以对应多个分区，一个分区只属于单个主题**。

当消息进行存储的时候，实际上是根据一个分区的**偏移值（offset）**进行存储，每一类消息在存储到主题中时，都是根据这个偏移值追加到对应分区的特定位置当中。同时，我们可以随时修改分区的数量来横向扩展消息储存容量。

### 消费者和分区的关系

每个消费者都对应一个特定的主题，而对于主题内的分区来说，默认是消费者瓜分分区，互相不影响。但也可以自定义为消费者共享分区，此时就形成了消息广播。

### 物理存储

主题和分区都是提供给上层用户的抽象，而在 Log 层面才有实际物理上的设计。

为了避免数据冗余和Log过大，在物理存储层面，Kafka采用了以下两个策略：

- 同一分区的多个副本必须分布在不同的broker中（解决数据冗余）
- 引入分段日志（LogSegment），各个段之间通过 offset 来保证有序性（解决单个Log过大）

### 多副本

上面提到了消息会存在副本，这是[分布式](https://baike.baidu.com/item/分布式/19276232)的特点。Kafka为分区引入了多副本(Replica)机制，通过增加副本数量可以提升容灾能力。同一分区的不同副本中保存的是相同的消息（在同一时刻，副本之间并非完全一样），副本之间是一主多从的关系，其中 leader 副本负责处理读写请求，follower 副本只负责与 leader 副本的消息同步。

由于多副本的机制和出现某个节点故障时的自动转移，Kafka 可以做到集群中某个 broker 失效时仍然能保证服务可用。

## Kafka应用实战

### saram

我们使用 go 操作 Kafka，这里使用比较常用的第三方库 sarama 来连接 Kafka 并且实现简单的发送消息和消费操作：

```go
package main

import (
	"fmt"
	"github.com/Shopify/sarama"
)

var config *sarama.Config

func main() {
	SendMsg()
	ConsumeMsg()
}

func SendMsg() {
	config = sarama.NewConfig()
	config.Producer.RequiredAcks = sarama.WaitForAll          // 发送完数据需要leader和follow都确认
	config.Producer.Partitioner = sarama.NewRandomPartitioner // 随机分配分区
	config.Producer.Return.Successes = true                   // 成功交付的消息将在success channel返回
	// 连接kafka
	client, err := sarama.NewSyncProducer([]string{"127.0.0.1:9092"}, config)
	if err != nil {
		fmt.Println("producer closed, err:", err)
		return
	}
	defer client.Close()

	// 构造一个消息
	msg := &sarama.ProducerMessage{}
	msg.Topic = "topic1"
	msg.Value = sarama.StringEncoder("this is a test log")

	// 发送消息
	pid, offset, err := client.SendMessage(msg)
	if err != nil {
		fmt.Println("send msg failed, err:", err)
		return
	}
	fmt.Printf("pid:%v offset:%v\n", pid, offset)
}
func ConsumeMsg() {
	consumer, err := sarama.NewConsumer([]string{"127.0.0.1:9092"}, nil)
	if err != nil {
		fmt.Printf("fail to start consumer, err:%v\n", err)
		return
	}
	partitionList, err := consumer.Partitions("topic1") // 根据topic取到所有的分区
	if err != nil {
		fmt.Printf("fail to get list of partition:err%v\n", err)
		return
	}
	fmt.Println(partitionList)
	for partition := range partitionList { // 遍历所有的分区
		// 针对每个分区创建一个对应的分区消费者
		pc, err := consumer.ConsumePartition("topic1", int32(partition), sarama.OffsetNewest)
		if err != nil {
			fmt.Printf("failed to start consumer for partition %d,err:%v\n", partition, err)
			return
		}
		defer pc.AsyncClose()
		// 异步从每个分区消费信息
		go func(sarama.PartitionConsumer) {
			for msg := range pc.Messages() {
				fmt.Printf("Partition:%d Offset:%d Key:%v Value:%v", msg.Partition, msg.Offset, msg.Key, msg.Value)
			}
		}(pc)
	}
}

```

### docker-compose

Kafka 方面，我们使用 docker-compose 来运行容器：

1. 编写 docker-compose.yml 文件

   ```yaml
   version: '3.7'
   services:
     zookeeper:
       image: wurstmeister/zookeeper
       volumes:
         - ./data:/data
       ports:
         - 2181:2181
   
     kafka:
       image: wurstmeister/kafka
       ports:
         - 9092:9092
       environment:
         KAFKA_BROKER_ID: 0
         KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://192.168.0.106:9092  #主机host，对外访问地址 
         KAFKA_CREATE_TOPICS: "topic1:2:0"   #kafka启动后初始化一个有2个partition(分区)0个副本名叫kafeidou的topic
         KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
         KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092
       volumes:
         - ./kafka-logs:/kafka
       depends_on:
         - zookeeper
   ```

2. shell里输入 `docker-compose up -d` 启动容器并且后台运行

### Kafka集群

如果只有一个服务器...

```yaml
version: '3.8'

services:
  zoo1:
    image: zookeeper
    container_name: zoo1
    hostname: zoo1
    ports:
      - 2181:2181
    volumes:
      - "./zoo1/data:/data"
      - "./zoo1/datalog:/datalog"
    environment:
      ZOO_MY_ID: 1
      ZOO_SERVERS: server.1=0.0.0.0:2888:3888;2181 server.2=zoo2:2888:3888;2181 server.3=zoo3:2888:3888;2181

  zoo2:
    image: zookeeper
    container_name: zoo2
    hostname: zoo2
    ports:
      - 2182:2181
    volumes:
      - "./zoo2/data:/data"
      - "./zoo2/datalog:/datalog"
    environment:
      ZOO_MY_ID: 2
      ZOO_SERVERS: server.1=zoo1:2888:3888;2181 server.2=0.0.0.0:2888:3888;2181 server.3=zoo3:2888:3888;2181

  zoo3:
    image: zookeeper
    container_name: zoo3
    hostname: zoo3
    ports:
      - 2183:2181
    volumes:
      - "./zoo3/data:/data"
      - "./zoo3/datalog:/datalog"
    environment:
      ZOO_MY_ID: 3
      ZOO_SERVERS: server.1=zoo1:2888:3888;2181 server.2=zoo2:2888:3888;2181 server.3=0.0.0.0:2888:3888;2181

  kafka1:
    image: wurstmeister/kafka
    restart: unless-stopped
    container_name: kafka1
    hostname: kafka1
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://192.168.0.106:9092    # 宿主机IP
      KAFKA_ADVERTISED_HOST_NAME: kafka1
      KAFKA_ADVERTISED_PORT: 9092
      KAFKA_ZOOKEEPER_CONNECT: "zoo1:2181"
    volumes:
      - "./kafka-logs:/kafka"

  kafka2:
    image: wurstmeister/kafka
    restart: unless-stopped
    container_name: kafka2
    hostname: kafka2
    ports:
      - "9093:9092"
    environment:
      KAFKA_BROKER_ID: 2
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://192.168.0.106:9093    # 宿主机IP
      KAFKA_ADVERTISED_HOST_NAME: kafka2
      KAFKA_ADVERTISED_PORT: 9093
      KAFKA_ZOOKEEPER_CONNECT: "zoo1:2181"
    volumes:
      - "./kafka-logs:/kafka"

  kafka3:
    image: wurstmeister/kafka
    restart: unless-stopped
    container_name: kafka3
    hostname: kafka3
    ports:
      - "9094:9092"
    environment:
      KAFKA_BROKER_ID: 3
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://192.168.0.106:9094   # 宿主机IP
      KAFKA_ADVERTISED_HOST_NAME: kafka3
      KAFKA_ADVERTISED_PORT: 9094
      KAFKA_ZOOKEEPER_CONNECT: "zoo1:2181"
    volumes:
      - "./kafka-logs:/kafka"

  kafka-manager: # Kafka 图形管理界面
    image: sheepkiller/kafka-manager:latest
    restart: unless-stopped
    container_name: kafka-manager
    hostname: kafka-manager
    ports:
      - "9000:9000"
    environment:
      ZK_HOSTS: zoo1:2181,zoo2:2182,zoo3:2183
      KAFKA_BROKERS: kafka1:9092,kafka2:9093,kafka3:9094
```

## RocketMQ理论基础

RocketMQ 经常被用在低延时场景下，例如秒杀，周年庆，电商场景中。

RocketMQ 相较于 Kafka，多了标签和生产者集群的观念，其他的类似。

<img src="https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20230220123853.png" style="zoom:67%;" />

### NameServer

NameServer 是 RocketMQ 的路由中心，用于 Broker 的注册和发现，类似 zookeeper,但比 zookeeper 性能更好，实现也更简单，因为 NameServer 集群中的服务器都是独立的，各实例间相互不进行信息通讯。

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20230220124135.png)

### 高级特性

RocketMQ 相较于 Kafka，多了一些高级特性来支持不同场景：

#### 事务场景

RocketMQ 通过事务保证了业务的最终一致性（这里指库存操作和写入消息队列是一个事务）：

<img src="https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20230220124700.png" style="zoom:50%;" />

具体实现（两阶段提交）：

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20230220125142.png)

#### 延迟发送

RocketMQ 可以设置定时来进行延迟发送，其内部实现流程为：

![](https://aeiblog-1301396258.cos.ap-chengdu.myqcloud.com/img/20230220143335.png)

简单来说就是从正常的生产消费流程中增加了日程队列和延时服务来在定时到期时重新新增一条 CommitLog。

#### 处理失败

RocketMQ 利用重试策略来实现消费失败的情况处理，例如设置重试此时，设置重试超限后延时投递消费重试等。



# 定时任务

单体定时任务：[如何优雅地实现定时任务？go定时任务库cron详解 - 腾讯云开发者社区-腾讯云 (tencent.com)](https://cloud.tencent.com/developer/article/1862333)

分布式定时任务：[几种主流的分布式定时任务，你知道哪些？ - 腾讯云开发者社区-腾讯云 (tencent.com)](https://cloud.tencent.com/developer/article/1950632)



# Elasticsearch

Elaticsearch，简称为 es， es 是一个开源的高扩展的分布式全文检索引擎，它可以近乎实时的存储、检索数据；本身扩展性很好，可以扩展到上百台服务器，处理海量数据。es 使用 Java 开发并使用 Lucene（Lucene 是一个开源的，**全文索引工具包**。有 **索引，搜索，分词** 等功能）作为其核心来实现所有索引和搜索的功能，但是它的目的是通过简单的 RESTful API 来隐藏 Lucene 的复杂性，从而让全文搜索变得简单。

> [快速上手搜索引擎的秘密武器——Lucene - 掘金 (juejin.cn)](https://juejin.cn/post/7021683796747485214)
