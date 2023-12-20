# 使用基于Debian的官方Docker镜像，并替换为国内镜像源
FROM debian:bullseye

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list

# 安装Java、SSH、wget等必要的工具
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    openssh-server \
    wget \
    rsync \
    tar \
    && apt-get clean \
# 设置JAVA_HOME环境变量
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:${PATH}"

# 下载并安装Hadoop
RUN wget https://mirrors.ustc.edu.cn/apache/hadoop/common/hadoop-3.3.5/hadoop-3.3.5.tar.gz && \
    tar -xzvf hadoop-3.3.5.tar.gz && \
    mv hadoop-3.3.5 /usr/local/hadoop && \
    rm hadoop-3.3.5.tar.gz

# 设置Hadoop环境变量
ENV HADOOP_HOME=/usr/local/hadoop
ENV PATH="$HADOOP_HOME/bin:$PATH"
ENV PATH="$HADOOP_HOME/sbin:$PATH"

# 复制hadoop配置
COPY ./docker/hadoop_config/hadoop-env.sh /usr/local/hadoop/etc/hadoop/hadoop-env.sh
COPY ./docker/hadoop_config/yarn-env.sh /usr/local/hadoop/etc/hadoop/yarn-env.sh
COPY ./docker/hadoop_config/core-site.xml /usr/local/hadoop/etc/hadoop/core-site.xml
COPY ./docker/hadoop_config/hdfs-site.xml /usr/local/hadoop/etc/hadoop/hdfs-site.xml
COPY ./docker/hadoop_config/mapred-site.xml /usr/local/hadoop/etc/hadoop/mapred-site.xml
COPY ./docker/hadoop_config/yarn-site.xml /usr/local/hadoop/etc/hadoop/yarn-site.xml
COPY ./docker/hadoop_config/start-dfs.sh /usr/local/hadoop/sbin/start-dfs.sh 
COPY ./docker/hadoop_config/stop-dfs.sh /usr/local/hadoop/sbin/stop-dfs.sh 
COPY ./docker/hadoop_config/start-yarn.sh /usr/local/hadoop/sbin/start-yarn.sh 
COPY ./docker/hadoop_config/stop-yarn.sh /usr/local/hadoop/sbin/stop-yarn.sh 


# 下载并安装HBase
RUN wget https://mirrors.tuna.tsinghua.edu.cn/apache/hbase/2.4.17/hbase-2.4.17-bin.tar.gz && \
    tar -xzvf hbase-2.4.17-bin.tar.gz && \
    mv hbase-2.4.17 /usr/local/hbase && \
    rm hbase-2.4.17-bin.tar.gz

# 设置HBase环境变量
ENV HBASE_HOME=/usr/local/hbase
ENV PATH="$HBASE_HOME/bin:$PATH"

# 复制hadoop配置
COPY ./docker/hbase_config/hbase-env.sh /usr/local/hbase/conf/hbase-env.sh
COPY ./docker/hbase_config/hbase-site.xml /usr/local/hbase/conf/hbase-site.xml

# 运行SSH服务器
RUN mkdir /var/run/sshd

# 执行 SSH 密钥生成
RUN mkdir -p ~/.ssh && ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

# 允许 SSH 访问
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# 开放SSH端口
EXPOSE 22

# 启动SSH服务
CMD ["/usr/sbin/sshd", "-D"]

# 暴露HBase服务使用的端口
EXPOSE 9090 
