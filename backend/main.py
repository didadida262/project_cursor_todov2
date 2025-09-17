"""
FastAPI主应用入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from database import init_database
from routers import todos

# 创建FastAPI应用实例
app = FastAPI(
    title="Todo API",
    description="一个简洁的待办事项管理API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS中间件
import os
allowed_origins = [
    "http://localhost:3000", 
    "http://127.0.0.1:3000",
    "https://your-frontend-app.vercel.app"  # 替换为你的Vercel域名
]

# 从环境变量读取允许的源
if os.environ.get("ALLOWED_ORIGINS"):
    allowed_origins.extend(os.environ.get("ALLOWED_ORIGINS").split(","))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(todos.router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """应用启动时初始化数据库"""
    init_database()
    print("🚀 Todo API 服务启动成功！")
    print("📖 API文档地址: http://localhost:8000/docs")

@app.get("/")
async def root():
    """根路径，返回API信息"""
    return {
        "message": "欢迎使用Todo API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "message": "服务运行正常"}

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """全局异常处理器"""
    return JSONResponse(
        status_code=500,
        content={"message": "服务器内部错误", "detail": str(exc)}
    )

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False,  # 生产环境关闭热重载
        log_level="info"
    )

