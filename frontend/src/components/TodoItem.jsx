/**
 * TodoItem 组件 - 单个任务项
 */
import React from 'react';
import './TodoItem.css';

const TodoItem = ({ 
  todo, 
  onToggle, 
  onDelete, 
  loading = false 
}) => {
  const { id, title, completed, created_at } = todo;

  /**
   * 处理完成状态切换
   */
  const handleToggle = async () => {
    try {
      await onToggle(id, !completed);
    } catch (error) {
      console.error('切换任务状态失败:', error);
    }
  };

  /**
   * 处理删除任务
   */
  const handleDelete = async () => {
    if (window.confirm('确定要删除这个任务吗？')) {
      try {
        await onDelete(id);
      } catch (error) {
        console.error('删除任务失败:', error);
      }
    }
  };

  /**
   * 格式化日期
   * @param {string} dateString - 日期字符串
   * @returns {string} 格式化后的日期
   */
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 1) {
      return '今天';
    } else if (diffDays === 2) {
      return '昨天';
    } else if (diffDays <= 7) {
      return `${diffDays - 1}天前`;
    } else {
      return date.toLocaleDateString('zh-CN', {
        month: 'short',
        day: 'numeric'
      });
    }
  };

  return (
    <div className={`todo-item ${completed ? 'completed' : ''} ${loading ? 'loading' : ''}`}>
      <div className="todo-content">
        <div className="todo-main">
          <button
            className={`toggle-button ${completed ? 'completed' : ''}`}
            onClick={handleToggle}
            disabled={loading}
            title={completed ? '标记为未完成' : '标记为完成'}
          >
            {completed ? '✓' : '○'}
          </button>
          
          <div className="todo-text">
            <span className={`todo-title ${completed ? 'completed' : ''}`}>
              {title}
            </span>
            <span className="todo-date">
              {formatDate(created_at)}
            </span>
          </div>
        </div>
        
        <div className="todo-actions">
          <button
            className="delete-button"
            onClick={handleDelete}
            disabled={loading}
            title="删除任务"
          >
            🗑️
          </button>
        </div>
      </div>
      
      {loading && (
        <div className="loading-overlay">
          <div className="loading-spinner">⏳</div>
        </div>
      )}
    </div>
  );
};

export default TodoItem;

