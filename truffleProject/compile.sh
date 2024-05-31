#!/bin/bash

# Define output file name
OUTPUT_FILE="contractAddr.json"

# Execute truffle compile
echo "Compiling contracts..."
truffle compile

# Check if compilation was successful
if [ $? -ne 0 ]; then
    echo "Compilation failed. Exiting."
    exit 1
fi

# Execute truffle migrate
echo "Migrating contracts..."
truffle migrate --reset --network live

# Check if migration was successful
if [ $? -ne 0 ]; then
    echo "Migration failed. Exiting."
    exit 1
fi

# Read all contract files in the build/contracts directory
CONTRACTS_DIR="build/contracts"
echo "Reading contract addresses..."

# Initialize a temporary file to store contract addresses
TEMP_FILE=$(mktemp)
echo "{" > $TEMP_FILE

# Loop through each contract file, extract the address, and write it to the temporary file
for file in $CONTRACTS_DIR/*.json; do
    CONTRACT_NAME=$(basename $file .json)

    # Check if the contract file contains deployed contracts (usually has 'networks' field)
    if jq -e '.networks | length > 0' $file > /dev/null; then
        ADDRESS=$(jq -r '.networks | to_entries[] | select(.value.address != null) | .value.address' $file)
        
        if [ -n "$ADDRESS" ]; then
            echo "  \"$CONTRACT_NAME\": {" >> $TEMP_FILE
            echo "    \"address\": \"$ADDRESS\"" >> $TEMP_FILE
            echo "  }," >> $TEMP_FILE
        fi
    fi
done

# Remove the trailing comma from the last line and add the closing brace
truncate -s-2 $TEMP_FILE
echo -e "\n}" >> $TEMP_FILE

# Move the temporary file to the final output file
mv $TEMP_FILE $OUTPUT_FILE

echo "Contract addresses have been written to $OUTPUT_FILE."
