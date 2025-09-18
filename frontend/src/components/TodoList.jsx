/**
 * TodoList 组件 - 任务列表
 */
import React, { memo } from 'react';
import TodoItem from './TodoItem';
import './TodoList.css';

const TodoList = memo(({ 
  todos, 
  onToggle, 
  onDelete, 
  loading = false 
}) => {
  /**
   * 渲染空状态
   */
  const renderEmptyState = () => (
    <div className="empty-state">
      <div className="empty-icon">📝</div>
      <div className="empty-title">暂无任务</div>
      <div className="empty-description">
        添加你的第一个任务开始管理待办事项吧！
      </div>
    </div>
  );

  /**
   * 渲染加载状态
   */
  const renderLoadingState = () => (
    <div className="loading-state">
      <div className="loading-spinner">⏳</div>
      <div className="loading-text">正在加载任务...</div>
    </div>
  );

  /**
   * 渲染任务列表
   */
  const renderTodoList = () => (
    <div className="todo-list">
      {todos.map((todo, index) => (
        <TodoItem
          key={`${todo.id}-${todo.created_at || index}`}
          todo={todo}
          onToggle={onToggle}
          onDelete={onDelete}
          loading={loading}
        />
      ))}
    </div>
  );

  if (loading && todos.length === 0) {
    return renderLoadingState();
  }

  if (todos.length === 0) {
    return renderEmptyState();
  }

  return (
    <div className="todo-list-container">
      <div className="todo-list-header">
        <div className="todo-count">
          共 {todos.length} 个任务
        </div>
        <div className="todo-stats">
          {todos.filter(todo => !todo.completed).length} 个未完成
        </div>
      </div>
      {renderTodoList()}
    </div>
  );
});

TodoList.displayName = 'TodoList';

export default TodoList;

