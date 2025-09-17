/**
 * API服务层 - 处理与后端的所有通信
 */
import axios from 'axios';

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    console.log(`🚀 API请求: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ 请求错误:', error);
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API响应: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('❌ 响应错误:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

/**
 * Todo API 服务类
 */
class TodoAPI {
  /**
   * 获取任务列表
   * @param {string} status - 筛选条件: 'all', 'active', 'completed'
   * @returns {Promise<Array>} 任务列表
   */
  async getTodos(status = 'all') {
    try {
      const response = await api.get('/todos', {
        params: { status }
      });
      return response.data;
    } catch (error) {
      console.error('获取任务列表失败:', error);
      throw new Error('获取任务列表失败');
    }
  }

  /**
   * 创建新任务
   * @param {Object} todoData - 任务数据
   * @param {string} todoData.title - 任务标题
   * @param {boolean} todoData.completed - 完成状态
   * @returns {Promise<Object>} 创建的任务
   */
  async createTodo(todoData) {
    try {
      const response = await api.post('/todos', todoData);
      return response.data;
    } catch (error) {
      console.error('创建任务失败:', error);
      throw new Error('创建任务失败');
    }
  }

  /**
   * 更新任务
   * @param {number} id - 任务ID
   * @param {Object} updateData - 更新数据
   * @returns {Promise<Object>} 更新后的任务
   */
  async updateTodo(id, updateData) {
    try {
      const response = await api.put(`/todos/${id}`, updateData);
      return response.data;
    } catch (error) {
      console.error('更新任务失败:', error);
      throw new Error('更新任务失败');
    }
  }

  /**
   * 删除任务
   * @param {number} id - 任务ID
   * @returns {Promise<string>} 删除结果消息
   */
  async deleteTodo(id) {
    try {
      const response = await api.delete(`/todos/${id}`);
      return response.data.message;
    } catch (error) {
      console.error('删除任务失败:', error);
      throw new Error('删除任务失败');
    }
  }

  /**
   * 批量删除已完成任务
   * @returns {Promise<string>} 删除结果消息
   */
  async deleteCompletedTodos() {
    try {
      const response = await api.delete('/todos/completed');
      return response.data.message;
    } catch (error) {
      console.error('批量删除已完成任务失败:', error);
      throw new Error('批量删除已完成任务失败');
    }
  }

  /**
   * 清空所有任务
   * @returns {Promise<string>} 删除结果消息
   */
  async deleteAllTodos() {
    try {
      const response = await api.delete('/todos/all');
      return response.data.message;
    } catch (error) {
      console.error('清空所有任务失败:', error);
      throw new Error('清空所有任务失败');
    }
  }

  /**
   * 检查API连接状态
   * @returns {Promise<boolean>} 连接状态
   */
  async checkConnection() {
    try {
      const response = await axios.get('http://localhost:8000/health');
      return response.status === 200;
    } catch (error) {
      console.error('API连接检查失败:', error);
      return false;
    }
  }
}

// 创建API实例
const todoAPI = new TodoAPI();

export default todoAPI;

