/**
 * 主应用组件 - Todo应用入口
 */
import React, { useState, useEffect, useCallback, startTransition, useMemo } from 'react';
import './styles/App.css';
import TodoForm from './components/TodoForm';
import TodoList from './components/TodoList';
import FilterBar from './components/FilterBar';
import Toast from './components/Toast';
import todoAPI from './services/api';

function App() {
  // 状态管理
  const [todos, setTodos] = useState([]);
  const [filter, setFilter] = useState('all');
  const [loading, setLoading] = useState(false);
  const [addingTodo, setAddingTodo] = useState(false);
  const [error, setError] = useState('');
  const [toast, setToast] = useState({ message: '', type: 'success' });
  const [connectionStatus, setConnectionStatus] = useState('loading');

  /**
   * 显示Toast提示
   * @param {string} message - 提示消息
   * @param {string} type - 提示类型: 'success', 'error', 'warning', 'info'
   */
  const showToast = useCallback((message, type = 'success') => {
    setToast({ message, type });
  }, []);

  /**
   * 隐藏Toast提示
   */
  const hideToast = () => {
    setToast({ message: '', type: 'success' });
  };

  /**
   * 获取任务列表
   * @param {string} status - 筛选状态
   */
  const fetchTodos = useCallback(async (status = filter) => {
    try {
      setLoading(true);
      setError('');
      const data = await todoAPI.getTodos(status);
      setTodos(data);
    } catch (err) {
      setError('获取任务列表失败，请检查网络连接');
      console.error('获取任务失败:', err);
    } finally {
      setLoading(false);
    }
  }, [filter]);

  /**
   * 添加新任务
   * @param {Object} todoData - 任务数据
   */
  const handleAddTodo = async (todoData) => {
    const startTime = Date.now();
    
    try {
      setAddingTodo(true);
      setError('');
      const newTodo = await todoAPI.createTodo(todoData);
      
      // 使用startTransition标记非紧急更新，减少闪烁
      startTransition(() => {
        setTodos(prevTodos => [newTodo, ...prevTodos]);
      });
      
      // 延迟显示Toast，避免与列表更新冲突
      setTimeout(() => {
        showToast('任务添加成功！', 'success');
      }, 100);
    } catch (err) {
      setError('添加任务失败，请重试');
      showToast('添加任务失败，请重试', 'error');
      console.error('添加任务失败:', err);
    } finally {
      // 确保loading至少显示1秒
      const elapsedTime = Date.now() - startTime;
      const remainingTime = Math.max(0, 1000 - elapsedTime);
      
      setTimeout(() => {
        setAddingTodo(false);
      }, remainingTime);
    }
  };

  /**
   * 切换任务完成状态
   * @param {number} id - 任务ID
   * @param {boolean} completed - 完成状态
   */
  const handleToggleTodo = async (id, completed) => {
    try {
      setLoading(true);
      setError('');
      const updatedTodo = await todoAPI.updateTodo(id, { completed });
      setTodos(prevTodos =>
        prevTodos.map(todo =>
          todo.id === id ? updatedTodo : todo
        )
      );
      showToast(completed ? '任务已完成！' : '任务已标记为未完成', 'success');
    } catch (err) {
      setError('更新任务状态失败，请重试');
      console.error('更新任务失败:', err);
    } finally {
      setLoading(false);
    }
  };

  /**
   * 删除单个任务
   * @param {number} id - 任务ID
   */
  const handleDeleteTodo = async (id) => {
    try {
      setLoading(true);
      setError('');
      await todoAPI.deleteTodo(id);
      setTodos(prevTodos => prevTodos.filter(todo => todo.id !== id));
      showToast('任务删除成功！', 'success');
    } catch (err) {
      setError('删除任务失败，请重试');
      console.error('删除任务失败:', err);
    } finally {
      setLoading(false);
    }
  };

  /**
   * 批量删除已完成任务
   */
  const handleClearCompleted = async () => {
    try {
      setLoading(true);
      setError('');
      const message = await todoAPI.deleteCompletedTodos();
      setTodos(prevTodos => prevTodos.filter(todo => !todo.completed));
      showToast(message, 'success');
    } catch (err) {
      setError('批量删除失败，请重试');
      console.error('批量删除失败:', err);
    } finally {
      setLoading(false);
    }
  };

  /**
   * 清空所有任务
   */
  const handleClearAll = async () => {
    try {
      setLoading(true);
      setError('');
      const message = await todoAPI.deleteAllTodos();
      setTodos([]);
      showToast(message, 'success');
    } catch (err) {
      setError('清空任务失败，请重试');
      console.error('清空任务失败:', err);
    } finally {
      setLoading(false);
    }
  };

  /**
   * 处理筛选变化
   * @param {string} newFilter - 新的筛选条件
   */
  const handleFilterChange = (newFilter) => {
    if (newFilter === filter) return; // 避免重复筛选
    setFilter(newFilter);
  };

  /**
   * 检查API连接状态
   */
  const checkConnection = async () => {
    try {
      const isConnected = await todoAPI.checkConnection();
      setConnectionStatus(isConnected ? 'connected' : 'disconnected');
    } catch (err) {
      setConnectionStatus('disconnected');
    }
  };

  // 组件挂载时获取数据
  useEffect(() => {
    fetchTodos();
    checkConnection();
  }, []);

  // 定期检查连接状态
  useEffect(() => {
    const interval = setInterval(checkConnection, 30000); // 每30秒检查一次
    return () => clearInterval(interval);
  }, []);

  // 根据筛选条件过滤任务（客户端筛选，减少API调用）
  const filteredTodos = useMemo(() => {
    return todos.filter(todo => {
      switch (filter) {
        case 'active':
          return !todo.completed;
        case 'completed':
          return todo.completed;
        default:
          return true;
      }
    });
  }, [todos, filter]);

  return (
    <div className="app">
      {/* 连接状态指示器 */}
      <div className={`status-indicator ${connectionStatus}`}>
        {connectionStatus === 'connected' && '🟢 已连接'}
        {connectionStatus === 'disconnected' && '🔴 连接断开'}
        {connectionStatus === 'loading' && '🟡 连接中...'}
      </div>

      <div className="app-container">
        {/* 应用头部 */}
        <header className="app-header">
          <h1 className="app-title">📝 Todo 待办事项</h1>
          <p className="app-subtitle">高效管理你的日常任务</p>
        </header>

        {/* 应用主体 */}
        <main className="app-main">
          {/* 错误提示 */}
          {error && (
            <div className="error-message">
              {error}
            </div>
          )}


          {/* 任务输入表单 */}
          <TodoForm
            onAddTodo={handleAddTodo}
            loading={addingTodo}
          />

          {/* 筛选和批量操作栏 */}
          <FilterBar
            currentFilter={filter}
            onFilterChange={handleFilterChange}
            onClearCompleted={handleClearCompleted}
            onClearAll={handleClearAll}
            todos={todos}
            loading={loading}
          />

          {/* 任务列表 */}
          <div key={filter} className="todo-list-wrapper">
            <div className="todo-list-container">
              <TodoList
                todos={filteredTodos}
                onToggle={handleToggleTodo}
                onDelete={handleDeleteTodo}
                loading={loading}
              />
            </div>
          </div>
        </main>
      </div>

      {/* 全局加载遮罩 - 只在批量操作时显示 */}
      {loading && !addingTodo && (
        <div className="loading-overlay">
          <div className="loading-content">
            <div className="loading-spinner"></div>
            <div>处理中...</div>
          </div>
        </div>
      )}

      {/* 添加任务loading遮罩 - 居中显示 */}
      {addingTodo && (
        <div className="adding-todo-overlay">
          <div className="adding-todo-content">
            <div className="loading-spinner"></div>
            <div>添加任务中...</div>
          </div>
        </div>
      )}

      {/* Toast 浮窗提示 */}
      <Toast
        message={toast.message}
        type={toast.type}
        onClose={hideToast}
        duration={3000}
      />
    </div>
  );
}

export default App;

