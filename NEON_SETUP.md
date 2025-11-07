# Neon 数据库设置指南

你已经选择使用 Neon 云端数据库，这样数据就不会存储在本地了。

## 步骤 1: 创建后端 .env 文件

在 `backend` 目录下创建 `.env` 文件：

```bash
cd backend
```

创建 `.env` 文件，内容如下：

```env
# Database Configuration - Neon Database
# 从 Neon Console 获取连接字符串: https://console.neon.tech/
DATABASE_URL=postgresql://user:password@host/database?sslmode=require

# JWT Configuration (使用下面的命令生成)
# 生成命令: openssl rand -hex 32
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email Service (Resend API) - 可选
# RESEND_API_KEY=your-resend-api-key-here
# FROM_EMAIL=noreply@yourdomain.com

# OpenAI API (AI 匹配功能) - 可选
# OPENAI_API_KEY=your-openai-api-key-here

# CORS Configuration
FRONTEND_URL=http://localhost:5173

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

**或者使用命令行快速创建：**

```bash
cd backend
cat > .env << 'EOF'
# 从 Neon Console 获取: https://console.neon.tech/
DATABASE_URL=postgresql://user:password@host/database?sslmode=require

# 生成命令: openssl rand -hex 32
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
FRONTEND_URL=http://localhost:5173
HOST=0.0.0.0
PORT=8000
EOF
```

## 步骤 2: 初始化 Neon 数据库表结构

运行初始化脚本：

```bash
cd database
./init_neon.sh
```

**或者手动运行：**

```bash
# 从 .env 文件中读取 DATABASE_URL
source backend/.env
psql "$DATABASE_URL" -f database/schema.sql
```

## 步骤 3: 启动后端

```bash
cd backend
source venv/bin/activate  # 如果还没有激活虚拟环境
python main.py
```

后端会在 `http://localhost:8000` 运行。

## 步骤 4: 启动前端

在新的终端窗口：

```bash
cd frontend
npm install  # 如果还没有安装依赖
npm run dev
```

前端会在 `http://localhost:5173` 运行。

## 验证数据库连接

你可以测试数据库连接：

```bash
# 从 .env 文件中读取 DATABASE_URL
source backend/.env
psql "$DATABASE_URL" -c "\dt"
```

这会列出所有表，确认表已经创建成功。

## 优势

使用 Neon 数据库的好处：
- ✅ 数据存储在云端，不占用本地空间
- ✅ 可以从任何地方访问
- ✅ 自动备份
- ✅ 免费 tier 足够 MVP 使用
- ✅ 无需本地安装 PostgreSQL

## 注意事项

- 确保你的 Neon 数据库连接字符串是正确的
- 如果连接失败，检查网络连接和 SSL 设置
- 在生产环境中，建议使用环境变量而不是硬编码密码

## 下一步

1. ✅ 创建 `.env` 文件
2. ✅ 运行数据库初始化
3. ✅ 启动后端服务器
4. ✅ 启动前端服务器
5. ✅ 测试应用！

