/**
 * TodoForm 组件 - 任务输入表单
 */
import React, { useState } from 'react';
import './TodoForm.css';

const TodoForm = ({ onAddTodo, loading = false }) => {
  const [title, setTitle] = useState('');
  const [error, setError] = useState('');

  /**
   * 处理表单提交
   * @param {Event} e - 表单提交事件
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // 验证输入
    if (!title.trim()) {
      setError('请输入任务标题');
      return;
    }

    if (title.trim().length > 255) {
      setError('任务标题不能超过255个字符');
      return;
    }

    try {
      setError('');
      await onAddTodo({ title: title.trim(), completed: false });
      setTitle(''); // 清空输入框
    } catch (error) {
      setError('添加任务失败，请重试');
      console.error('添加任务失败:', error);
    }
  };

  /**
   * 处理输入变化
   * @param {Event} e - 输入事件
   */
  const handleInputChange = (e) => {
    setTitle(e.target.value);
    if (error) setError(''); // 清除错误信息
  };

  /**
   * 处理键盘事件
   * @param {Event} e - 键盘事件
   */
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSubmit(e);
    }
  };

  return (
    <form className="todo-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <div className="input-container">
          <input
            type="text"
            value={title}
            onChange={handleInputChange}
            onKeyPress={handleKeyPress}
            placeholder="输入新任务..."
            className={`form-input ${error ? 'error' : ''}`}
            disabled={loading}
            maxLength={255}
          />
          <button
            type="submit"
            className="add-button"
            disabled={loading || !title.trim()}
          >
            <span>添加</span>
          </button>
        </div>
        {error && <div className="error-message">{error}</div>}
        <div className="input-hint">
          按 Enter 键或点击添加按钮创建任务
        </div>
      </div>
    </form>
  );
};

export default TodoForm;

