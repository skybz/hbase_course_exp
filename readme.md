大数据系统课程实验 2023
skybz 

运行之前将自己的ssh密钥 id_rsa.pub放在./docker/sshkey中

#### docker运行 终端目录在当前目录

'''
docker build -t hadoop-hbase-image .
docker run -d -p 2222:22 --name hadoop-hbase-container hadoop-hbase-image
docker ps //看id
docker exec -it <id> /bin/bash //ssh连接进去用终端 
'''

hadoop namenode -format
start-dfs.sh