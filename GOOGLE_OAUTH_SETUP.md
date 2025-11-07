# Google OAuth 设置指南

## 为什么使用 Google OAuth？

- ✅ 简单易用，用户只需点击一次
- ✅ 自动验证邮箱（必须是 @usc.edu）
- ✅ 不需要用户记住密码
- ✅ 更安全的认证方式

## 设置步骤

### 1. 创建 Google OAuth 应用

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目或选择现有项目
3. 启用 **Google+ API**
4. 进入 **Credentials** → **Create Credentials** → **OAuth client ID**
5. 选择 **Web application**
6. 配置：
   - **Name**: University Dating App
   - **Authorized JavaScript origins**: 
     - `http://localhost:5173` (开发环境)
     - `https://your-domain.com` (生产环境)
   - **Authorized redirect URIs**:
     - `http://localhost:5173` (开发环境)
     - `https://your-domain.com` (生产环境)

### 2. 获取 Client ID

创建后，你会得到：
- **Client ID** (例如: `123456789-abc.apps.googleusercontent.com`)
- **Client Secret** (后端需要，但前端只需要 Client ID)

### 3. 配置前端

在 `frontend/.env` 文件中添加：

```env
VITE_GOOGLE_CLIENT_ID=your-google-client-id-here.apps.googleusercontent.com
```

### 4. 配置后端（可选）

在 `backend/.env` 文件中添加（用于服务器端验证）：

```env
GOOGLE_CLIENT_ID=your-google-client-id-here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret-here
```

**注意**: 对于 MVP，前端验证就足够了。后端验证是可选的，但更安全。

### 5. 安装依赖

前端依赖已经添加到 `package.json`，运行：

```bash
cd frontend
npm install
```

后端依赖已经添加到 `requirements.txt`，运行：

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

## 工作流程

1. 用户点击 "Sign in with Google"
2. Google 弹出登录窗口
3. 用户选择 Google 账户
4. 应用收到 Google ID token
5. 后端验证 token 并检查邮箱是否为 `@usc.edu`
6. 如果是 USC 邮箱：
   - 新用户：创建账户，跳转到个人信息填写
   - 老用户：直接登录
7. 如果不是 USC 邮箱：显示错误

## 安全说明

- ✅ 只有 `@usc.edu` 邮箱可以注册
- ✅ Google 自动验证邮箱真实性
- ✅ 不需要存储用户密码
- ✅ 使用 JWT token 进行后续认证

## 测试

1. 使用你的 USC Google 账户测试登录
2. 尝试使用非 USC 邮箱，应该被拒绝
3. 新用户应该跳转到个人信息填写页面
4. 老用户应该直接进入应用

## 故障排除

**问题**: Google 登录按钮不显示
- 检查 `VITE_GOOGLE_CLIENT_ID` 是否正确设置
- 检查 Google Cloud Console 中的授权域名是否正确

**问题**: "Invalid token" 错误
- 检查后端 `GOOGLE_CLIENT_ID` 是否与前端一致
- 检查 token 是否过期（通常 1 小时）

**问题**: "Only USC students allowed" 错误
- 确保使用的 Google 账户邮箱是 `@usc.edu` 结尾
- 检查后端 `validate_usc_email` 函数

