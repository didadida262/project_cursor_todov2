"""
数据库模型定义
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class TodoBase(BaseModel):
    """Todo基础模型"""
    title: str
    completed: bool = False

class TodoCreate(TodoBase):
    """创建Todo的模型"""
    pass

class TodoUpdate(BaseModel):
    """更新Todo的模型"""
    title: Optional[str] = None
    completed: Optional[bool] = None

class Todo(TodoBase):
    """Todo完整模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TodoResponse(BaseModel):
    """Todo响应模型"""
    id: int
    title: str
    completed: bool
    created_at: str
    updated_at: str

class MessageResponse(BaseModel):
    """消息响应模型"""
    message: str

