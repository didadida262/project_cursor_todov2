@echo off
echo 🚀 Vercel 部署脚本
echo ========================================

echo.
echo 📦 检查前端依赖...
cd frontend
if not exist node_modules (
    echo 正在安装前端依赖...
    npm install
) else (
    echo ✅ 前端依赖已安装
)

echo.
echo 🔨 构建前端项目...
npm run build
if errorlevel 1 (
    echo ❌ 前端构建失败
    pause
    exit /b 1
)
echo ✅ 前端构建成功

echo.
echo 📤 部署到 Vercel...
cd ..
vercel --prod

echo.
echo ✅ 部署完成！
echo 📍 访问你的应用: https://your-project-name.vercel.app
echo.
echo 按任意键退出...
pause >nul
