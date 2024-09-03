import os
from web3 import Web3

# 连接到以太坊节点
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))  # 使用默认的本地节点地址

# 指定資料夾路徑
folder_path = '/home/jeff/private_chain/data/keystore/'

# 列出資料夾內的所有檔案
files = os.listdir(folder_path)

# 列出檔案清單供使用者選擇
print("Keystore files in the folder:")
for idx, file_name in enumerate(files):
    print(f"{idx + 1}. {file_name}")

# 讓使用者選擇要解密的keystore文件
file_index = int(input("Enter the number of the keystore file you want to decrypt: ")) - 1

# 指定選取的keystore檔案路徑
selected_file_path = os.path.join(folder_path, files[file_index])

# 讀取選取的keystore檔案
with open(selected_file_path, 'r') as f:
    keystore = f.read()

# 输入 keystore 的密码
password = input("Enter your keystore password: ")

# 使用 Web3.eth.accounts.decrypt 方法解密私钥
try:
    private_key = w3.eth.account.decrypt(keystore, password)
    print("Decryption successful.")
    print("Your private key is:", private_key.hex())

    # 將私鑰儲存到文本檔案中
    output_file_path = f"private_key.txt"
    with open(output_file_path, 'w') as output_file:
        output_file.write(private_key.hex())
        print(f"Private key saved to {output_file_path}")
except ValueError as e:
    print("Error:", e)