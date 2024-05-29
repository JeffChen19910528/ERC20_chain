#!/bin/bash

# Define directory path
DIR="$PWD/data/keystore"

# Prepare addresses file and genesis JSON
echo "Extracting addresses from keystore files..."
> address.txt  # Clear or create the address file
jsonobj='{'

# Loop through all files in the directory
for file in "$DIR"/*; do
    # Extract address using jq, prepend "0x" and add to address.txt
    addr=$(jq -r '.address' "$file")
    echo "0x$addr" >> address.txt

    # Append data to JSON object string
    jsonobj+='"0x'"$addr"'":{"balance":"200000000000000000000"},'
done

# Correctly close the JSON object by removing the last comma and adding a closing brace
jsonobj="${jsonobj%,}}"
echo "$jsonobj"

# Rewrite genesis file with the new allocation object
echo "Updating genesis.json with new allocation..."
jq --argjson val "$jsonobj" '.alloc = $val' genesis.json > temp_genesis.json
mv temp_genesis.json genesis.json

# Initialize geth with the updated genesis block
echo "Initializing geth with new genesis block..."
geth --datadir data init genesis.json

echo "Done!"