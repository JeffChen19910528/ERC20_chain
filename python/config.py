"""Central configuration for the Python scripts.

All values can be overridden with environment variables so the scripts work
against different chains/paths without editing code.
"""

import os

RPC_URL = os.environ.get("ETH_RPC_URL", "http://localhost:8545")
TRUFFLE_PROJECT_DIR = os.environ.get("TRUFFLE_PROJECT_DIR", "truffleProject")
KEYSTORE_DIR = os.environ.get("KEYSTORE_DIR", os.path.join("data", "keystore"))
CONTRACT_NAME = os.environ.get("CONTRACT_NAME", "MyToken")
