#!/bin/bash

# Slidev 幻灯片预览脚本
# 用途: 快速启动 Slidev 预览
# 使用: ./scripts/preview.sh <slides-file.md>

FILE="$1"

# 检查参数
if [ -z "$FILE" ]; then
    echo "用法: $0 <slides-file.md>"
    exit 1
fi

# 检查文件
if [ ! -f "$FILE" ]; then
    echo "错误: 文件不存在: $FILE"
    exit 1
fi

# 检查 Slidev
if ! command -v slidev &> /dev/null; then
    echo "错误: Slidev 未安装"
    echo "安装: npm install -g @slidev/cli"
    exit 1
fi

# 启动预览
FILE_DIR=$(dirname "$FILE")
FILE_NAME=$(basename "$FILE")

echo "🚀 启动 Slidev 预览..."
echo "📄 文件: $FILE_NAME"
echo ""

cd "$FILE_DIR" && slidev "$FILE_NAME" --open
