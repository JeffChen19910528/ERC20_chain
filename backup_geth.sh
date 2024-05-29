#!/bin/bash

# Define the data directory
DATA_DIR="data"  # Your geth data directory

# Define the backup directory in the user's home directory
BACKUP_DIR="$HOME/backup"

# Get the current timestamp
TIMESTAMP=$(date +"%Y%m%d%H%M%S")

# Create the backup file name
BACKUP_FILE="$BACKUP_DIR/ethereum_backup_$TIMESTAMP.tar.gz"

# Stop geth service (uncomment and adjust the command as needed)
# pkill geth

# Check if the data directory exists
if [ ! -d "$DATA_DIR" ]; then
  echo "Data directory $DATA_DIR does not exist!"
  exit 1
fi

# Check if the backup directory exists, create if not
if [ ! -d "$BACKUP_DIR" ]; then
  echo "Backup directory $BACKUP_DIR does not exist. Creating it..."
  mkdir -p "$BACKUP_DIR"
  if [ $? -eq 0 ]; then
    echo "Backup directory created successfully."
  else
    echo "Failed to create backup directory!"
    exit 1
  fi
fi

# Backup the data directory
echo "Backing up data directory $DATA_DIR to $BACKUP_FILE ..."
tar -czvf "$BACKUP_FILE" -C "$DATA_DIR" .

if [ $? -eq 0 ]; then
  echo "Backup successful! Backup file saved as $BACKUP_FILE"
else
  echo "Backup failed!"
  exit 1
fi

# Restart geth service (uncomment and adjust the command as needed)
# geth --datadir "$DATA_DIR" --networkid 10 --http --http.addr 0.0.0.0 --http.vhosts "*" --http.api "db,net,eth,web3,personal" --http.corsdomain "*" --snapshot=false --allow-insecure-unlock --unlock "$accounts" --password "password.txt" console 2> 1.log &

echo "Backup script completed."
