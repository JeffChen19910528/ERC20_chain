"""Demo: approve + transferFrom happy path (formerly index.py)."""

from chain import get_web3, load_contract


def main():
    web3 = get_web3()
    token = load_contract(web3)

    alice, bob = web3.eth.accounts[0], web3.eth.accounts[1]
    amount = 10000

    tx_hash = token.functions.approve(bob, amount).transact({"from": alice})
    web3.eth.wait_for_transaction_receipt(tx_hash)

    tx_hash = token.functions.transferFrom(alice, bob, amount).transact({"from": bob})
    web3.eth.wait_for_transaction_receipt(tx_hash)

    print(f"Alice's balance: {token.functions.balanceOf(alice).call()}")
    print(f"Bob's balance: {token.functions.balanceOf(bob).call()}")


if __name__ == "__main__":
    main()
