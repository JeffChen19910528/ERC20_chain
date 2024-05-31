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

# 设置帐户和私钥
my_address = web3.eth.accounts[0]  # 替换为你的以太坊地址
private_key = "0xcd01f5af3862e8a62ad667603c72079a6ea71511792795fc4d64d7b44790e677"  # 替换为你的私钥

# 仲裁者的地址和私钥
arbiter_address = web3.eth.accounts[1]  # 替换为仲裁者的以太坊地址
arbiter_private_key = "0xb8e25828167407c5777de3dc465dcf98974196c8ef001679731b3e0ac156a79e"  # 替换为仲裁者的私钥

# 指定Truffle项目路径
truffle_project_path = "truffleProject"

# 读取合约地址
with open(os.path.join(truffle_project_path, 'contractAddr.json')) as f:
    contract_addresses = json.load(f)

# 读取合约ABI
with open(os.path.join(truffle_project_path, 'build/contracts/MyToken.json')) as f:
    token_json = json.load(f)
    token_abi = token_json['abi']

with open(os.path.join(truffle_project_path, 'build/contracts/EscrowERC20.json')) as f:
    escrow_json = json.load(f)
    escrow_abi = escrow_json['abi']

# 获取合约地址
token_contract_address = contract_addresses['MyToken']['address']
escrow_contract_address = contract_addresses['EscrowERC20']['address']

# 创建ERC20和Escrow合约实例
token = web3.eth.contract(address=token_contract_address, abi=token_abi)
escrow = web3.eth.contract(address=escrow_contract_address, abi=escrow_abi)

# 示例操作：锁定资金
amount_to_lock = web3.to_wei(10, 'ether')  # 锁定的ERC20代币数量

# 获取最新的 nonce
nonce = web3.eth.get_transaction_count(my_address)

# 设置初始 gas price
initial_gas_price = web3.to_wei('5', 'gwei')

# 确保发起人已经批准Escrow合约可以转移ERC20代币
approve_tx = token.functions.approve(escrow_contract_address, amount_to_lock).build_transaction({
    'chainId': web3.eth.chain_id,
    'gas': 200000,
    'gasPrice': int(initial_gas_price),  # 设置合理的 gas price 并确保为整数
    'nonce': nonce,
})
signed_approve_tx = web3.eth.account.sign_transaction(approve_tx, private_key)
approve_tx_hash = web3.eth.send_raw_transaction(signed_approve_tx.rawTransaction)
print(f"Approve transaction hash: {approve_tx_hash.hex()}")
web3.eth.wait_for_transaction_receipt(approve_tx_hash)
print("Approve transaction confirmed")

# 增加 nonce 和 gas price
nonce += 1
gas_price = int(initial_gas_price * 1.1)

# 锁定资金
lock_tx = escrow.functions.lock().build_transaction({
    'chainId': web3.eth.chain_id,
    'gas': 200000,
    'gasPrice': int(gas_price),  # 增加 gas price 并确保为整数
    'nonce': nonce,
})
signed_lock_tx = web3.eth.account.sign_transaction(lock_tx, private_key)
lock_tx_hash = web3.eth.send_raw_transaction(signed_lock_tx.rawTransaction)
print(f"Lock transaction hash: {lock_tx_hash.hex()}")
web3.eth.wait_for_transaction_receipt(lock_tx_hash)
print("Lock transaction confirmed")

# 增加 nonce 和 gas price
nonce += 1
gas_price = int(gas_price * 1.1)

# 确认交易（由仲裁者进行）
confirm_nonce = web3.eth.get_transaction_count(arbiter_address)  # 获取仲裁者最新的 nonce
confirm_tx = escrow.functions.confirm().build_transaction({
    'chainId': web3.eth.chain_id,
    'gas': 200000,
    'gasPrice': int(gas_price),  # 增加 gas price 并确保为整数
    'nonce': confirm_nonce,
})
signed_confirm_tx = web3.eth.account.sign_transaction(confirm_tx, arbiter_private_key)
confirm_tx_hash = web3.eth.send_raw_transaction(signed_confirm_tx.rawTransaction)
print(f"Confirm transaction hash: {confirm_tx_hash.hex()}")
web3.eth.wait_for_transaction_receipt(confirm_tx_hash)
print("Confirm transaction confirmed")

# 获取最新的 nonce 和增加 gas price
nonce = web3.eth.get_transaction_count(my_address)
gas_price = int(gas_price * 1.1)

# 提交交易
commit_tx = escrow.functions.commit().build_transaction({
    'chainId': web3.eth.chain_id,
    'gas': 200000,
    'gasPrice': int(gas_price),  # 增加 gas price 并确保为整数
    'nonce': nonce,
})
signed_commit_tx = web3.eth.account.sign_transaction(commit_tx, private_key)
commit_tx_hash = web3.eth.send_raw_transaction(signed_commit_tx.rawTransaction)
print(f"Commit transaction hash: {commit_tx_hash.hex()}")
web3.eth.wait_for_transaction_receipt(commit_tx_hash)
print("Commit transaction confirmed")
