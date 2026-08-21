# ERC20 Private Chain

A private geth chain (chain id `10`) used to deploy and experiment with a
custom `MyToken` ERC20 contract, including a deliberately vulnerable
`unsafeTransferFrom` function used to demonstrate a `transferFrom` race
condition.

## Layout

```
.
├── initproject.sh          # one-time setup: create data/, chmod scripts
├── createAccount.sh        # create a new geth account, append its password
├── deleteAccount.sh        # remove an account and its password entry
├── init.sh                 # rebuild genesis.json alloc from keystore addresses, geth init
├── start.sh                 # start geth with all accounts unlocked (HTTP RPC on :8545)
├── backup_geth.sh / restore_geth.sh
├── genesis.json             # chain genesis config (alloc is rewritten by init.sh)
├── requirements.txt          # Python deps (web3.py)
├── python/
│   ├── config.py             # RPC URL / paths, overridable via env vars
│   ├── chain.py               # shared Web3 connection + contract loader
│   ├── decrypt_keystore.py    # decrypt a geth keystore file to a private key
│   ├── demo_approve_transfer.py  # approve + transferFrom happy path
│   └── demo_race_condition.py    # concurrent unsafeTransferFrom race demo
└── truffleProject/
    ├── contracts/MyToken.sol
    ├── migrations/
    ├── compile.sh             # truffle compile + migrate, writes contractAddr.json
    └── truffle-config.js
```

## Setup

```bash
./initproject.sh                 # creates data/, makes scripts executable
./createAccount.sh                # repeat for each account you want (e.g. 3)
./init.sh                          # writes genesis.json alloc + geth init
./start.sh                         # starts geth, RPC on http://localhost:8545
```

In another terminal, deploy the contract:

```bash
cd truffleProject
npm install
./compile.sh                      # truffle compile + migrate --network live
```

## Python scripts

```bash
pip install -r requirements.txt
```

All scripts read configuration from environment variables (see
`python/config.py`), so they don't need editing to point at a different RPC
endpoint or truffle project path:

| Variable              | Default                | Purpose                          |
|-----------------------|-------------------------|-----------------------------------|
| `ETH_RPC_URL`          | `http://localhost:8545` | geth JSON-RPC endpoint            |
| `TRUFFLE_PROJECT_DIR`  | `truffleProject`        | where `contractAddr.json`/`build` live |
| `KEYSTORE_DIR`         | `data/keystore`         | default folder for keystore files |
| `CONTRACT_NAME`        | `MyToken`                | contract to load                  |

Run from the project root:

```bash
python python/demo_approve_transfer.py
python python/demo_race_condition.py
python python/decrypt_keystore.py --keystore-file data/keystore/<file>
```

`decrypt_keystore.py` prompts for the password (never hardcoded, never
echoed) and only writes the private key to disk if you pass `--output`.

## Security notes

- `address.txt`, `password.txt`, `private_key.txt` and `*.log` are
  generated locally by the scripts above and are gitignored — never commit
  them.
- This chain is for local experimentation only (fake balances, chain id
  `10`). `unsafeTransferFrom` in `MyToken.sol` is intentionally vulnerable
  and exists only to demonstrate the race condition in
  `python/demo_race_condition.py`; don't reuse it in a real deployment.
- `truffleProject/execute.js` references an `EscrowERC20` contract that
  isn't part of this repo yet — it's a work-in-progress example, not a
  working script.
