"""
简单的API测试脚本
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_api():
    """测试API基本功能"""
    print("🧪 开始测试 Todo API...")
    
    try:
        # 测试健康检查
        response = requests.get("http://localhost:8000/health")
        print(f"✅ 健康检查: {response.status_code}")
        
        # 测试获取任务列表
        response = requests.get(f"{BASE_URL}/todos")
        print(f"✅ 获取任务列表: {response.status_code}")
        
        # 测试创建任务
        new_todo = {"title": "测试任务", "completed": False}
        response = requests.post(f"{BASE_URL}/todos", json=new_todo)
        print(f"✅ 创建任务: {response.status_code}")
        
        if response.status_code == 200:
            todo_data = response.json()
            todo_id = todo_data["id"]
            print(f"   创建的任务ID: {todo_id}")
            
            # 测试更新任务
            update_data = {"completed": True}
            response = requests.put(f"{BASE_URL}/todos/{todo_id}", json=update_data)
            print(f"✅ 更新任务: {response.status_code}")
            
            # 测试删除任务
            response = requests.delete(f"{BASE_URL}/todos/{todo_id}")
            print(f"✅ 删除任务: {response.status_code}")
        
        print("🎉 API测试完成！")
        
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到API服务器，请确保服务器正在运行")
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")

if __name__ == "__main__":
    test_api()

