# 待办事项应用 PRD 技术文档

## 1. 产品概述

### 1.1 产品名称
待办事项管理应用 (Todo Application)

### 1.2 产品定位
一个简洁、现代的待办事项管理工具，帮助用户高效管理日常任务，支持任务的增删改查、状态管理等功能。

### 1.3 目标用户
- 个人用户：需要管理日常任务的个人
- 学生：需要跟踪学习任务和作业的学生
- 职场人士：需要管理工作任务的专业人士

## 2. 功能需求

### 2.1 核心功能

#### 2.1.1 任务管理
- **添加任务**：用户可以通过输入框添加新的待办事项
- **查看任务**：以列表形式展示所有待办事项
- **标记完成**：用户可以标记任务为已完成状态
- **删除任务**：用户可以删除不需要的任务

#### 2.1.2 任务筛选
- **全部任务**：显示所有任务（已完成+未完成）
- **未完成任务**：仅显示未完成的任务
- **已完成任务**：仅显示已完成的任务

#### 2.1.3 批量操作
- **清除已完成**：批量删除所有已完成的任务
- **清除全部**：批量删除所有任务

### 2.2 界面要求

#### 2.2.1 布局设计
- 主体内容居中显示
- 最大宽度限制为800px
- 响应式设计，适配不同屏幕尺寸

#### 2.2.2 视觉设计
- 现代、简洁的CSS样式
- 输入框和按钮样式美观
- 列表项之间有适当间距
- 鼠标悬停效果（按钮和列表项）

#### 2.2.3 交互设计
- 添加任务后自动清空输入框
- 完成的任务显示删除线效果
- 按钮点击有视觉反馈

## 3. 技术架构

### 3.1 技术栈
- **前端**：React
- **后端**：FastAPI
- **数据库**：SQLite
- **项目结构**：分为backend和frontend两个目录

### 3.2 系统架构图
```
┌─────────────────┐    HTTP API    ┌─────────────────┐    SQL    ┌─────────────────┐
│   React Frontend │ ◄─────────────► │  FastAPI Backend │ ◄─────────► │   SQLite DB     │
│                 │                │                 │          │                 │
│ - 任务列表组件    │                │ - REST API      │          │ - todos 表      │
│ - 任务表单组件    │                │ - 数据验证      │          │ - 任务数据存储   │
│ - 筛选组件       │                │ - 业务逻辑      │          │                 │
│ - 批量操作组件    │                │ - 错误处理      │          │                 │
└─────────────────┘                └─────────────────┘          └─────────────────┘
```

### 3.3 项目目录结构
```
project_cursor_todov2/
├── backend/
│   ├── main.py              # FastAPI 应用入口
│   ├── models.py            # 数据模型
│   ├── database.py          # 数据库连接
│   ├── routers/             # API 路由
│   │   └── todos.py
│   ├── schemas.py           # Pydantic 模型
│   └── requirements.txt     # Python 依赖
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/      # React 组件
│   │   │   ├── TodoList.jsx
│   │   │   ├── TodoForm.jsx
│   │   │   ├── TodoItem.jsx
│   │   │   └── FilterBar.jsx
│   │   ├── services/        # API 服务
│   │   │   └── api.js
│   │   ├── styles/          # CSS 样式
│   │   │   └── App.css
│   │   └── App.js           # 主应用组件
│   ├── package.json         # Node.js 依赖
│   └── README.md
└── README.md                # 项目说明
```

## 4. 数据库设计

### 4.1 表结构设计

#### 4.1.1 todos 表
```sql
CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 4.2 字段说明
- **id**：主键，自增整数
- **title**：任务标题，最大长度255字符，必填
- **completed**：完成状态，布尔值，默认false
- **created_at**：创建时间，自动记录
- **updated_at**：更新时间，自动记录

### 4.3 索引设计
```sql
-- 为completed字段创建索引，提高查询性能
CREATE INDEX idx_todos_completed ON todos(completed);

-- 为created_at字段创建索引，支持按时间排序
CREATE INDEX idx_todos_created_at ON todos(created_at);
```

## 5. API 设计

### 5.1 接口规范
- **基础URL**：`http://localhost:8000/api/v1`
- **数据格式**：JSON
- **HTTP方法**：GET, POST, PUT, DELETE

### 5.2 接口列表

#### 5.2.1 获取任务列表
```
GET /todos
参数：
- status: string (可选) - 筛选条件：all, active, completed
响应：
{
  "todos": [
    {
      "id": 1,
      "title": "学习React",
      "completed": false,
      "created_at": "2024-01-01T10:00:00Z",
      "updated_at": "2024-01-01T10:00:00Z"
    }
  ]
}
```

