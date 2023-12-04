大数据系统课程实验 2023
skybz 

#### docker运行 终端目录在当前目录

```shell
docker build -t hadoop-hbase-image .
docker run -d -p 2222:22 --name hadoop-hbase-container hadoop-hbase-image
docker ps //看id
docker exec -it <id> /bin/bash //ssh连接进去用终端 
```

#### 启动hadoop和hbase
```shell
hadoop namenode -format
start-dfs.sh
start-hbase.sh
```