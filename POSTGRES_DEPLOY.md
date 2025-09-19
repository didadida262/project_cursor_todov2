# Vercel Postgres 数据持久化部署指南

## 🚀 步骤1: 在 Vercel Marketplace 中设置 Postgres

### 1.1 进入 Vercel 项目
1. 登录 [Vercel Dashboard](https://vercel.com/dashboard)
2. 选择你的 Todo 项目

### 1.2 添加 Postgres 数据库
1. 点击项目页面的 **"Storage"** 标签
2. 点击 **"Browse Marketplace"**
3. 搜索 **"Postgres"** 或 **"Neon"**
4. 选择 **Neon** (推荐) 或 **Supabase**
5. 点击 **"Add Integration"**
6. 按照提示完成设置

### 1.3 获取数据库连接信息
设置完成后，Vercel会自动在你的项目中添加以下环境变量：
- `POSTGRES_URL` - 数据库连接字符串
- `POSTGRES_PRISMA_URL` - Prisma连接字符串
- `POSTGRES_URL_NON_POOLING` - 非连接池URL

## 🔧 步骤2: 更新 API 代码

### 2.1 替换 API 文件
将 `api/todos.py` 重命名为 `api/todos_backup.py`，然后将 `api/todos_postgres.py` 重命名为 `api/todos.py`：

```bash
# 备份原文件
mv api/todos.py api/todos_backup.py

# 使用Postgres版本
mv api/todos_postgres.py api/todos.py
```

### 2.2 更新 vercel.json
确保 `vercel.json` 配置正确：

```json
{
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "/api/todos"
    },
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

## 🚀 步骤3: 部署到 Vercel

### 3.1 提交代码
```bash
git add .
git commit -m "Add Postgres database support for data persistence"
git push origin main
```

### 3.2 自动部署
Vercel会自动检测到代码变更并开始部署。

## ✅ 步骤4: 验证部署

### 4.1 检查环境变量
在 Vercel 项目设置中确认 `POSTGRES_URL` 环境变量已正确设置。

### 4.2 测试 API
访问你的 Vercel 部署URL，测试以下功能：
- 添加任务
- 查看任务列表
- 更新任务状态
- 删除任务

### 4.3 验证数据持久化
1. 添加一些任务
2. 等待几分钟
3. 刷新页面，确认数据仍然存在

## 🔍 故障排除

### 问题1: 数据库连接失败
**解决方案**: 检查 `POSTGRES_URL` 环境变量是否正确设置

### 问题2: 表不存在
**解决方案**: API会自动创建表，如果失败，检查数据库权限

### 问题3: CORS 错误
**解决方案**: 确保API返回正确的CORS头

## 📊 数据库结构

Postgres表结构：
```sql
CREATE TABLE todos (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## 🎯 优势

- ✅ **数据持久化**: 数据不会因为函数重启而丢失
- ✅ **SQL兼容**: 使用标准SQL语法，与SQLite类似
- ✅ **自动扩展**: Vercel自动管理数据库连接
- ✅ **免费额度**: 大多数Postgres服务提供免费额度
- ✅ **备份恢复**: 自动备份和恢复功能

## 📝 注意事项

1. **免费额度限制**: 注意数据库的免费额度限制
2. **连接池**: 使用连接池可以提高性能
3. **索引优化**: 已自动创建必要的索引
4. **时区处理**: 使用UTC时间存储，前端显示时转换

现在你的Todo应用就具备了完整的数据持久化功能！
