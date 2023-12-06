import happybase
import json

def create_table(connection, table_name, column_family):
    families = {column_family: dict()}
    connection.create_table(table_name, families)
    print(f"Table '{table_name}' created with column family '{column_family}'.")

def delete_table(connection, table_name):
    if table_name.encode() in connection.tables():
        connection.delete_table(table_name, disable=True)
        print(f"Table '{table_name}' deleted.")



def upload_to_hbase(json_file_path, table_name, column_family):

    # 连接 HBase
    connection = happybase.Connection('172.17.0.2', port=9090)  # ip 用readme中指令查 
    connection.open()
    print("Connected to HBase")
    
    # Delete existing table (if any)
    delete_table(connection, table_name)

    # Create a new table
    create_table(connection, table_name, column_family)

    # 获取表对象
    table = connection.table(table_name)

    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            for record in data:
                # print(type(record.get('link')), type(record.get('title')), type(record.get('publish_date')))
                # print(record.get('link'), record.get('title'), record.get('publish_date'))
                row_key = record.get('link')
                data_values = {
                    'cf1:title': record.get('title'),
                    'cf1:publish_date': record.get('publish_date')
                }
                table.put(row_key, data_values)

    except Exception as e:
        print(f"Error: {e}")

    # 关闭连接
    connection.close()
    print("Connection to HBase closed")


def retrieve_and_print_data(table_name, column_family):
    connection = happybase.Connection('172.17.0.2', port=9090)  # ip 用readme中指令查 
    connection.open()
    table = connection.table(table_name)

    for key, data in table.scan():
        print(f"Row Key: {key.decode('utf-8')}")
        for column, value in data.items():
            print(f"{column.decode('utf-8')}: {value.decode('utf-8')}")

    connection.close()

if __name__ == "__main__":
    json_file_path = 'output.json'
    table_name = 'my_table'
    column_family = 'cf1'

    upload_to_hbase(json_file_path, table_name, column_family)
    print("Data uploaded to HBase.")

    retrieve_and_print_data(table_name, column_family)
