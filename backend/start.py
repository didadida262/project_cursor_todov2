"""
后端服务启动脚本
"""
import subprocess
import sys
import os

def install_requirements():
    """安装依赖包"""
    print("📦 正在安装依赖包...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 依赖包安装完成")
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖包安装失败: {e}")
        return False
    return True

def start_server():
    """启动服务器"""
    print("🚀 正在启动 Todo API 服务器...")
    print("📍 服务地址: http://localhost:8000")
    print("📖 API文档: http://localhost:8000/docs")
    print("🔄 按 Ctrl+C 停止服务")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n👋 服务已停止")

def main():
    """主函数"""
    print("🎯 Todo API 后端服务")
    print("=" * 50)
    
    # 检查是否在正确的目录
    if not os.path.exists("main.py"):
        print("❌ 请在 backend 目录下运行此脚本")
        return
    
    # 安装依赖
    if not install_requirements():
        return
    
    # 启动服务
    start_server()

if __name__ == "__main__":
    main()
