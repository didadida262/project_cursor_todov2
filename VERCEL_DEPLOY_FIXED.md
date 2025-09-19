# Vercel 部署修复指南

## 🔧 修复的问题

1. **数据库依赖问题**：移除了SQLite依赖，使用纯内存数据库
2. **API函数简化**：重写了`api/todos.py`，移除了文件系统操作
3. **配置优化**：更新了`vercel.json`配置

## 🚀 部署步骤

### 方法1：使用Vercel CLI（推荐）

```bash
# 1. 安装Vercel CLI
npm install -g vercel

# 2. 登录Vercel
vercel login

# 3. 部署项目
vercel

# 4. 按照提示配置：
# - 项目名称：todo-app
# - 框架：Other
# - 根目录：./
# - 构建命令：cd frontend && npm install && npm run build
# - 输出目录：frontend/build
```

### 方法2：使用Vercel Dashboard

1. 访问 [Vercel Dashboard](https://vercel.com/dashboard)
2. 点击 "New Project"
3. 导入你的GitHub仓库
4. 配置项目设置：
   - **Framework Preset**: Other
   - **Root Directory**: `./`
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Output Directory**: `frontend/build`
   - **Install Command**: `npm install`

### 方法3：使用简化的vercel.json

如果上述方法失败，可以尝试使用`vercel-simple.json`：

```bash
# 重命名配置文件
mv vercel.json vercel-complex.json
mv vercel-simple.json vercel.json

# 然后部署
vercel
```

## 🔍 验证部署

部署成功后，访问你的Vercel域名：

1. **前端应用**：`https://your-app.vercel.app`
2. **API健康检查**：`https://your-app.vercel.app/api/health`
3. **API文档**：`https://your-app.vercel.app/api/todos`

## 🐛 常见问题

### 问题1：构建失败
**解决方案**：
- 确保`frontend/package.json`存在
- 检查Node.js版本（推荐16.x或18.x）

### 问题2：API函数错误
**解决方案**：
- 检查`api/todos.py`语法
- 确保没有外部依赖

### 问题3：CORS错误
**解决方案**：
- API函数已包含CORS头
- 检查前端API URL配置

## 📝 注意事项

1. **数据持久化**：当前使用内存数据库，重启后数据会丢失
2. **生产环境**：如需数据持久化，建议使用外部数据库服务
3. **性能**：Serverless函数有冷启动时间，首次请求可能较慢

## 🔄 回滚方案

如果部署失败，可以：

1. 使用`vercel-complex.json`恢复原配置
2. 检查Vercel Dashboard中的构建日志
3. 联系Vercel支持

## 📞 技术支持

- Vercel文档：https://vercel.com/docs
- 项目Issues：在GitHub仓库中创建Issue
