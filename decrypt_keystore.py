from web3 import Web3
import json

# 读取keystore文件
keystore_path = "data/keystore/UTC--2024-05-29T12-07-43.134782608Z--6eac03869a87c759d4ddc1405c0c96829dbe7c24"  # 更改为你的keystore文件路径
with open(keystore_path) as keyfile:
    encrypted_key = json.load(keyfile)

# 输入密码
password = "123456"  # 更改为创建keystore文件时使用的密码

# 解密keystore文件以获取私钥
private_key = Web3().eth.account.decrypt(encrypted_key, password)
private_key_hex = private_key.hex()

print(f"私钥: {private_key_hex}")
