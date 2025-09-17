#!/bin/bash

echo "🎯 Todo 项目简单启动脚本"
echo "========================================"

echo ""
echo "📦 启动后端服务..."
echo "请在另一个终端窗口中运行以下命令："
echo "cd backend && python start.py"
echo ""

echo "⏳ 等待5秒后启动前端服务..."
sleep 5

echo ""
echo "🎨 启动前端服务..."
echo "请在另一个终端窗口中运行以下命令："
echo "cd frontend && npm start"
echo ""

echo "✅ 启动说明完成！"
echo "📍 后端API: http://localhost:8000"
echo "📍 前端应用: http://localhost:3000"
echo "📖 API文档: http://localhost:8000/docs"
echo ""
echo "请按照上述说明手动启动两个服务"

