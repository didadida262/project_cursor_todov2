#!/bin/bash

echo "🎯 Todo 项目启动脚本"
echo "========================================"

# 检测可用的终端模拟器
detect_terminal() {
    if command -v gnome-terminal >/dev/null 2>&1; then
        echo "gnome-terminal"
    elif command -v xterm >/dev/null 2>&1; then
        echo "xterm"
    elif command -v konsole >/dev/null 2>&1; then
        echo "konsole"
    elif command -v xfce4-terminal >/dev/null 2>&1; then
        echo "xfce4-terminal"
    elif command -v mate-terminal >/dev/null 2>&1; then
        echo "mate-terminal"
    else
        echo "none"
    fi
}

# 启动终端窗口
start_terminal() {
    local cmd="$1"
    local title="$2"
    local terminal=$(detect_terminal)
    
    case $terminal in
        "gnome-terminal")
            gnome-terminal -- bash -c "$cmd; exec bash" &
            ;;
        "xterm")
            xterm -title "$title" -e "bash -c '$cmd; exec bash'" &
            ;;
        "konsole")
            konsole --new-tab -e "bash -c '$cmd; exec bash'" &
            ;;
        "xfce4-terminal")
            xfce4-terminal --title="$title" -e "bash -c '$cmd; exec bash'" &
            ;;
        "mate-terminal")
            mate-terminal --title="$title" -e "bash -c '$cmd; exec bash'" &
            ;;
        *)
            echo "❌ 未找到可用的终端模拟器"
            echo "请手动打开两个终端窗口，分别运行："
            echo "终端1: cd backend && python start.py"
            echo "终端2: cd frontend && npm start"
            return 1
            ;;
    esac
}

echo ""
echo "📦 正在启动后端服务..."
if start_terminal "cd backend && python start.py" "后端服务"; then
    echo "✅ 后端服务启动命令已执行"
else
    exit 1
fi

echo ""
echo "⏳ 等待后端服务启动..."
sleep 5

echo ""
echo "🎨 正在启动前端服务..."
if start_terminal "cd frontend && npm start" "前端服务"; then
    echo "✅ 前端服务启动命令已执行"
else
    exit 1
fi

echo ""
echo "✅ 项目启动完成！"
echo "📍 后端API: http://localhost:8000"
echo "📍 前端应用: http://localhost:3000"
echo "📖 API文档: http://localhost:8000/docs"
echo ""
echo "如果终端窗口没有自动打开，请手动运行："
echo "终端1: cd backend && python start.py"
echo "终端2: cd frontend && npm start"
echo ""
echo "按任意键退出..."
read -n 1
