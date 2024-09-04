from web3 import Web3
import json
import os

# 连接到私有链节点
private_chain_url = "http://localhost:8545"  # 更改为您的私有链节点地址
web3 = Web3(Web3.HTTPProvider(private_chain_url))

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
token = web3.eth.contract(address=token_contract_address, abi=token_abi)

# 帳戶（從 Ganache 或其他來源獲取）
alice = web3.eth.accounts[0]
bob = web3.eth.accounts[1]

# 授權數量
amount = 10000

# Alice 批准 Bob 花費代幣
tx_hash = token.functions.approve(bob, amount).transact({'from': alice})
web3.eth.wait_for_transaction_receipt(tx_hash)

# Bob 從 Alice 的帳戶轉帳給自己
tx_hash = token.functions.transferFrom(alice, bob, amount).transact({'from': bob})
web3.eth.wait_for_transaction_receipt(tx_hash)

# 檢查 Bob 的餘額
balance = token.functions.balanceOf(alice).call()
print(f"Alice's balance: {balance}")

# 檢查 Bob 的餘額
balance = token.functions.balanceOf(bob).call()
print(f"Bob's balance: {balance}")
