/**
 * 前端应用启动脚本
 */
const { spawn } = require('child_process');
const path = require('path');

console.log('🎯 Todo 前端应用启动器');
console.log('=' .repeat(50));

// 检查是否安装了依赖
const fs = require('fs');
const nodeModulesPath = path.join(__dirname, 'node_modules');

if (!fs.existsSync(nodeModulesPath)) {
  console.log('📦 正在安装依赖包...');
  
  const installProcess = spawn('npm', ['install'], {
    stdio: 'inherit',
    shell: true,
    cwd: __dirname
  });
  
  installProcess.on('close', (code) => {
    if (code === 0) {
      console.log('✅ 依赖包安装完成');
      startApp();
    } else {
      console.log('❌ 依赖包安装失败');
      process.exit(1);
    }
  });
} else {
  console.log('✅ 依赖包已安装');
  startApp();
}

function startApp() {
  console.log('🚀 正在启动前端开发服务器...');
  console.log('📍 应用地址: http://localhost:3000');
  console.log('🔄 按 Ctrl+C 停止服务');
  console.log('⚠️  请确保后端服务运行在 http://localhost:8000');
  console.log('-'.repeat(50));
  
  const startProcess = spawn('npm', ['start'], {
    stdio: 'inherit',
    shell: true,
    cwd: __dirname
  });
  
  startProcess.on('close', (code) => {
    console.log(`\n👋 应用已停止 (退出码: ${code})`);
  });
  
  // 处理进程退出
  process.on('SIGINT', () => {
    console.log('\n🛑 正在停止应用...');
    startProcess.kill('SIGINT');
  });
}

