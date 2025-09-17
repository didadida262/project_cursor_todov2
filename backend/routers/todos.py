"""
Todo相关的API路由
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlite3 import Row
from datetime import datetime

from database import get_db_connection
from models import TodoCreate, TodoUpdate, TodoResponse, MessageResponse

router = APIRouter(prefix="/todos", tags=["todos"])

@router.get("/", response_model=List[TodoResponse])
async def get_todos(
    status: Optional[str] = Query(None, description="筛选条件: all, active, completed")
):
    """
    获取任务列表
    
    Args:
        status: 筛选条件，可选值：all(全部), active(未完成), completed(已完成)
    
    Returns:
        List[TodoResponse]: 任务列表
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # 构建查询SQL
        if status == "active":
            query = "SELECT * FROM todos WHERE completed = FALSE ORDER BY created_at DESC"
        elif status == "completed":
            query = "SELECT * FROM todos WHERE completed = TRUE ORDER BY created_at DESC"
        else:  # all 或 None
            query = "SELECT * FROM todos ORDER BY created_at DESC"
        
        cursor.execute(query)
        rows = cursor.fetchall()
        
        todos = []
        for row in rows:
            todos.append(TodoResponse(
                id=row["id"],
                title=row["title"],
                completed=bool(row["completed"]),
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            ))
        
        return todos

@router.post("/", response_model=TodoResponse)
async def create_todo(todo: TodoCreate):
    """
    创建新任务
    
    Args:
        todo: 任务创建数据
    
    Returns:
        TodoResponse: 创建的任务信息
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # 插入新任务
        cursor.execute("""
            INSERT INTO todos (title, completed, created_at, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """, (todo.title, todo.completed))
        
        # 获取新插入的任务ID
        todo_id = cursor.lastrowid
        
        # 查询新创建的任务
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        row = cursor.fetchone()
        
        conn.commit()
        
        return TodoResponse(
            id=row["id"],
            title=row["title"],
            completed=bool(row["completed"]),
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )

@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: int, todo_update: TodoUpdate):
    """
    更新任务
    
    Args:
        todo_id: 任务ID
        todo_update: 更新数据
    
    Returns:
        TodoResponse: 更新后的任务信息
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # 检查任务是否存在
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        existing_todo = cursor.fetchone()
        
        if not existing_todo:
            raise HTTPException(status_code=404, detail="任务不存在")
        
        # 构建更新SQL
        update_fields = []
        update_values = []
        
        if todo_update.title is not None:
            update_fields.append("title = ?")
            update_values.append(todo_update.title)
        
        if todo_update.completed is not None:
            update_fields.append("completed = ?")
            update_values.append(todo_update.completed)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="没有提供要更新的字段")
        
        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        update_values.append(todo_id)
        
        query = f"UPDATE todos SET {', '.join(update_fields)} WHERE id = ?"
        cursor.execute(query, update_values)
        
        # 查询更新后的任务
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        row = cursor.fetchone()
        
        conn.commit()
        
        return TodoResponse(
            id=row["id"],
            title=row["title"],
            completed=bool(row["completed"]),
            created_at=row["created_at"],
            updated_at=row["updated_at"]
        )

@router.delete("/{todo_id}", response_model=MessageResponse)
async def delete_todo(todo_id: int):
    """
    删除任务
    
    Args:
        todo_id: 任务ID
    
    Returns:
        MessageResponse: 删除结果消息
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # 检查任务是否存在
        cursor.execute("SELECT * FROM todos WHERE id = ?", (todo_id,))
        existing_todo = cursor.fetchone()
        
        if not existing_todo:
            raise HTTPException(status_code=404, detail="任务不存在")
        
        # 删除任务
        cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        conn.commit()
        
        return MessageResponse(message="任务删除成功")

@router.delete("/completed", response_model=MessageResponse)
async def delete_completed_todos():
    """
    批量删除已完成的任务
    
    Returns:
        MessageResponse: 删除结果消息
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # 查询已完成任务数量
        cursor.execute("SELECT COUNT(*) FROM todos WHERE completed = TRUE")
        count = cursor.fetchone()[0]
        
        # 删除已完成的任务
        cursor.execute("DELETE FROM todos WHERE completed = TRUE")
        conn.commit()
        
        return MessageResponse(message=f"已删除{count}个已完成任务")

@router.delete("/all", response_model=MessageResponse)
async def delete_all_todos():
    """
    清空所有任务
    
    Returns:
        MessageResponse: 删除结果消息
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # 查询总任务数量
        cursor.execute("SELECT COUNT(*) FROM todos")
        count = cursor.fetchone()[0]
        
        # 删除所有任务
        cursor.execute("DELETE FROM todos")
        conn.commit()
        
        return MessageResponse(message=f"已清空{count}个任务")

