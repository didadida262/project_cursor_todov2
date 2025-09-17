/**
 * React应用入口文件
 */
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

// 创建React根节点
const root = ReactDOM.createRoot(document.getElementById('root'));

// 渲染应用
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

