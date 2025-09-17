# Vercel 全栈部署指南

## 🚀 在 Vercel 上部署前后端

Vercel 支持前端 + Serverless Functions，完美适合我们的 Todo 应用。

### 第一步：准备项目

项目已经配置好了 Vercel 支持：
- `frontend/` - React 前端
- `api/todos.py` - Python API 函数
- `frontend/vercel.json` - Vercel 配置

### 第二步：安装 Vercel CLI（可选）

```bash
# 安装 Vercel CLI
npm install -g vercel

# 或者使用 yarn
yarn global add vercel
```

### 第三步：部署到 Vercel

#### 方法一：通过 Vercel 网站（推荐）

1. **访问 Vercel 官网**
   - 打开 [https://vercel.com](https://vercel.com)
   - 点击 "Sign up" 或 "Login"

2. **连接 GitHub**
   - 选择 "Continue with GitHub"
   - 授权 Vercel 访问你的 GitHub 账户

3. **导入项目**
   - 点击 "New Project"
   - 选择你的 `project_cursor_todov2` 仓库
   - 点击 "Import"

4. **配置项目**
   - **Framework Preset**: 选择 "Other" 或 "Create React App"
   - **Root Directory**: 留空（使用根目录）
   - **Build Command**: `cd frontend && npm run build`
   - **Output Directory**: `frontend/build`
   - **Install Command**: `cd frontend && npm install`

5. **环境变量设置**
   - 在 "Environment Variables" 部分添加：
   - `REACT_APP_API_URL` = `/api`

6. **部署**
   - 点击 "Deploy"
   - 等待部署完成（通常 2-5 分钟）

#### 方法二：通过 Vercel CLI

```bash
# 进入项目根目录
cd project_cursor_todov2

# 登录 Vercel
vercel login

# 部署项目
vercel

# 设置环境变量
vercel env add REACT_APP_API_URL
# 输入值：/api

# 重新部署
vercel --prod
```

### 第四步：验证部署

部署完成后，你会得到一个 Vercel 域名，格式如：
`https://your-project-name.vercel.app`

#### 测试前端
访问：`https://your-project-name.vercel.app`
- 应该看到 Todo 应用界面

#### 测试 API
访问以下端点测试 API：

1. **健康检查**
   ```
   https://your-project-name.vercel.app/api/health
   ```
   应该返回：
   ```json
   {
     "status": "healthy",
     "message": "服务运行正常"
   }
   ```

2. **获取任务列表**
   ```
   https://your-project-name.vercel.app/api/todos
   ```
   应该返回空数组：
   ```json
   []
   ```

3. **创建任务**
   ```bash
   curl -X POST https://your-project-name.vercel.app/api/todos \
     -H "Content-Type: application/json" \
     -d '{"title": "测试任务", "completed": false}'
   ```

### 第五步：项目结构说明

```
project_cursor_todov2/
├── frontend/                 # React 前端
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vercel.json          # Vercel 配置
├── api/                     # Vercel Functions
│   └── todos.py             # Python API 函数
└── README.md
```

### 第六步：API 端点说明

所有 API 端点都以 `/api` 开头：

- `GET /api/health` - 健康检查
- `GET /api/todos` - 获取任务列表
- `POST /api/todos` - 创建任务
- `PUT /api/todos/{id}` - 更新任务
- `DELETE /api/todos/{id}` - 删除任务
- `DELETE /api/todos/completed` - 删除已完成任务
- `DELETE /api/todos/all` - 清空所有任务

### 第七步：环境变量配置

在 Vercel 控制台中设置：

1. 进入你的项目
2. 点击 "Settings" 标签
3. 点击 "Environment Variables"
4. 添加：
   - **Name**: `REACT_APP_API_URL`
   - **Value**: `/api`
   - **Environment**: Production, Preview, Development

### 第八步：自定义域名（可选）

1. 在 Vercel 控制台，点击 "Domains"
2. 点击 "Add Domain"
3. 输入你的域名
4. 按照指示配置 DNS

### 第九步：监控和维护

#### 查看日志
1. 在 Vercel 控制台，点击 "Functions"
2. 选择 `api/todos.py`
3. 查看 "Logs" 标签

#### 查看分析
1. 在 Vercel 控制台，点击 "Analytics"
2. 查看访问统计和性能数据

#### 重新部署
- 推送代码到 GitHub，Vercel 会自动重新部署
- 或使用 CLI：`vercel --prod`

### 第十步：故障排除

#### 常见问题

1. **API 函数不工作**
   - 检查 `api/todos.py` 文件是否存在
   - 查看 Vercel Functions 日志
   - 确保 Python 版本兼容

2. **前端无法连接 API**
   - 检查环境变量 `REACT_APP_API_URL` 是否正确设置
   - 确保 API 路径以 `/api` 开头

3. **数据库问题**
   - Vercel Functions 使用临时文件系统
   - 数据在每次函数调用时可能重置
   - 如需持久化，考虑使用外部数据库

4. **构建失败**
   - 检查 `frontend/package.json` 中的依赖
   - 查看 Vercel 的构建日志
   - 确保 Node.js 版本兼容

#### 调试步骤

1. **检查部署日志**
   - Vercel 控制台 -> Deployments -> 查看构建日志

2. **测试 API 端点**
   - 使用 curl 或 Postman 测试各个端点

3. **检查网络请求**
   - 浏览器开发者工具 -> Network 标签

4. **查看函数日志**
   - Vercel 控制台 -> Functions -> 查看日志

### 第十一步：性能优化

#### 前端优化
- 使用 Vercel 的图片优化
- 启用 Edge Functions
- 使用 CDN 加速

#### 后端优化
- 函数冷启动优化
- 数据库连接池
- 缓存策略

## 🎉 部署完成！

部署成功后，你的 Todo 应用将完全免费运行在 Vercel 上，包括：
- ✅ 前端 React 应用
- ✅ 后端 Python API
- ✅ 自动 HTTPS
- ✅ 全球 CDN
- ✅ 自动部署

---

**访问你的应用：`https://your-project-name.vercel.app`**
