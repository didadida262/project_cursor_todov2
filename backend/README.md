# Todo API 后端技术文档

## 📋 项目概述

这是一个基于 FastAPI 构建的待办事项管理 API 后端服务，提供完整的任务 CRUD 操作、状态管理和批量操作功能。

## 🏗️ 技术架构

### 技术栈
- **框架**: FastAPI 0.104.1
- **数据库**: SQLite 3
- **ORM**: 原生 SQLite3 (轻量级选择)
- **数据验证**: Pydantic 2.5.0
- **服务器**: Uvicorn
- **API文档**: 自动生成 (Swagger UI + ReDoc)

### 项目结构
```
backend/
├── main.py              # FastAPI 应用入口
├── database.py          # 数据库连接和初始化
├── models.py            # Pydantic 数据模型
├── requirements.txt     # Python 依赖
├── routers/             # API 路由模块
│   ├── __init__.py
│   └── todos.py         # Todo 相关路由
└── README.md           # 技术文档
```

## 🚀 快速开始

### 环境要求
- Python 3.8+
- SQLite 3

### 安装和运行

1. **安装依赖**
```bash
pip install -r requirements.txt
```

2. **启动服务**
```bash
# 开发模式 (自动重载)
python main.py

# 或使用 uvicorn 命令
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. **访问服务**
- API 服务: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📊 数据库设计

### 表结构
```sql
CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 索引优化
```sql
-- 完成状态索引
CREATE INDEX idx_todos_completed ON todos(completed);

-- 创建时间索引
CREATE INDEX idx_todos_created_at ON todos(created_at);
```

### 字段说明
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键，自增 |
| title | VARCHAR(255) | 任务标题，必填 |
| completed | BOOLEAN | 完成状态，默认 FALSE |
| created_at | DATETIME | 创建时间，自动记录 |
| updated_at | DATETIME | 更新时间，自动记录 |

## 🔌 API 接口文档

### 基础信息
- **基础URL**: `http://localhost:8000/api/v1`
- **数据格式**: JSON
- **认证**: 无 (简化版本)

### 接口列表

#### 1. 获取任务列表
```http
GET /api/v1/todos?status={status}
```

**参数**:
- `status` (可选): 筛选条件
  - `all`: 全部任务 (默认)
  - `active`: 未完成任务
  - `completed`: 已完成任务

**响应示例**:
```json
[
  {
    "id": 1,
    "title": "学习 FastAPI",
    "completed": false,
    "created_at": "2024-01-01T10:00:00",
    "updated_at": "2024-01-01T10:00:00"
  }
]
```

#### 2. 创建任务
```http
POST /api/v1/todos
```

**请求体**:
```json
{
  "title": "新任务标题",
  "completed": false
}
```

**响应**: 创建的任务对象

#### 3. 更新任务
```http
PUT /api/v1/todos/{todo_id}
```

**请求体**:
```json
{
  "title": "更新后的标题",
  "completed": true
}
```

**响应**: 更新后的任务对象

#### 4. 删除任务
```http
DELETE /api/v1/todos/{todo_id}
```

**响应**:
```json
{
  "message": "任务删除成功"
}
```

#### 5. 批量删除已完成任务
```http
DELETE /api/v1/todos/completed
```

**响应**:
```json
{
  "message": "已删除3个已完成任务"
}
```

#### 6. 清空所有任务
```http
DELETE /api/v1/todos/all
```

**响应**:
```json
{
  "message": "已清空5个任务"
}
```

## 🛠️ 核心模块详解

### 1. 数据库模块 (`database.py`)

#### 功能特性
- **连接管理**: 使用上下文管理器确保连接正确关闭
- **自动初始化**: 应用启动时自动创建表和索引
- **行工厂**: 配置 `sqlite3.Row` 支持列名访问

#### 核心函数
```python
@contextmanager
def get_db_connection():
    """获取数据库连接的上下文管理器"""

def init_database():
    """初始化数据库，创建todos表"""

def get_db():
    """获取数据库连接的生成器函数"""
```

### 2. 数据模型 (`models.py`)

#### Pydantic 模型层次
```python
TodoBase          # 基础模型
├── TodoCreate    # 创建模型
└── TodoUpdate    # 更新模型

Todo              # 完整模型 (包含ID和时间戳)
TodoResponse      # 响应模型 (字符串时间格式)
MessageResponse   # 消息响应模型
```

