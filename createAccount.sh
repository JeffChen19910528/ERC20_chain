#!/bin/bash

# Set the directory variable
DIR="$PWD/data/keystore"

# Check the number of accounts in the keystore directory
num_accounts=$(ls -1q "$DIR" | wc -l)

# If no accounts are present, clear the password.txt file before adding a new password
if [ "$num_accounts" -eq 0 ]; then
    echo "No accounts found. Clearing password.txt file."
    > password.txt  # This empties the password.txt file
fi

# Create account
read -p "password: " pwd
geth --datadir "data" account new --password <(echo $pwd)

# Append the password to the password.txt file
printf "$pwd\n" >> password.txt

# Run initialization script
./init.sh

echo "Account creation and initialization completed."