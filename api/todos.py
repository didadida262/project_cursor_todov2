"""
Vercel API 函数 - Todo 管理
"""
from http.server import BaseHTTPRequestHandler
import json
import sqlite3
import os
from urllib.parse import urlparse, parse_qs
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """处理 GET 请求"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/api/todos':
            self.get_todos()
        elif path == '/api/health':
            self.health_check()
        else:
            self.send_error(404, "Not Found")
    
    def do_POST(self):
        """处理 POST 请求"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/api/todos':
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
        
        if path.startswith('/api/todos/'):
            todo_id = path.split('/')[-1]
            self.delete_todo(todo_id)
        elif path == '/api/todos/completed':
            self.delete_completed_todos()
        elif path == '/api/todos/all':
            self.delete_all_todos()
        else:
            self.send_error(404, "Not Found")
    
    def get_db_connection(self):
        """获取数据库连接"""
        # 在 Vercel 中，我们需要使用临时文件
        db_path = '/tmp/todos.db'
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """初始化数据库"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(255) NOT NULL,
                completed BOOLEAN DEFAULT FALSE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def get_todos(self):
        """获取任务列表"""
        try:
            self.init_database()
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # 获取查询参数
            parsed_path = urlparse(self.path)
            query_params = parse_qs(parsed_path.query)
            status = query_params.get('status', ['all'])[0]
            
            if status == 'active':
                query = "SELECT * FROM todos WHERE completed = FALSE ORDER BY created_at DESC"
            elif status == 'completed':
                query = "SELECT * FROM todos WHERE completed = TRUE ORDER BY created_at DESC"
            else:
                query = "SELECT * FROM todos ORDER BY created_at DESC"
            
            cursor.execute(query)
            rows = cursor.fetchall()
            
            todos = []
            for row in rows:
                todos.append({
                    "id": row["id"],
                    "title": row["title"],
                    "completed": bool(row["completed"]),
                    "created_at": row["created_at"],
                    "updated_at": row["updated_at"]
                })
            
            conn.close()
            
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
            self.init_database()
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            todo_data = json.loads(post_data.decode('utf-8'))
            
            cursor.execute("""
                INSERT INTO todos (title, completed, created_at, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """, (todo_data['title'], todo_data.get('completed', False)))
            
            todo_id = cursor.lastrowid
            
            cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
            row = cursor.fetchone()
            
            conn.commit()
            conn.close()
            
            todo = {
                "id": row["id"],
                "title": row["title"],
                "completed": bool(row["completed"]),
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            }
            
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
            self.init_database()
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            update_data = json.loads(post_data.decode('utf-8'))
            
            # 检查任务是否存在
            cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
            existing_todo = cursor.fetchone()
            
            if not existing_todo:
                self.send_error(404, "任务不存在")
                return
            
            # 构建更新SQL
            update_fields = []
            update_values = []
            
            if 'title' in update_data:
                update_fields.append("title = ?")
                update_values.append(update_data['title'])
            
            if 'completed' in update_data:
                update_fields.append("completed = ?")
                update_values.append(update_data['completed'])
            
            if update_fields:
                update_fields.append("updated_at = CURRENT_TIMESTAMP")
                update_values.append(todo_id)
                
                query = f"UPDATE todos SET {', '.join(update_fields)} WHERE id = ?"
                cursor.execute(query, update_values)
            
            # 查询更新后的任务
            cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
            row = cursor.fetchone()
            
            conn.commit()
            conn.close()
            
            todo = {
                "id": row["id"],
                "title": row["title"],
                "completed": bool(row["completed"]),
                "created_at": row["created_at"],
                "updated_at": row["updated_at"]
            }
            
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
            self.init_database()
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # 检查任务是否存在
            cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
            existing_todo = cursor.fetchone()
            
            if not existing_todo:
                self.send_error(404, "任务不存在")
                return
            
            # 删除任务
            cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
            conn.commit()
            conn.close()
            
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
            self.init_database()
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # 查询已完成任务数量
            cursor.execute("SELECT COUNT(*) FROM todos WHERE completed = TRUE")
            count = cursor.fetchone()[0]
            
            # 删除已完成的任务
            cursor.execute("DELETE FROM todos WHERE completed = TRUE")
            conn.commit()
            conn.close()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"message": f"已删除{count}个已完成任务"}).encode())
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def delete_all_todos(self):
        """清空所有任务"""
        try:
            self.init_database()
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # 查询总任务数量
            cursor.execute("SELECT COUNT(*) FROM todos")
            count = cursor.fetchone()[0]
            
            # 删除所有任务
            cursor.execute("DELETE FROM todos")
            conn.commit()
            conn.close()
            
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
