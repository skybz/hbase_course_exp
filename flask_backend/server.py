from flask import Flask, request, jsonify
from flask_cors import CORS
import happybase

app = Flask(__name__)
CORS(app)

# 连接 HBase 数据库
connection = happybase.Connection('172.17.0.2', port=9090)
connection.open()
table = connection.table('my_table') 
print("Connected to HBase")

# 接收前端请求并处理搜索
@app.route('/search')
def search():
    query_string = request.args.get('query')  # 获取查询参数
    print(query_string)

    if query_string is None or query_string == '':
        results = {}
        for key, row_data in table.scan():  # 遍历表中的每一行
            row_key = key.decode()  # 将字节型的行键解码为字符串
            results[row_key] = {k.decode('utf-8'): v.decode('utf-8') for k, v in row_data.items()}
    else:
        results = {}
        for key, row_data in table.scan():  # 遍历表中的每一行
            row_key = key.decode()  # 将字节型的行键解码为字符串

            # 使用 row() 方法获取整行数据
            row_data = table.row(row_key)  # 获取整行数据，包括所有列

            # 如果行中包含特定子串，将行键和对应数据存储在结果中
            if any(query_string in value.decode('utf-8') for value in row_data.values()):
                results[row_key] = {k.decode('utf-8'): v.decode('utf-8') for k, v in row_data.items()}

    # 在循环中将字典中的值提取出来，以显示在返回结果中
    return_result = [f"链接: {key}, Data: {data}" for key, data in results.items()]

    return jsonify(return_result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
