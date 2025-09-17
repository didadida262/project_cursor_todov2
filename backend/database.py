"""
数据库连接和初始化模块
"""
import sqlite3
from typing import Generator
from contextlib import contextmanager
import os

# 数据库文件路径
DATABASE_URL = "sqlite:///./todos.db"

@contextmanager
def get_db_connection():
    """
    获取数据库连接的上下文管理器
    """
    conn = sqlite3.connect("todos.db")
    conn.row_factory = sqlite3.Row  # 使结果可以通过列名访问
    try:
        yield conn
    finally:
        conn.close()

def init_database():
    """
    初始化数据库，创建todos表
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # 创建todos表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(255) NOT NULL,
                completed BOOLEAN DEFAULT FALSE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
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
        print("数据库初始化完成")

def get_db():
    """
    获取数据库连接的生成器函数
    """
    with get_db_connection() as conn:
        yield conn

