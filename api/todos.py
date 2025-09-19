"""
Vercel API 函数 - Todo 管理
使用内存数据库，适合Serverless环境
"""
import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime

# 简化的内存数据库（避免文件系统问题）
TODOS_DB = []
NEXT_ID = 1

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """处理 GET 请求"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/api/todos' or path == '/api/todos/':
            self.get_todos()
        elif path == '/api/health' or path == '/api/health/':
            self.health_check()
        else:
            self.send_error(404, "Not Found")
    
    def do_POST(self):
        """处理 POST 请求"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/api/todos' or path == '/api/todos/':
            self.create_todo()
        else:
            self.send_error(404, "Not Found")
    
    def do_PUT(self):
        """处理 PUT 请求"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path.startswith('/api/todos/'):
            todo_id = path.split('/')[-1]
            self.update_todo(todo_id)
        else:
            self.send_error(404, "Not Found")
    
    def do_DELETE(self):
        """处理 DELETE 请求"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path.startswith('/api/todos/') and path != '/api/todos/completed' and path != '/api/todos/all':
            todo_id = path.split('/')[-1]
            self.delete_todo(todo_id)
        elif path == '/api/todos/completed' or path == '/api/todos/completed/':
            self.delete_completed_todos()
        elif path == '/api/todos/all' or path == '/api/todos/all/':
            self.delete_all_todos()
        else:
            self.send_error(404, "Not Found")
    
    def get_todos_from_memory(self):
        """从内存获取任务列表"""
        return TODOS_DB
    
    def add_todo_to_memory(self, title, completed=False):
        """添加任务到内存"""
        global NEXT_ID
        todo = {
            "id": NEXT_ID,
            "title": title,
            "completed": completed,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        TODOS_DB.append(todo)
        NEXT_ID += 1
        return todo
    
    def get_todos(self):
        """获取任务列表"""
        try:
            # 获取查询参数
            parsed_path = urlparse(self.path)
            query_params = parse_qs(parsed_path.query)
            status = query_params.get('status', ['all'])[0]
            
            todos = self.get_todos_from_memory()
            
            # 根据状态筛选
            if status == 'active':
                todos = [todo for todo in todos if not todo['completed']]
            elif status == 'completed':
                todos = [todo for todo in todos if todo['completed']]
            
            # 按创建时间倒序排列
            todos.sort(key=lambda x: x['created_at'], reverse=True)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(json.dumps(todos).encode())
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def create_todo(self):
        """创建任务"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            todo_data = json.loads(post_data.decode('utf-8'))
            
            todo = self.add_todo_to_memory(
                title=todo_data['title'],
                completed=todo_data.get('completed', False)
            )
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(todo).encode())
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def update_todo(self, todo_id):
        """更新任务"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            update_data = json.loads(post_data.decode('utf-8'))
            
            # 查找任务
            todo = None
            for i, t in enumerate(TODOS_DB):
                if t['id'] == int(todo_id):
                    todo = t
                    break
            
            if not todo:
                self.send_error(404, "任务不存在")
                return
            
            # 更新任务
            if 'title' in update_data:
                todo['title'] = update_data['title']
            if 'completed' in update_data:
                todo['completed'] = update_data['completed']
            
            todo['updated_at'] = datetime.now().isoformat()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(todo).encode())
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def delete_todo(self, todo_id):
        """删除任务"""
        try:
            # 查找并删除任务
            global TODOS_DB
            original_length = len(TODOS_DB)
            TODOS_DB = [todo for todo in TODOS_DB if todo['id'] != int(todo_id)]
            
            if len(TODOS_DB) == original_length:
                self.send_error(404, "任务不存在")
                return
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "任务删除成功"}).encode())
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def delete_completed_todos(self):
        """批量删除已完成任务"""
        try:
            global TODOS_DB
            original_length = len(TODOS_DB)
            TODOS_DB = [todo for todo in TODOS_DB if not todo['completed']]
            deleted_count = original_length - len(TODOS_DB)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"message": f"已删除{deleted_count}个已完成任务"}).encode())
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def delete_all_todos(self):
        """清空所有任务"""
        try:
            global TODOS_DB
            count = len(TODOS_DB)
            TODOS_DB = []
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"message": f"已清空{count}个任务"}).encode())
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def health_check(self):
        """健康检查"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "healthy", "message": "服务运行正常"}).encode())
    
    def do_OPTIONS(self):
        """处理 CORS 预检请求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()