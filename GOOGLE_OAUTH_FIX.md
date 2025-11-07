# Google OAuth 配置修复

## 问题
你看到错误：`The given origin is not allowed for the given client ID`

这是因为你的前端运行在 `http://localhost:5176`，但 Google Cloud Console 中只配置了其他端口。

## 解决方案

### 1. 更新 Google Cloud Console 配置

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 进入 **APIs & Services** → **Credentials**
3. 找到你的 OAuth 2.0 Client ID（`834866041297-lbm2t1v0ipl3c2qusfcme0jdf1ue69lb.apps.googleusercontent.com`）
4. 点击编辑
5. 在 **Authorized JavaScript origins** 中添加：
   ```
   http://localhost:5173
   http://localhost:5174
   http://localhost:5175
   http://localhost:5176
   http://127.0.0.1:5173
   http://127.0.0.1:5174
   http://127.0.0.1:5175
   http://127.0.0.1:5176
   ```
6. 在 **Authorized redirect URIs** 中添加相同的 URL
7. 点击 **Save**

### 2. 后端 CORS 已更新

后端现在已经允许所有常见的 Vite 开发端口（5173-5176）。

### 3. 重启前端

修改 Google Cloud Console 后，**不需要重启前端**，但建议清除浏览器缓存或使用无痕模式测试。

## 验证

1. 清除浏览器缓存或使用无痕模式
2. 访问 `http://localhost:5176/register`
3. 点击 Google 登录按钮
4. 应该可以正常工作了

## 如果还有问题

检查浏览器控制台，确保没有其他错误。如果仍有问题，请提供具体的错误信息。

