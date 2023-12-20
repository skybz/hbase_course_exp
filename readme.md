大数据系统课程实验 2023
skybz 

#### docker运行 终端目录在当前目录

```shell
docker build -t hadoop-hbase-image .
docker run -d -p 2222:22 -p 9090:9090 --name hadoop-hbase-container hadoop-hbase-image
docker ps //看id
docker exec -it <id> /bin/bash //ssh连接进去用终端 
```

#### 启动hadoop和hbase
```shell
hadoop namenode -format
start-dfs.sh
start-yarn.sh
start-hbase.sh  //(输yes)
hbase-daemon.sh start thrift
```

### 启动python程序连接hbase
```shell
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container_name_or_id //查对应的ip

#插入数据
cd data_insert
python hello.py
cd ..

python ./flask_backend/server.py
#用浏览器打开前端的页面即可

```
