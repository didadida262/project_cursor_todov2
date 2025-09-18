@echo off
echo 🎯 Todo 项目启动脚本
echo ========================================

echo.
echo 📦 正在启动后端服务...
cd /d "%~dp0"
start "后端服务" cmd /k "cd /d %~dp0backend && python main.py"

echo.
echo ⏳ 等待后端服务启动...
timeout /t 5 /nobreak >nul

echo.
echo 🎨 正在启动前端服务...
start "前端服务" cmd /k "cd /d %~dp0frontend && npm start"

echo.
echo ✅ 项目启动完成！
echo 📍 后端API: http://localhost:8000
echo 📍 前端应用: http://localhost:3000
echo 📖 API文档: http://localhost:8000/docs
echo.
echo 按任意键退出...
pause >nul
