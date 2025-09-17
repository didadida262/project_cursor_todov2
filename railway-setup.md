# Railway CLI 设置指南

## 安装 Railway CLI

### Windows (PowerShell)
```powershell
# 使用 winget 安装
winget install Railway.Railway

# 或者使用 npm 安装
npm install -g @railway/cli
```

### 其他系统
```bash
# 使用 npm 安装
npm install -g @railway/cli

# 或者使用 curl 安装
curl -fsSL https://railway.app/install.sh | sh
```

## 使用 CLI 设置项目

1. **登录 Railway**
```bash
railway login
```

2. **初始化项目**
```bash
railway init
```

3. **设置根目录**
```bash
railway variables set RAILWAY_ROOT_DIRECTORY=backend
```

4. **部署项目**
```bash
railway up
```

## 通过 Web 界面设置

如果找不到 Root Directory 设置，可以尝试以下方法：

### 方法1：重新部署
1. 在 Railway 项目页面
2. 点击 "Settings" 标签
3. 找到 "Source" 部分
4. 点击 "Connect Repo" 重新连接
5. 在连接时选择 "backend" 作为根目录

### 方法2：使用 nixpacks.toml
在项目根目录创建 `nixpacks.toml` 文件：

```toml
[phases.setup]
nixPkgs = ["python39", "pip"]

[phases.install]
cmds = ["cd backend && pip install -r requirements.txt"]

[phases.build]
cmds = ["cd backend && echo 'Build complete'"]

[start]
cmd = "cd backend && python main.py"
```

### 方法3：修改启动命令
在 Railway 项目设置中，将启动命令改为：
```
cd backend && python main.py
```
