import json

# 存储所有 Spider 输出的数据的列表
all_data = []

# 读取每个 Spider 输出的文件
with open('output.json', 'r', encoding='utf-8') as f:
    # 读取 JSON 数据
    all_data = json.load(f)

# 将合并后的数据写入到一个新文件
with open('merged_output.json', 'w', encoding='utf-8') as merged_file:
    json.dump(all_data, merged_file, ensure_ascii=False, indent=2)

print('合并完成！')
