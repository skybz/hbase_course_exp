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

    # 使用查询字符串查询 HBase 数据
    result = table.row(query_string.encode())  # 假设查询字符串作为行键

    # 将查询结果转换为 JSON 格式并返回给前端
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
