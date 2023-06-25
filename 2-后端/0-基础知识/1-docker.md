## Docker

#### 挂载本地目录到容器

[docker](https://so.csdn.net/so/search?q=docker&spm=1001.2101.3001.7020)可以支持把一个宿主机上的目录挂载到镜像里。

```groovy
docker run -it -v /home/dock/Downloads:/usr/Downloads ubuntu64 /bin/bash
```

通过-v参数，冒号前为宿主机目录，必须为绝对路径，冒号后为镜像内挂载的路径。

```bash
docker run --name slavemysql -d -p 3308:3306 -e MYSQL_ROOT_PASSWORD=root -v ~/test/mysql_test/slave/data:/var/lib/mysql -v ~/test/mysql_test/slave/conf/my.cnf:/etc/mysql/my.cnf mysql:5.7
```

#### 进入容器进行命令行操作

**docker exec ：**在运行的容器中执行命令

```
docker exec [OPTIONS] CONTAINER COMMAND [ARG...]
```

OPTIONS说明：

- **-i :**即使没有附加也保持STDIN 打开
- **-t :**分配一个伪终端

例子：进入一个mysql容器执行终端命令

```bash
docker exec -it mysql-xxx bash
```

## docker-compose

1. 编写 docker-compose.yml 文件
2. shell里输入 `docker-compose up -d` 启动容器并且后台运行 （-d 是后台运行）

[Docker Compose | 菜鸟教程 (runoob.com)](https://www.runoob.com/docker/docker-compose.html)
