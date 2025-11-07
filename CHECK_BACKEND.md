# 检查后端连接

如果看到 "Network Error"，请按以下步骤检查：

## 1. 检查后端是否运行

打开终端，运行：

```bash
cd backend
source venv/bin/activate
python main.py
```

你应该看到类似输出：
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## 2. 检查后端端口

后端应该运行在 `http://localhost:8000`

在浏览器中访问：`http://localhost:8000/docs` 应该能看到 FastAPI 的 API 文档页面。

## 3. 检查前端 API 配置

确保 `frontend/.env` 文件包含：
```env
VITE_API_URL=http://localhost:8000
```

如果没有这个文件，创建它：
```bash
cd frontend
echo "VITE_API_URL=http://localhost:8000" > .env
```

## 4. 重启前端开发服务器

修改 `.env` 后需要重启前端：

```bash
# 停止当前服务器 (Ctrl+C)
cd frontend
npm run dev
```

## 5. 检查浏览器控制台

打开浏览器开发者工具 (F12)，查看 Console 标签页，应该能看到详细的错误信息。

## 6. 常见问题

**问题**: "Network Error" 或 "ERR_NETWORK"
- **解决**: 确保后端正在运行 (`python main.py`)

**问题**: CORS 错误
- **解决**: 检查 `backend/.env` 中的 `FRONTEND_URL` 是否正确设置为 `http://localhost:5173`

**问题**: 连接超时
- **解决**: 检查防火墙设置，确保端口 8000 没有被阻止

## 7. 测试后端连接

在浏览器中直接访问：
- `http://localhost:8000/docs` - API 文档
- `http://localhost:8000/api/auth/check-school?email=test@usc.edu` - 测试端点

如果这些都能访问，说明后端正常运行。

