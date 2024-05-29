#!/bin/bash

# 定義輸出文件名
OUTPUT_FILE="contractAddr.json"

# 執行 truffle compile
echo "Compiling contracts..."
truffle compile

# 檢查編譯是否成功
if [ $? -ne 0 ]; then
    echo "Compilation failed. Exiting."
    exit 1
fi

# 執行 truffle migrate
echo "Migrating contracts..."
truffle migrate --reset --network live

# 檢查遷移是否成功
if [ $? -ne 0 ]; then
    echo "Migration failed. Exiting."
    exit 1
fi

# 讀取 build/contracts 目錄下的所有合約文件
CONTRACTS_DIR="build/contracts"
echo "Reading contract addresses..."

# 清空並初始化 JSON 文件
echo "{" > $OUTPUT_FILE

# 迴圈讀取每個合約文件，提取地址並寫入 JSON 文件
for file in $CONTRACTS_DIR/*.json; do
    CONTRACT_NAME=$(basename $file .json)

    # 確認合約文件包含遷移的合約（通常會有'networks'字段）
    if jq -e '.networks | length > 0' $file > /dev/null; then
        ADDRESS=$(jq -r '.networks | to_entries[] | select(.value.address != null) | .value.address' $file)
        
        if [ -n "$ADDRESS" ]; then
            echo "  \"$CONTRACT_NAME\": \"$ADDRESS\"," >> $OUTPUT_FILE
        fi
    fi
done

# 去掉最後一行的逗號，並添加結束大括號
sed -i '' '$ s/,$//' $OUTPUT_FILE
echo "}" >> $OUTPUT_FILE

echo "Contract addresses have been written to $OUTPUT_FILE."
