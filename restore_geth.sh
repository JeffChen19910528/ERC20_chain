#!/bin/bash

# Define the backup directory and restore directory
BACKUP_DIR="$HOME/backup"  # Backup directory in the user's home directory
RESTORE_DIR="data"  # Directory to restore the geth data

# List all backup files and assign a number to each
echo "Available backup files:"
backup_files=($BACKUP_DIR/*.tar.gz)
for i in "${!backup_files[@]}"; do
  echo "[$i] ${backup_files[$i]}"
done

# Prompt user to select a backup file by number
echo -n "Enter the number of the backup file to restore: "
read FILE_NUMBER

# Check if the input is a valid number
if ! [[ "$FILE_NUMBER" =~ ^[0-9]+$ ]]; then
  echo "Invalid input! Please enter a valid number."
  exit 1
fi

# Check if the selected number is within range
if [ "$FILE_NUMBER" -lt 0 ] || [ "$FILE_NUMBER" -ge "${#backup_files[@]}" ]; then
  echo "Invalid number! Please select a number from the list."
  exit 1
fi

# Full path to the selected backup file
BACKUP_PATH="${backup_files[$FILE_NUMBER]}"

# Check if the backup file exists
if [ ! -f "$BACKUP_PATH" ]; then
  echo "Backup file $BACKUP_PATH does not exist!"
  exit 1
fi

# Create the restore directory if it does not exist
if [ ! -d "$RESTORE_DIR" ]; then
  echo "Restore directory $RESTORE_DIR does not exist. Creating it..."
  mkdir -p "$RESTORE_DIR"
  if [ $? -eq 0 ]; then
    echo "Restore directory created successfully."
  else
    echo "Failed to create restore directory!"
    exit 1
  fi
fi

# Stop geth service (uncomment and adjust the command as needed)
# pkill geth

# Extract the backup file to the restore directory
echo "Restoring backup from $BACKUP_PATH to $RESTORE_DIR ..."
tar -xzvf "$BACKUP_PATH" -C "$RESTORE_DIR"

if [ $? -eq 0 ]; then
  echo "Restore successful! Data restored to $RESTORE_DIR"
else
  echo "Restore failed!"
  exit 1
fi

# Restart geth service (uncomment and adjust the command as needed)
# geth --datadir "$RESTORE_DIR" --networkid 10 --http --http.addr 0.0.0.0 --http.vhosts "*" --http.api "db,net,eth,web3,personal" --http.corsdomain "*" --snapshot=false --allow-insecure-unlock --unlock "$accounts" --password "password.txt" console 2> 1.log &

echo "Restore script completed."
