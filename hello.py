import happybase

def connect_to_hbase():
    try:
        # 连接 HBase
        connection = happybase.Connection('172.17.0.2', port=9090)  # ip 用readme中指令查 
        connection.open()
        print("Connected to HBase")
        
        # 创建表
        table_name = 'my_table'
        families = {
            'cf1': dict(),  # 列族名称
            # 可以添加更多的列族，例如 'cf2': dict(), 'cf3': dict()
        }

        if table_name.encode() not in connection.tables():
            connection.create_table(table_name, families)
            print(f"Table '{table_name}' created")
        else:
            print(f"Table '{table_name}' already exists")
        
        # 获取表对象
        table = connection.table(table_name)

        # 插入数据
        row_key = 'row1'
        data = {
            'cf1:column1': 'value1',
            'cf1:column2': 'value2',
            # 可以添加更多列，例如 'cf1:column3': 'value3'
        }
        table.put(row_key, data)
        print("Data inserted")

        # 获取数据
        row = table.row(row_key)
        print(f"Retrieved row '{row_key}': {row}")

        # 关闭连接
        connection.close()
        print("Connection to HBase closed")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    connect_to_hbase()
