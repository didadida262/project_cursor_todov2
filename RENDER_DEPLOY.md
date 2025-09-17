# Render 部署指南

## 🚀 快速部署到 Render

### 第一步：准备 GitHub 仓库
1. 确保代码已推送到 GitHub
2. 确保 `backend/` 目录包含所有必要文件

### 第二步：注册 Render
1. 访问 [https://render.com](https://render.com)
2. 点击 "Get Started for Free"
3. 选择 "Sign up with GitHub"
4. 授权 Render 访问你的 GitHub 账户

### 第三步：创建 Web Service
1. 在 Render 控制台，点击 "New +"
2. 选择 "Web Service"
3. 选择 "Build and deploy from a Git repository"
4. 选择你的 GitHub 仓库

### 第四步：配置服务
```
Name: todo-api
Root Directory: backend
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: python main.py
```

### 第五步：设置环境变量
在 "Environment Variables" 部分添加：
```
ALLOWED_ORIGINS = https://your-frontend-app.vercel.app
```

### 第六步：部署
1. 点击 "Create Web Service"
2. 等待部署完成（5-10分钟）
3. 获取你的 API URL（格式：https://todo-api-xxx.onrender.com）

### 第七步：测试
访问以下 URL 测试：
- 健康检查：`https://your-api-url.onrender.com/health`
- API 文档：`https://your-api-url.onrender.com/docs`
- API 端点：`https://your-api-url.onrender.com/api/v1/todos`

### 第八步：更新前端
在 Vercel 中设置环境变量：
```
REACT_APP_API_URL = https://your-api-url.onrender.com/api/v1
```

## ⚠️ 注意事项

1. **冷启动**：Render 免费计划有冷启动，首次访问可能需要几秒钟
2. **睡眠**：免费计划在无活动时会睡眠，首次访问会唤醒
3. **域名**：Render 会提供 `.onrender.com` 域名

## 🔧 故障排除

### 部署失败
1. 检查 Root Directory 是否设置为 `backend`
2. 检查 Build Command 是否正确
3. 查看 Render 的构建日志

### API 无法访问
1. 检查环境变量设置
2. 检查 CORS 配置
3. 确认服务状态为 "Live"

### 数据库问题
1. Render 会自动创建 SQLite 数据库
2. 数据在每次重新部署时会重置
3. 如需持久化，可考虑使用 Render 的 PostgreSQL

## 📞 获取帮助

- Render 文档：https://render.com/docs
- Render 社区：https://community.render.com
- 检查部署日志：Render 控制台 -> 你的服务 -> Logs
