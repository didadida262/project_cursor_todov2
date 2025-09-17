#!/bin/bash

echo "🚀 Todo 应用一键部署脚本"
echo "========================================"

# 检查是否在项目根目录
if [ ! -f "package.json" ] && [ ! -d "frontend" ] && [ ! -d "backend" ]; then
    echo "❌ 请在项目根目录运行此脚本"
    exit 1
fi

echo ""
echo "📦 1. 构建前端项目..."
cd frontend
npm run build
if [ $? -ne 0 ]; then
    echo "❌ 前端构建失败"
    exit 1
fi
echo "✅ 前端构建成功"

echo ""
echo "🔧 2. 检查后端依赖..."
cd ../backend
python -c "import fastapi, uvicorn, pydantic" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 安装后端依赖..."
    pip install -r requirements.txt
fi
echo "✅ 后端依赖检查完成"

echo ""
echo "🎯 3. 部署准备完成！"
echo ""
echo "📋 下一步操作："
echo "1. 将代码推送到 GitHub"
echo "2. 前端部署到 Vercel："
echo "   - 访问 https://vercel.com"
echo "   - 连接 GitHub 仓库"
echo "   - 选择 frontend 目录"
echo "   - 设置环境变量 REACT_APP_API_URL"
echo ""
echo "3. 后端部署到 Railway："
echo "   - 访问 https://railway.app"
echo "   - 连接 GitHub 仓库"
echo "   - 选择 backend 目录"
echo "   - 设置环境变量 ALLOWED_ORIGINS"
echo ""
echo "📖 详细部署说明请查看 DEPLOYMENT.md"
