"""
Vercel API 函数 - Todo 管理 (使用 Postgres 数据库)
实现数据持久化存储
"""
import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor

# 从环境变量获取数据库连接信息
DATABASE_URL = os.environ.get('POSTGRES_URL')

def get_db_connection():
    """获取数据库连接"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

def init_database():
    """初始化数据库表"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # 创建todos表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            )
        """)
        
        # 创建索引
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_todos_completed 
            ON todos(completed)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_todos_created_at 
            ON todos(created_at)
        """)
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Database initialization error: {e}")
        return False
    finally:
        conn.close()

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
        
        if path.startswith('/api/todos/') and path != '/api/todos/completed' and path != '/api/todos/all':
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
    
    def do_OPTIONS(self):
        """处理 CORS 预检请求"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def get_todos(self):
        """获取任务列表"""
        try:
            # 初始化数据库
            init_database()
            
            # 获取查询参数
            parsed_path = urlparse(self.path)
            query_params = parse_qs(parsed_path.query)
            status = query_params.get('status', ['all'])[0]
            
            conn = get_db_connection()
            if not conn:
                self.send_error(500, "Database connection failed")
                return
            
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # 构建查询SQL
            if status == 'active':
                cursor.execute("SELECT * FROM todos WHERE completed = FALSE ORDER BY created_at DESC")
            elif status == 'completed':
                cursor.execute("SELECT * FROM todos WHERE completed = TRUE ORDER BY created_at DESC")
            else:
                cursor.execute("SELECT * FROM todos ORDER BY created_at DESC")
            
            todos = cursor.fetchall()
            
            # 转换为字典列表
            todos_list = []
            for todo in todos:
                todos_list.append({
                    'id': todo['id'],
                    'title': todo['title'],
                    'completed': todo['completed'],
                    'created_at': todo['created_at'].isoformat(),
                    'updated_at': todo['updated_at'].isoformat()
                })
            
            cursor.close()
            conn.close()
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(json.dumps(todos_list).encode())
            
        except Exception as e:
            self.send_error(500, str(e))
    
    def create_todo(self):
        """创建任务"""
        try:
            # 初始化数据库
            init_database()
            
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            todo_data = json.loads(post_data.decode('utf-8'))
            
            conn = get_db_connection()
            if not conn:
                self.send_error(500, "Database connection failed")
                return
            
            cursor = conn.cursor()
            
            # 插入新任务
            cursor.execute("""
                INSERT INTO todos (title, completed) 
                VALUES (%s, %s) 
                RETURNING id, title, completed, created_at, updated_at
            """, (todo_data['title'], todo_data.get('completed', False)))
            
            result = cursor.fetchone()
            todo = {
                'id': result[0],
                'title': result[1],
                'completed': result[2],
                'created_at': result[3].isoformat(),
                'updated_at': result[4].isoformat()
            }
            
            conn.commit()
            cursor.close()
            conn.close()
            
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
            # 初始化数据库
            init_database()
            
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            update_data = json.loads(post_data.decode('utf-8'))
            
            conn = get_db_connection()
            if not conn:
                self.send_error(500, "Database connection failed")
                return
            
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # 构建更新SQL
            set_clauses = []
            params = []
            
            if 'title' in update_data:
                set_clauses.append("title = %s")
                params.append(update_data['title'])
            
            if 'completed' in update_data:
                set_clauses.append("completed = %s")
                params.append(update_data['completed'])
            
            set_clauses.append("updated_at = NOW()")
            params.append(todo_id)
            
            cursor.execute(f"""
                UPDATE todos 
                SET {', '.join(set_clauses)}
                WHERE id = %s
                RETURNING id, title, completed, created_at, updated_at
            """, params)
            
            result = cursor.fetchone()
            if not result:
                self.send_error(404, "任务不存在")
                return
            
            todo = {
                'id': result['id'],
                'title': result['title'],
                'completed': result['completed'],
                'created_at': result['created_at'].isoformat(),
                'updated_at': result['updated_at'].isoformat()
            }
            
            conn.commit()
            cursor.close()
            conn.close()
            
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
            # 初始化数据库
            init_database()
            
            conn = get_db_connection()
            if not conn:
                self.send_error(500, "Database connection failed")
                return
            
            cursor = conn.cursor()
            
            # 删除任务
            cursor.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
            
            if cursor.rowcount == 0:
                self.send_error(404, "任务不存在")
                return
            
            conn.commit()
            cursor.close()
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
            # 初始化数据库
            init_database()
            
            conn = get_db_connection()
            if not conn:
                self.send_error(500, "Database connection failed")
                return
            
            cursor = conn.cursor()
            
            # 删除已完成任务
            cursor.execute("DELETE FROM todos WHERE completed = TRUE")
            deleted_count = cursor.rowcount
            
            conn.commit()
            cursor.close()
            conn.close()
            
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
            # 初始化数据库
            init_database()
            
            conn = get_db_connection()
            if not conn:
                self.send_error(500, "Database connection failed")
                return
            
            cursor = conn.cursor()
            
            # 获取任务数量
            cursor.execute("SELECT COUNT(*) FROM todos")
            count = cursor.fetchone()[0]
            
            # 清空所有任务
            cursor.execute("DELETE FROM todos")
            
            conn.commit()
            cursor.close()
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
