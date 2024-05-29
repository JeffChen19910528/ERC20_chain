#!/bin/bash

# The filename as the first argument of the script
FILES="password.txt"

# Define a function to display the current content of the file
display_file_content() {
    echo "Current file content:"
    nl -ba "$FILES"  # The nl command is used to add line numbers and print the content of the file
    echo "----------------------------"
}

# Check if the file exists, if not, create it
if [ ! -f "$FILES" ]; then
    echo "File does not exist, creating new file: $FILES"
    touch "$FILES"
fi

# Display the initial content
display_file_content

# Define a function to delete the content of a specified line number
delete_line() {
    sed -i "${1}d" "$FILES"
}

# Specify the folder path
DIR_PATH="$PWD/data/keystore"

# Initialize an array of addresses and a map from addresses to file paths
declare -a ADDRESS_ARRAY
declare -A ADDRESS_TO_FILE_MAP

# Check if the folder exists
if [ ! -d "$DIR_PATH" ]; then
    echo "Folder does not exist: $DIR_PATH"
    exit 1
fi

# Read each JSON file in the folder
for FILE in "$DIR_PATH"/*; do
    # Use the jq tool to read the address value from each JSON file
    ADDRESS=$(jq -r '.address' "$FILE" 2>/dev/null)

    # Check if the address is non-empty
    if [ -n "$ADDRESS" ] && [ "$ADDRESS" != "null" ]; then
        ADDRESS_ARRAY+=("$ADDRESS")
        ADDRESS_TO_FILE_MAP["$ADDRESS"]="$FILE"
    fi
done

# Display all the addresses retrieved
echo "All retrieved addresses:"
for i in "${!ADDRESS_ARRAY[@]}"; do
    echo "$((i + 1))) ${ADDRESS_ARRAY[$i]}"
done

# Prompt the user to enter the address code to delete
read -p "Please enter the address code to delete: " INDEX
let INDEX=INDEX-1

# Validate the input as a number and within a valid range
if ! [[ $INDEX =~ ^[0-9]+$ ]] || [[ "$INDEX" -lt 0 || "$INDEX" -ge "${#ADDRESS_ARRAY[@]}" ]]; then
    echo "Please enter a valid address code."
    exit 1
fi

# Get the file path to be deleted
DELETE_FILE="${ADDRESS_TO_FILE_MAP["${ADDRESS_ARRAY[$INDEX]}"]}"

# Delete the file
if [ -n "$DELETE_FILE" ]; then
    echo "Deleting file: $DELETE_FILE"
    rm "$DELETE_FILE"
    echo "File deleted."
else
    echo "No file associated with the selected address was found."
fi

# Call the function to delete the content at the specified line number
delete_line $((INDEX + 1))

# Finally, display the file's final content again
display_file_content
echo "Update completed."
./init.sh
