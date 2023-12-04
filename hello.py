import happybase

def connect_to_hbase():
    # HBase连接信息
    hbase_host = '172.17.0.2'  # 替换为您HBase容器的IP地址
    hbase_port = 9090  # HBase默认端口

    # 建立HBase连接
    connection = happybase.Connection(host=hbase_host, port=hbase_port)

    # 在连接上打开一个表
    table_name = b'my_table'  # 替换为您要连接的HBase表名
    table = connection.table(table_name)

    # 示例：执行一些操作
    # 获取一行数据
    row_key = b'row_key_here'  # 替换为您要获取的行键
    data = table.row(row_key)

    # 打印获取到的数据
    print(f"Data for row key {row_key}: {data}")

    # 关闭连接
    connection.close()

connect_to_hbase()