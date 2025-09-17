# 部署指南

## 🚀 部署方案

本项目采用前后端分离架构，需要分别部署前端和后端服务。

## 📱 前端部署到 Vercel

### 1. 准备工作
- 确保前端代码在 `frontend/` 目录
- 已配置 `vercel.json` 文件
- 已设置环境变量 `REACT_APP_API_URL`

### 2. 部署步骤

#### 方法一：通过 Vercel CLI
```bash
# 安装 Vercel CLI
npm i -g vercel

# 进入前端目录
cd frontend

# 登录 Vercel
vercel login

# 部署
vercel

# 设置环境变量
vercel env add REACT_APP_API_URL
# 输入你的后端API地址，如：https://your-api.railway.app/api/v1
```

#### 方法二：通过 GitHub 集成
1. 将代码推送到 GitHub 仓库
2. 在 Vercel 官网连接 GitHub 仓库
3. 设置构建配置：
   - Framework Preset: Create React App
   - Build Command: `npm run build`
   - Output Directory: `build`
4. 设置环境变量：`REACT_APP_API_URL`

### 3. 环境变量配置
```
REACT_APP_API_URL=https://your-backend-api.railway.app/api/v1
```

## 🔧 后端部署选项

### 选项1：Railway（推荐）

#### 1. 准备工作
- 确保后端代码在 `backend/` 目录
- 已配置 `railway.json` 文件

#### 2. 部署步骤
1. 访问 [Railway.app](https://railway.app)
2. 使用 GitHub 登录
3. 点击 "New Project" -> "Deploy from GitHub repo"
4. 选择你的仓库
5. 选择 `backend` 目录作为根目录
6. Railway 会自动检测 Python 项目并部署

#### 3. 环境变量配置
```
ALLOWED_ORIGINS=https://your-frontend-app.vercel.app
```

### 选项2：Render

#### 1. 准备工作
- 确保后端代码在 `backend/` 目录
- 已配置 `render.yaml` 文件

#### 2. 部署步骤
1. 访问 [Render.com](https://render.com)
2. 连接 GitHub 仓库
3. 选择 "New Web Service"
4. 选择你的仓库和 `backend` 目录
5. 配置：
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`

### 选项3：Heroku

#### 1. 准备工作
- 确保后端代码在 `backend/` 目录
- 已配置 `Procfile` 和 `runtime.txt`

#### 2. 部署步骤
```bash
# 安装 Heroku CLI
# 登录 Heroku
heroku login

# 创建应用
heroku create your-todo-api

# 设置环境变量
heroku config:set ALLOWED_ORIGINS=https://your-frontend-app.vercel.app

# 部署
git subtree push --prefix backend heroku main
```

## 🔄 完整部署流程

### 第一步：部署后端
1. 选择上述任一后端部署平台
2. 部署后端API
3. 记录API地址（如：`https://your-api.railway.app`）

### 第二步：部署前端
1. 更新 `frontend/vercel.json` 中的 `REACT_APP_API_URL`
2. 部署到 Vercel
3. 在 Vercel 中设置环境变量

### 第三步：配置CORS
1. 在后端平台设置环境变量 `ALLOWED_ORIGINS`
2. 值为你的 Vercel 域名

## 🌐 域名配置

### 自定义域名
1. 在 Vercel 中添加自定义域名
2. 更新后端 CORS 配置
3. 更新前端环境变量

## 📊 监控和维护

### 日志查看
- **Vercel**: Dashboard -> Functions -> View Function Logs
- **Railway**: Dashboard -> Deployments -> View Logs
- **Render**: Dashboard -> Services -> Logs

### 性能监控
- 使用 Vercel Analytics
- 后端平台提供的监控工具

## 🛠️ 故障排除

### 常见问题

1. **CORS 错误**
   - 检查后端 CORS 配置
   - 确认前端域名在允许列表中

2. **API 连接失败**
   - 检查环境变量配置
   - 确认后端服务正常运行

3. **构建失败**
   - 检查依赖版本
   - 查看构建日志

### 调试步骤
1. 检查前端网络请求
2. 查看后端日志
3. 验证环境变量
4. 测试API端点

## 📝 更新部署

### 前端更新
```bash
cd frontend
npm run build
vercel --prod
```

### 后端更新
- 推送代码到 GitHub
- 平台会自动重新部署

---

**部署完成后，你的应用将可以通过以下地址访问：**
- 前端：`https://your-app.vercel.app`
- 后端API：`https://your-api.railway.app`
- API文档：`https://your-api.railway.app/docs`