#### 模型特性
- **数据验证**: 自动验证输入数据类型和格式
- **序列化**: 自动处理 JSON 序列化/反序列化
- **文档生成**: 自动生成 API 文档

### 3. 路由模块 (`routers/todos.py`)

#### 路由设计原则
- **RESTful**: 遵循 REST API 设计规范
- **错误处理**: 统一的 HTTP 异常处理
- **参数验证**: 使用 Pydantic 进行数据验证
- **状态码**: 正确的 HTTP 状态码返回

#### 核心功能
- **CRUD 操作**: 完整的增删改查功能
- **条件查询**: 支持按完成状态筛选
- **批量操作**: 支持批量删除功能
- **事务安全**: 使用数据库事务确保数据一致性

### 4. 主应用 (`main.py`)

#### 应用配置
```python
app = FastAPI(
    title="Todo API",
    description="一个简洁的待办事项管理API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
```

#### 中间件配置
- **CORS**: 支持跨域请求，配置前端开发服务器地址
- **异常处理**: 全局异常处理器，统一错误响应格式

#### 生命周期事件
- **启动事件**: 自动初始化数据库
- **健康检查**: 提供 `/health` 端点监控服务状态

## 🔧 开发指南

### 代码规范
1. **类型注解**: 所有函数参数和返回值都使用类型注解
2. **文档字符串**: 使用 Google 风格的文档字符串
3. **错误处理**: 使用 FastAPI 的 HTTPException 处理业务异常
4. **日志记录**: 关键操作添加日志输出

### 扩展开发
1. **添加新路由**: 在 `routers/` 目录下创建新的路由文件
2. **数据库迁移**: 在 `database.py` 中添加新的表结构
3. **中间件**: 在 `main.py` 中注册新的中间件
4. **认证授权**: 可以集成 JWT 或其他认证方案

### 测试建议
```python
# 使用 pytest 进行单元测试
pip install pytest httpx

# 测试示例
def test_create_todo():
    response = client.post("/api/v1/todos", json={"title": "测试任务"})
    assert response.status_code == 200
    assert response.json()["title"] == "测试任务"
```

## 🚀 部署指南

### 开发环境
```bash
# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
python main.py
```

### 生产环境
```bash
# 使用 gunicorn + uvicorn workers
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# 或使用 Docker
docker build -t todo-api .
docker run -p 8000:8000 todo-api
```

### 环境变量
```bash
# 数据库配置
DATABASE_URL=sqlite:///./todos.db

# 服务器配置
HOST=0.0.0.0
PORT=8000
DEBUG=False
```

## 📈 性能优化

### 数据库优化
1. **索引优化**: 为常用查询字段创建索引
2. **连接池**: 生产环境建议使用连接池
3. **查询优化**: 避免 N+1 查询问题

### API 优化
1. **分页**: 大量数据时实现分页查询
2. **缓存**: 使用 Redis 缓存热点数据
3. **压缩**: 启用 gzip 压缩响应数据

## 🔒 安全考虑

### 当前实现
- **输入验证**: 使用 Pydantic 验证所有输入
- **SQL 注入**: 使用参数化查询防止 SQL 注入
- **CORS 配置**: 限制允许的源域名

### 生产环境建议
- **认证授权**: 实现用户认证和权限控制
- **HTTPS**: 使用 HTTPS 加密传输
- **限流**: 实现 API 限流防止滥用
- **日志审计**: 记录所有操作日志

## 🐛 故障排除

### 常见问题

1. **数据库文件权限问题**
```bash
chmod 664 todos.db
```

2. **端口占用问题**
```bash
# 查看端口占用
netstat -tulpn | grep :8000
# 杀死进程
kill -9 <PID>
```

3. **依赖安装问题**
```bash
# 升级 pip
pip install --upgrade pip
# 清理缓存
pip cache purge
```

### 日志调试
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📚 相关资源

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [SQLite 官方文档](https://www.sqlite.org/docs.html)
- [Pydantic 官方文档](https://pydantic-docs.helpmanual.io/)
- [Uvicorn 官方文档](https://www.uvicorn.org/)

## 📝 更新日志

### v1.0.0 (2024-01-01)
- ✨ 初始版本发布
- 🎯 实现基础 CRUD 操作
- 🔍 支持任务状态筛选
- 🗑️ 支持批量删除操作
- 📖 自动生成 API 文档

---

**维护团队**: 开发团队  
**最后更新**: 2024年1月  
**文档版本**: v1.0.0

