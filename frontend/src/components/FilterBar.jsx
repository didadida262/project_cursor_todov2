/**
 * FilterBar 组件 - 筛选和批量操作栏
 */
import React from 'react';
import './FilterBar.css';

const FilterBar = ({ 
  currentFilter, 
  onFilterChange, 
  onClearCompleted, 
  onClearAll,
  todos = [],
  loading = false 
}) => {
  const completedCount = todos.filter(todo => todo.completed).length;
  const hasCompleted = completedCount > 0;
  const hasTodos = todos.length > 0;

  /**
   * 筛选选项配置
   */
  const filterOptions = [
    { value: 'all', label: '全部', count: todos.length },
    { value: 'active', label: '未完成', count: todos.filter(todo => !todo.completed).length },
    { value: 'completed', label: '已完成', count: completedCount }
  ];

  /**
   * 处理筛选变化
   * @param {string} filter - 筛选条件
   */
  const handleFilterChange = (filter) => {
    if (filter !== currentFilter) {
      onFilterChange(filter);
    }
  };

  /**
   * 处理清除已完成任务
   */
  const handleClearCompleted = () => {
    if (hasCompleted && window.confirm(`确定要删除 ${completedCount} 个已完成的任务吗？`)) {
      onClearCompleted();
    }
  };

  /**
   * 处理清空所有任务
   */
  const handleClearAll = () => {
    if (hasTodos && window.confirm(`确定要清空所有 ${todos.length} 个任务吗？此操作不可撤销！`)) {
      onClearAll();
    }
  };

  return (
    <div className="filter-bar">
      <div className="filter-tabs">
        {filterOptions.map((option) => (
          <button
            key={option.value}
            className={`filter-tab ${currentFilter === option.value ? 'active' : ''}`}
            onClick={() => handleFilterChange(option.value)}
            disabled={loading}
          >
            <span className="filter-label">{option.label}</span>
            <span className="filter-count">{option.count}</span>
          </button>
        ))}
      </div>
      
      <div className="filter-actions">
        {hasCompleted && (
          <button
            className="action-button clear-completed"
            onClick={handleClearCompleted}
            disabled={loading}
            title={`删除 ${completedCount} 个已完成任务`}
          >
            🗑️ 清除已完成
          </button>
        )}
        
        {hasTodos && (
          <button
            className="action-button clear-all"
            onClick={handleClearAll}
            disabled={loading}
            title={`清空所有 ${todos.length} 个任务`}
          >
            🧹 清空全部
          </button>
        )}
      </div>
    </div>
  );
};

export default FilterBar;

