# Netlify 部署指南

## 🚀 免费全栈部署到 Netlify

Netlify 提供免费的静态网站托管和 Serverless Functions，完美适合我们的 Todo 应用。

### 第一步：准备项目

项目已经配置好了 Netlify 支持：
- `netlify.toml` - Netlify 配置文件
- `netlify/functions/todos.js` - API 函数
- `frontend/` - React 前端

### 第二步：注册 Netlify

1. 访问 [https://netlify.com](https://netlify.com)
2. 点击 "Sign up"
3. 选择 "Sign up with GitHub"
4. 授权 Netlify 访问你的 GitHub 账户

### 第三步：部署项目

#### 方法一：通过 GitHub 连接（推荐）

1. 在 Netlify 控制台，点击 "New site from Git"
2. 选择 "GitHub"
3. 选择你的 `project_cursor_todov2` 仓库
4. 配置部署设置：
   - **Build command**: `cd frontend && npm run build`
   - **Publish directory**: `frontend/build`
   - **Functions directory**: `netlify/functions`
5. 点击 "Deploy site"

#### 方法二：通过 Netlify CLI

```bash
# 安装 Netlify CLI
npm install -g netlify-cli

# 登录
netlify login

# 部署
netlify deploy --prod
```

### 第四步：配置环境变量

在 Netlify 控制台：
1. 进入你的站点
2. 点击 "Site settings"
3. 点击 "Environment variables"
4. 添加：
   - `REACT_APP_API_URL` = `/api`

### 第五步：测试部署

部署完成后，你会得到一个 Netlify 域名，格式如：
`https://your-site-name.netlify.app`

测试以下端点：
- 前端应用：`https://your-site-name.netlify.app`
- API 健康检查：`https://your-site-name.netlify.app/api/health`
- API 文档：`https://your-site-name.netlify.app/api/todos`

### 第六步：自定义域名（可选）

1. 在 Netlify 控制台，点击 "Domain settings"
2. 点击 "Add custom domain"
3. 输入你的域名
4. 按照指示配置 DNS

## 🔧 项目结构

```
project_cursor_todov2/
├── frontend/                 # React 前端
│   ├── src/
│   ├── public/
│   └── package.json
├── netlify/
│   └── functions/
│       └── todos.js         # API 函数
├── netlify.toml             # Netlify 配置
└── README.md
```

## 📊 功能特性

### 前端功能
- ✅ React 应用
- ✅ 响应式设计
- ✅ 现代化 UI
- ✅ 状态管理

### 后端功能
- ✅ Serverless Functions
- ✅ SQLite 数据库
- ✅ RESTful API
- ✅ CORS 支持

### 部署特性
- ✅ 免费托管
- ✅ 自动 HTTPS
- ✅ 全球 CDN
- ✅ 自动部署
- ✅ 无服务器架构

## 🛠️ 故障排除

### 构建失败
1. 检查 `frontend/package.json` 中的依赖
2. 查看 Netlify 的构建日志
3. 确保 Node.js 版本兼容

### API 函数不工作
1. 检查 `netlify/functions/todos.js` 文件
2. 查看 Netlify Functions 日志
3. 确保函数路径正确

### 数据库问题
1. Netlify Functions 使用临时文件系统
2. 数据在每次函数调用时可能重置
3. 如需持久化，考虑使用外部数据库

## 📈 性能优化

### 前端优化
- 使用 Netlify 的图片优化
- 启用 Brotli 压缩
- 使用 CDN 加速

### 后端优化
- 函数冷启动优化
- 数据库连接池
- 缓存策略

## 🔄 更新部署

### 自动部署
- 推送代码到 GitHub
- Netlify 自动重新部署

### 手动部署
```bash
netlify deploy --prod
```

## 📞 获取帮助

- Netlify 文档：https://docs.netlify.com
- Netlify 社区：https://community.netlify.com
- 查看部署日志：Netlify 控制台 -> Deploys

---

**部署完成后，你的应用将完全免费运行在 Netlify 上！**
