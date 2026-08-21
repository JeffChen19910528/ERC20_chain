"""Decrypt a geth keystore file into a raw private key.

Replaces the old key.py / decrypt_keystore.py duplicates. Unlike the
original decrypt_keystore.py, the password is never hardcoded and is read
with getpass so it isn't echoed or left in shell history; the private key is
only written to disk if --output is given.
"""

import argparse
import getpass
import os

from web3 import Web3

import config


def list_keystore_files(keystore_dir):
    return sorted(f for f in os.listdir(keystore_dir) if os.path.isfile(os.path.join(keystore_dir, f)))


def choose_keystore_file(keystore_dir):
    files = list_keystore_files(keystore_dir)
    if not files:
        raise FileNotFoundError(f"No keystore files found in {keystore_dir}")

    print("Keystore files:")
    for idx, name in enumerate(files, start=1):
        print(f"{idx}. {name}")

    choice = int(input("Select a keystore file by number: ")) - 1
    return os.path.join(keystore_dir, files[choice])


def main():
    parser = argparse.ArgumentParser(description="Decrypt a geth keystore file")
    parser.add_argument("--keystore-dir", default=config.KEYSTORE_DIR, help="Folder to pick a keystore file from")
    parser.add_argument("--keystore-file", help="Path to a specific keystore file (skips the interactive picker)")
    parser.add_argument("--output", help="Save the decrypted private key to this file (omit to only print it)")
    args = parser.parse_args()

    keystore_path = args.keystore_file or choose_keystore_file(args.keystore_dir)

    with open(keystore_path) as f:
        keystore = f.read()

    password = getpass.getpass("Keystore password: ")

    try:
        private_key = Web3().eth.account.decrypt(keystore, password)
    except ValueError as exc:
        print(f"Error: {exc}")
        return

    print("Decryption successful.")
    print(f"Private key: {private_key.hex()}")

    if args.output:
        with open(args.output, "w") as f:
            f.write(private_key.hex())
        print(f"Private key saved to {args.output}")


if __name__ == "__main__":
    main()
