# Vercel 部署完整指南

## 📋 概述

本指南将帮助你将Todo应用完整部署到Vercel平台，包括前端React应用和后端API函数。

## 🏗️ 项目架构

- **前端**: React应用 (静态文件)
- **后端**: Python Serverless Functions (API)
- **数据库**: 内存数据库 (适合演示)

## 🚀 部署步骤

### 第一步：准备工作

1. **确保项目结构正确**
```
project_cursor_todov2/
├── frontend/           # React前端应用
│   ├── package.json
│   ├── src/
│   └── public/
├── api/                # Python API函数
│   ├── todos.py        # 主API函数
│   └── requirements.txt
├── vercel.json         # Vercel配置文件
└── README.md
```

2. **安装Vercel CLI**
```bash
npm install -g vercel
```

3. **登录Vercel账户**
```bash
vercel login
```

### 第二步：本地测试

1. **测试前端构建**
```bash
cd frontend
yarn install
yarn build
```

2. **验证构建输出**
确保`frontend/build`目录存在且包含静态文件。

### 第三步：部署到Vercel

#### 方法1：使用Vercel CLI（推荐）

```bash
# 在项目根目录执行
vercel

# 按照提示配置：
# ? Set up and deploy "project_cursor_todov2"? [Y/n] Y
# ? Which scope do you want to deploy to? Your Account
# ? Link to existing project? [y/N] N
# ? What's your project's name? todo-app
# ? In which directory is your code located? ./
```

#### 方法2：使用Vercel Dashboard

1. 访问 [Vercel Dashboard](https://vercel.com/dashboard)
2. 点击 "New Project"
3. 导入GitHub仓库
4. 配置项目设置：
   - **Framework Preset**: Other
   - **Root Directory**: `./`
   - **Build Command**: `cd frontend && yarn build`
   - **Output Directory**: `frontend/build`
   - **Install Command**: `cd frontend && yarn install`

### 第四步：配置环境变量

在Vercel Dashboard中设置环境变量：
- `REACT_APP_API_URL`: `/api`

### 第五步：验证部署

部署成功后，访问你的域名：

1. **前端应用**: `https://your-app.vercel.app`
2. **API健康检查**: `https://your-app.vercel.app/api/health`
3. **API测试**: `https://your-app.vercel.app/api/todos`

## 🔧 配置文件说明

### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "frontend/build"
      }
    },
    {
      "src": "api/todos.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/todos"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ],
  "env": {
    "REACT_APP_API_URL": "/api"
  }
}
```

### api/todos.py
- 使用内存数据库，适合Serverless环境
- 支持所有CRUD操作
- 包含CORS处理

## 🐛 常见问题解决

### 问题1：构建失败 - 找不到index.html
**错误信息**: `Could not find a required file. Name: index.html Searched in: /vercel/path0/frontend/public`
**解决方案**:
1. 使用简化的`vercel.json`配置
2. 删除`.vercelignore`中的`*.md`规则
3. 确保`frontend/public/index.html`存在
4. 尝试使用`vercel-simple.json`配置

### 问题2：构建失败 - 通用错误
**错误信息**: `Build failed`
**解决方案**:
1. 检查`frontend/package.json`是否存在
2. 确保Node.js版本兼容（推荐16.x或18.x）
3. 检查构建日志中的具体错误信息

### 问题2：API函数错误
**错误信息**: `Function Error`
**解决方案**:
1. 检查`api/todos.py`语法
2. 确保没有外部依赖
3. 查看Vercel函数日志

### 问题3：CORS错误
**错误信息**: `CORS policy error`
**解决方案**:
1. API函数已包含CORS头
2. 检查前端API URL配置
3. 确保环境变量`REACT_APP_API_URL`设置为`/api`

### 问题4：路由404错误
**错误信息**: `404 Not Found`
**解决方案**:
1. 检查`vercel.json`中的路由配置
2. 确保API路径匹配正确
3. 验证构建输出目录

## 📊 性能优化

### 前端优化
- 使用`npm run build`生成生产版本
- 启用代码分割和懒加载
- 压缩静态资源

### 后端优化
- 使用内存数据库减少延迟
- 优化API响应时间
- 合理使用缓存

## 🔄 更新部署

### 自动部署
- 连接到GitHub仓库后，每次push会自动部署
- 支持预览部署（Pull Request）

### 手动部署
```bash
# 重新部署
vercel --prod

# 部署到预览环境
vercel
```

## 📝 注意事项

1. **数据持久化**: 当前使用内存数据库，重启后数据会丢失
2. **冷启动**: Serverless函数有冷启动时间，首次请求可能较慢
3. **限制**: Vercel免费版有使用限制，生产环境建议升级
4. **域名**: 可以绑定自定义域名

## 🔧 故障排除

### 如果部署仍然失败

1. **使用简化配置**：
```bash
# 备份当前配置
mv vercel.json vercel-backup.json
mv vercel-simple.json vercel.json

# 重新部署
vercel --prod
```

2. **检查文件结构**：
确保项目结构如下：
```
project_cursor_todov2/
├── frontend/
│   ├── package.json
│   ├── public/
│   │   └── index.html  ← 必须存在
│   └── src/
├── api/
│   └── todos.py
└── vercel.json
```

3. **手动构建测试**：
```bash
cd frontend
yarn install
yarn build
# 检查 build/ 目录是否生成
```

## 🆘 获取帮助

- **Vercel文档**: https://vercel.com/docs
- **社区支持**: https://github.com/vercel/vercel/discussions
- **项目Issues**: 在GitHub仓库中创建Issue

## 📈 监控和日志

1. **访问Vercel Dashboard**
2. **查看部署日志**
3. **监控性能指标**
4. **设置告警通知**

---

**部署成功后，你的Todo应用将在全球CDN上运行，提供快速可靠的用户体验！** 🎉
