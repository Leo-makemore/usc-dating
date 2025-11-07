#!/bin/bash

# Initialize Neon Database with schema
# This script runs the schema.sql on your Neon database

set -e

echo "🚀 正在初始化 Neon 数据库..."

# Neon database connection string
# 优先从环境变量读取，如果没有则从 backend/.env 读取
if [ -z "$NEON_DB_URL" ] && [ -f "../backend/.env" ]; then
    export NEON_DB_URL=$(grep "^DATABASE_URL=" ../backend/.env | cut -d '=' -f2- | tr -d '"' | tr -d "'")
fi

if [ -z "$NEON_DB_URL" ]; then
    echo "❌ 错误: 未找到数据库连接字符串"
    echo "请设置环境变量 NEON_DB_URL 或在 backend/.env 中配置 DATABASE_URL"
    exit 1
fi

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCHEMA_FILE="$SCRIPT_DIR/schema.sql"

if [ ! -f "$SCHEMA_FILE" ]; then
    echo "❌ 找不到 schema.sql 文件: $SCHEMA_FILE"
    exit 1
fi

echo "📝 正在运行 schema.sql..."
psql "$NEON_DB_URL" -f "$SCHEMA_FILE"

echo "✅ Neon 数据库初始化完成！"
echo ""
echo "现在你可以启动后端服务器了。"

