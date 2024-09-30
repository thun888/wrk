import re
import json
import os  # 新增：用于获取环境变量
import requests

# 单位转换表，转换为 MB
unit_conversion = {
    "B": 1e-6,     # Bytes to MB
    "KB": 1e-3,    # Kilobytes to MB
    "MB": 1,       # Megabytes to MB
    "GB": 1e3,     # Gigabytes to MB
    "TB": 1e6      # Terabytes to MB
}

# 读取 wrk 输出文件
with open('temp.txt', 'r') as file:
    content = file.read()

# 提取 URL
url_pattern = r'Running \d+m test @ (\S+)'
url_match = re.search(url_pattern, content)
url = url_match.group(1) if url_match else None

# 提取 read 数据，支持不同单位
data_pattern = r'(\d+(\.\d+)?)\s*(B|KB|MB|GB|TB) read'
data_match = re.search(data_pattern, content)

if data_match:
    data_size = float(data_match.group(1))  # 提取数字部分
    unit = data_match.group(3)              # 提取单位
    data_in_mb = data_size * unit_conversion[unit]  # 转换为 MB
else:
    data_in_mb = 0.0  # 如果匹配失败，默认值

# 创建 JSON 数据
data = {
    "url": url,
    "data_size_MB": data_in_mb
}

# 从环境变量中获取保存数据的 URL 和 Token
save_url = os.getenv('SAVEURL', 'https://default-save-url.com/savedata')
save_token = os.getenv('SAVETOKEN', '')

# 发送带有认证 Token 的 POST 请求
headers = {
    'Authorization': f'Bearer {save_token}'
}

response = requests.post(save_url, json=data, headers=headers)

# 输出结果以便在Action日志中查看
# print(f"Sent data: {data}")
print(f"Response status: {response.status_code}")
print(f"Response content: {response.text}")
