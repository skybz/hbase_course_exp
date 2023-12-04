# 使用基于Debian的官方Docker镜像
FROM debian:bullseye

# 安装Java、SSH、wget等必要的工具
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    openssh-server \
    wget \
    rsync \
    tar \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 设置JAVA_HOME环境变量
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:${PATH}"

# 下载并安装Hadoop
RUN wget https://mirrors.tuna.tsinghua.edu.cn/apache/hadoop/common/hadoop-3.3.1/hadoop-3.3.1.tar.gz && \
    tar -xzvf hadoop-3.3.1.tar.gz && \
    mv hadoop-3.3.1 /usr/local/hadoop && \
    rm hadoop-3.3.1.tar.gz

# 设置Hadoop环境变量
ENV HADOOP_HOME=/usr/local/hadoop
ENV PATH="$HADOOP_HOME/sbin:$PATH"

# 下载并安装HBase
RUN wget https://mirrors.tuna.tsinghua.edu.cn/apache/hbase/2.4.17/hbase-2.4.17-bin.tar.gz && \
    tar -xzvf hbase-2.4.17-bin.tar.gz && \
    mv hbase-2.4.17 /usr/local/hbase && \
    rm hbase-2.4.17-bin.tar.gz

# 设置HBase环境变量
ENV HBASE_HOME=/usr/local/hbase
ENV PATH="$HBASE_HOME/bin:$PATH"

# 运行SSH服务器
RUN mkdir /var/run/sshd

# 开放SSH端口
EXPOSE 22

# 启动SSH服务
CMD ["/usr/sbin/sshd", "-D"]

# 暴露HBase服务使用的端口
EXPOSE 2181 16000 16020
