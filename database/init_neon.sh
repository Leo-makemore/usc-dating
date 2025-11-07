#!/bin/bash

# Initialize Neon Database with schema
# This script runs the schema.sql on your Neon database

set -e

echo "🚀 正在初始化 Neon 数据库..."

# Neon database connection string
NEON_DB_URL="${NEON_DB_URL:-postgresql://neondb_owner:npg_0UiRFOK1qGml@ep-plain-leaf-a4h7kg5v-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require}"

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

