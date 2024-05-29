#!/bin/bash

# Read addresses from address.txt
mapfile -t addr < "address.txt"
#echo "${addr[@]}"

# Get password.txt lines and count
mapfile -t lines < "password.txt"
num_accounts=${#lines[@]}  # Get the number of accounts from the length of lines array

# Build a comma-separated list of account indexes
accounts=$(seq 0 $((num_accounts - 1)) | paste -sd ',' -)
#echo $accounts

# Start Ethereum using geth with specified configuration
geth --datadir "data" --networkid 10 --http \
     --http.addr 0.0.0.0 --http.vhosts "*" --http.api "db,net,eth,web3,personal" \
     --http.corsdomain "*" --snapshot=false --allow-insecure-unlock \
     --unlock "$accounts" --password "password.txt" console 2> 1.log

echo "Geth is running..."