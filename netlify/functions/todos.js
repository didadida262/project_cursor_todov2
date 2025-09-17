/**
 * Netlify Functions - Todo API
 */
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

// 数据库文件路径
const DB_PATH = '/tmp/todos.db';

// 初始化数据库
function initDatabase() {
  return new Promise((resolve, reject) => {
    const db = new sqlite3.Database(DB_PATH, (err) => {
      if (err) {
        reject(err);
        return;
      }
      
      db.serialize(() => {
        db.run(`
          CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(255) NOT NULL,
            completed BOOLEAN DEFAULT FALSE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
          )
        `);
      });
      
      resolve(db);
    });
  });
}

// 处理 CORS
function setCorsHeaders(response) {
  response.headers = {
    ...response.headers,
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
  };
  return response;
}

exports.handler = async (event, context) => {
  // 处理 CORS 预检请求
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
      },
      body: ''
    };
  }

  try {
    const db = await initDatabase();
    const { httpMethod, path, queryStringParameters, body } = event;
    
    // 解析路径
    const pathParts = path.split('/').filter(part => part);
    const endpoint = pathParts[pathParts.length - 1];
    
    let result;
    
    switch (httpMethod) {
      case 'GET':
        if (endpoint === 'health') {
          result = { status: 'healthy', message: '服务运行正常' };
        } else {
          result = await getTodos(db, queryStringParameters);
        }
        break;
        
      case 'POST':
        result = await createTodo(db, JSON.parse(body || '{}'));
        break;
        
      case 'PUT':
        const todoId = pathParts[pathParts.length - 1];
        result = await updateTodo(db, todoId, JSON.parse(body || '{}'));
        break;
        
      case 'DELETE':
        if (endpoint === 'completed') {
          result = await deleteCompletedTodos(db);
        } else if (endpoint === 'all') {
          result = await deleteAllTodos(db);
        } else {
          const todoId = pathParts[pathParts.length - 1];
          result = await deleteTodo(db, todoId);
        }
        break;
        
      default:
        return setCorsHeaders({
          statusCode: 405,
          body: JSON.stringify({ error: 'Method not allowed' })
        });
    }
    
    db.close();
    
    return setCorsHeaders({
      statusCode: 200,
      body: JSON.stringify(result)
    });
    
  } catch (error) {
    console.error('Error:', error);
    return setCorsHeaders({
      statusCode: 500,
      body: JSON.stringify({ error: error.message })
    });
  }
};

// 获取任务列表
function getTodos(db, queryParams) {
  return new Promise((resolve, reject) => {
    const status = queryParams?.status || 'all';
    let query = 'SELECT * FROM todos';
    
    if (status === 'active') {
      query += ' WHERE completed = FALSE';
    } else if (status === 'completed') {
      query += ' WHERE completed = TRUE';
    }
    
    query += ' ORDER BY created_at DESC';
    
    db.all(query, [], (err, rows) => {
      if (err) {
        reject(err);
        return;
      }
      
      const todos = rows.map(row => ({
        id: row.id,
        title: row.title,
        completed: Boolean(row.completed),
        created_at: row.created_at,
        updated_at: row.updated_at
      }));
      
      resolve(todos);
    });
  });
}

// 创建任务
function createTodo(db, todoData) {
  return new Promise((resolve, reject) => {
    const { title, completed = false } = todoData;
    
    db.run(
      'INSERT INTO todos (title, completed) VALUES (?, ?)',
      [title, completed],
      function(err) {
        if (err) {
          reject(err);
          return;
        }
        
        const todoId = this.lastID;
        db.get('SELECT * FROM todos WHERE id = ?', [todoId], (err, row) => {
          if (err) {
            reject(err);
            return;
          }
          
          resolve({
            id: row.id,
            title: row.title,
            completed: Boolean(row.completed),
            created_at: row.created_at,
            updated_at: row.updated_at
          });
        });
      }
    );
  });
}

// 更新任务
function updateTodo(db, todoId, updateData) {
  return new Promise((resolve, reject) => {
    const { title, completed } = updateData;
    const updates = [];
    const values = [];
    
    if (title !== undefined) {
      updates.push('title = ?');
      values.push(title);
    }
    
    if (completed !== undefined) {
      updates.push('completed = ?');
      values.push(completed);
    }
    
    if (updates.length === 0) {
      reject(new Error('No fields to update'));
      return;
    }
    
    updates.push('updated_at = CURRENT_TIMESTAMP');
    values.push(todoId);
    
    const query = `UPDATE todos SET ${updates.join(', ')} WHERE id = ?`;
    
    db.run(query, values, function(err) {
      if (err) {
        reject(err);
        return;
      }
      
      if (this.changes === 0) {
        reject(new Error('Task not found'));
        return;
      }
      
      db.get('SELECT * FROM todos WHERE id = ?', [todoId], (err, row) => {
        if (err) {
          reject(err);
          return;
        }
        
        resolve({
          id: row.id,
          title: row.title,
          completed: Boolean(row.completed),
          created_at: row.created_at,
          updated_at: row.updated_at
        });
      });
    });
  });
}

// 删除任务
function deleteTodo(db, todoId) {
  return new Promise((resolve, reject) => {
    db.run('DELETE FROM todos WHERE id = ?', [todoId], function(err) {
      if (err) {
        reject(err);
        return;
      }
      
      if (this.changes === 0) {
        reject(new Error('Task not found'));
        return;
      }
      
      resolve({ message: '任务删除成功' });
    });
  });
}

// 删除已完成任务
function deleteCompletedTodos(db) {
  return new Promise((resolve, reject) => {
    db.get('SELECT COUNT(*) as count FROM todos WHERE completed = TRUE', [], (err, row) => {
      if (err) {
        reject(err);
        return;
      }
      
      const count = row.count;
      
      db.run('DELETE FROM todos WHERE completed = TRUE', [], (err) => {
        if (err) {
          reject(err);
          return;
        }
        
        resolve({ message: `已删除${count}个已完成任务` });
      });
    });
  });
}

// 删除所有任务
function deleteAllTodos(db) {
  return new Promise((resolve, reject) => {
    db.get('SELECT COUNT(*) as count FROM todos', [], (err, row) => {
      if (err) {
        reject(err);
        return;
      }
      
      const count = row.count;
      
      db.run('DELETE FROM todos', [], (err) => {
        if (err) {
          reject(err);
          return;
        }
        
        resolve({ message: `已清空${count}个任务` });
      });
    });
  });
}
