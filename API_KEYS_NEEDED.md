# 需要的 API Keys

## 当前状态

✅ **数据库已配置** - 使用 Neon DB（PostgreSQL）
- 连接字符串已在 `backend/.env` 中配置
- 无需额外操作

## 可选但推荐的 API Keys

### 1. OpenAI API Key（用于 AI 匹配推荐）

**用途**: 使用 AI embeddings 进行更智能的匹配推荐

**获取方式**:
1. 访问 [OpenAI Platform](https://platform.openai.com/)
2. 注册/登录账户
3. 进入 **API Keys** 页面
4. 点击 **Create new secret key**
5. 复制 API key

**配置**:
在 `backend/.env` 文件中添加：
```env
OPENAI_API_KEY=sk-your-openai-api-key-here
```

**注意**: 
- 如果没有 OpenAI API key，系统会使用基础匹配算法（基于共同兴趣、学校、年级等）
- AI 匹配是可选的，基础匹配功能已经可以工作

### 2. Resend API Key（用于邮件验证）

**用途**: 发送邮箱验证邮件

**获取方式**:
1. 访问 [Resend](https://resend.com/)
2. 注册/登录账户
3. 进入 **API Keys** 页面
4. 创建新的 API key
5. 复制 API key

**配置**:
在 `backend/.env` 文件中添加：
```env
RESEND_API_KEY=re_your-resend-api-key-here
FROM_EMAIL=noreply@yourdomain.com
```

**注意**:
- 如果没有配置，系统会在控制台打印验证链接（开发模式）
- 邮件验证是可选的，用户仍然可以注册和使用

## 当前必需配置

**后端** (`backend/.env`):
```env
DATABASE_URL=postgresql://neondb_owner:npg_0UiRFOK1qGml@ep-plain-leaf-a4h7kg5v-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
SECRET_KEY=your-secret-key-here
HOST=0.0.0.0
PORT=8000
FRONTEND_URL=http://localhost:5176
```

**前端** (`frontend/.env`):
```env
VITE_API_URL=http://localhost:8000
```

## 总结

**最小配置**（可以立即使用）:
- ✅ 数据库连接（已配置）
- ✅ JWT Secret Key（需要设置）

**推荐配置**（更好的体验）:
- ✅ 数据库连接
- ✅ JWT Secret Key
- ⚠️ OpenAI API Key（AI 匹配推荐）
- ⚠️ Resend API Key（邮件验证）

## 下一步

1. 确保 `backend/.env` 中有 `SECRET_KEY`
2. （可选）添加 `OPENAI_API_KEY` 用于 AI 匹配
3. （可选）添加 `RESEND_API_KEY` 用于邮件验证
4. 启动后端和前端
5. 开始注册和测试！

