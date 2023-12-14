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

    results = {}
    return_result = []
    for key, _ in table.scan():  # 只需要行键，不需要数据内容
        row_key = key.decode()  # 将字节型的行键解码为字符串

        # 使用 row() 方法获取指定行键的数据
        row_data = table.row(row_key, columns=[b'cf1:title'])  # 获取指定列的数据

        # 如果 cf1:title 列存在并包含特定子串，将行键和对应数据存储在结果中
        if b'cf1:title' in row_data and query_string in row_data[b'cf1:title'].decode('utf-8'):
            results[row_key] = row_data

    # 在循环中将字节串解码为可读的字符串
    for key, data in results.items():
        
        # 将数据中的字节串转换为字节形式的字符串，然后解码为可读的字符串
        decoded_data = {k.decode('utf-8'): str(v).encode().decode('unicode-escape').encode('raw_unicode_escape').decode() for k, v in data.items()}

        return_result.append(f"链接: {row_key}, Data: {decoded_data}")


    
    return return_result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
