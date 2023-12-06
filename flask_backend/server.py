from flask import Flask, request, jsonify
import happybase

app = Flask(__name__)

# 连接 HBase 数据库
connection = happybase.Connection('172.17.0.2')
table = connection.table('my_table')  # 将 'your_table_name' 替换为你的 HBase 表名称

# 接收前端请求并处理搜索
@app.route('/search')
def search():
    query_string = request.args.get('query')  # 获取查询参数
    
    print(query_string)
    # 查询 HBase 表中行键包含特定子串的数据
    results = {}
    return_result = []
    for key, data in table.scan():
        row_key = key.decode()  # 将字节型的行键解码为字符串
        if query_string in row_key:
            results[row_key] = data  # 将符合条件的行键和对应数据存储在结果中

    # 输出查询结果
    for key, data in results.items():
        return_result.append(f"Row key: {key}, Data: {data}")
    
    print(return_result)
    return return_result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