#### 5.2.2 创建任务
```
POST /todos
请求体：
{
  "title": "新任务标题"
}
响应：
{
  "id": 1,
  "title": "新任务标题",
  "completed": false,
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

#### 5.2.3 更新任务状态
```
PUT /todos/{id}
请求体：
{
  "completed": true
}
响应：
{
  "id": 1,
  "title": "任务标题",
  "completed": true,
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T11:00:00Z"
}
```

#### 5.2.4 删除任务
```
DELETE /todos/{id}
响应：
{
  "message": "任务删除成功"
}
```

#### 5.2.5 批量删除已完成任务
```
DELETE /todos/completed
响应：
{
  "message": "已删除3个已完成任务"
}
```

#### 5.2.6 清空所有任务
```
DELETE /todos/all
响应：
{
  "message": "已清空所有任务"
}
```

## 6. 前端组件设计

### 6.1 组件架构
```
App
├── TodoForm          # 任务输入表单
├── FilterBar         # 筛选和批量操作栏
└── TodoList          # 任务列表
    └── TodoItem      # 单个任务项
```

### 6.2 组件详细设计

#### 6.2.1 TodoForm 组件
- **功能**：输入新任务并提交
- **状态**：输入框内容
- **事件**：onSubmit, onChange

#### 6.2.2 TodoList 组件
- **功能**：显示任务列表
- **Props**：todos, onToggle, onDelete
- **状态**：无

#### 6.2.3 TodoItem 组件
- **功能**：单个任务的显示和操作
- **Props**：todo, onToggle, onDelete
- **状态**：无

#### 6.2.4 FilterBar 组件
- **功能**：筛选和批量操作
- **状态**：当前筛选条件
- **事件**：onFilterChange, onClearCompleted, onClearAll

## 7. 样式设计规范

### 7.1 颜色方案
```css
:root {
  --primary-color: #007bff;
  --secondary-color: #6c757d;
  --success-color: #28a745;
  --danger-color: #dc3545;
  --warning-color: #ffc107;
  --light-color: #f8f9fa;
  --dark-color: #343a40;
  --border-color: #dee2e6;
  --text-color: #212529;
  --text-muted: #6c757d;
}
```

### 7.2 布局规范
- 容器最大宽度：800px
- 内边距：20px
- 外边距：0 auto（居中）
- 圆角：8px
- 阴影：0 2px 4px rgba(0,0,0,0.1)

### 7.3 交互效果
- 按钮悬停：背景色加深，过渡时间0.2s
- 列表项悬停：背景色变化，过渡时间0.2s
- 完成状态：文字删除线，颜色变灰

## 8. 开发计划

### 8.1 开发阶段
1. **第一阶段**：后端API开发（2天）
   - 数据库设计和初始化
   - FastAPI应用搭建
   - 基础CRUD接口实现

2. **第二阶段**：前端基础功能（2天）
   - React应用搭建
   - 基础组件开发
   - API集成

3. **第三阶段**：样式和交互优化（1天）
   - CSS样式完善
   - 交互效果实现
   - 响应式适配

4. **第四阶段**：测试和部署（1天）
   - 功能测试
   - 性能优化
   - 部署配置

### 8.2 里程碑
- [ ] 数据库表创建完成
- [ ] 后端API开发完成
- [ ] 前端基础功能完成
- [ ] 样式和交互完成
- [ ] 功能测试通过
- [ ] 项目部署完成

## 9. 测试计划

### 9.1 功能测试
- 添加任务功能测试
- 标记完成功能测试
- 删除任务功能测试
- 筛选功能测试
- 批量操作功能测试

### 9.2 界面测试
- 响应式布局测试
- 浏览器兼容性测试
- 交互效果测试

### 9.3 性能测试
- API响应时间测试
- 大数据量加载测试
- 内存使用情况测试

## 10. 部署说明

### 10.1 环境要求
- Node.js 16+
- Python 3.8+
- SQLite 3

### 10.2 部署步骤
1. 克隆项目代码
2. 安装后端依赖：`pip install -r backend/requirements.txt`
3. 安装前端依赖：`npm install`
4. 启动后端服务：`uvicorn backend.main:app --reload`
5. 启动前端服务：`npm start`
6. 访问应用：`http://localhost:3000`

## 11. 维护和扩展

### 11.1 后续功能扩展
- 任务分类功能
- 任务优先级设置
- 任务截止时间
- 用户认证系统
- 数据导入导出

### 11.2 技术优化
- 数据库连接池优化
- 前端状态管理优化
- 缓存机制引入
- 单元测试覆盖

---

**文档版本**：v1.0  
**创建日期**：2024年1月  
**最后更新**：2024年1月  
**维护人员**：开发团队
