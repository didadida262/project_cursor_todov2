"""
PythonAnywhere 部署脚本
"""
import os
import sys

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

# 添加当前目录到 Python 路径
sys.path.insert(0, '/home/yourusername/todo-api')

# 导入并运行 FastAPI 应用
from main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
