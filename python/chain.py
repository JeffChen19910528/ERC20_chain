"""Shared Web3 connection and contract-loading helpers.

Both demo scripts need a connected Web3 instance and the deployed MyToken
contract; this module is the single place that knows how to build them.
"""

import json
import os

from web3 import Web3

import config


def get_web3():
    web3 = Web3(Web3.HTTPProvider(config.RPC_URL))
    if not web3.is_connected():
        raise ConnectionError(f"Failed to connect to the Ethereum node at {config.RPC_URL}")
    return web3


def load_contract(web3, contract_name=None):
    contract_name = contract_name or config.CONTRACT_NAME

    with open(os.path.join(config.TRUFFLE_PROJECT_DIR, "contractAddr.json")) as f:
        addresses = json.load(f)

    artifact_path = os.path.join(config.TRUFFLE_PROJECT_DIR, "build", "contracts", f"{contract_name}.json")
    with open(artifact_path) as f:
        artifact = json.load(f)

    address = addresses[contract_name]["address"]
    return web3.eth.contract(address=address, abi=artifact["abi"])
