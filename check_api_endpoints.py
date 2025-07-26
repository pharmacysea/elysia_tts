#!/usr/bin/env python3
"""
检查GPT-SOVITs服务的实际API端点
"""

import requests
import json

def check_root_endpoint():
    """检查根端点"""
    url = "http://localhost:9872/"
    try:
        response = requests.get(url, timeout=10)
        print(f"根端点响应状态: {response.status_code}")
        print(f"响应内容: {response.text[:500]}...")
        
        # 尝试解析JSON
        try:
            data = response.json()
            print(f"JSON响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
        except:
            print("响应不是JSON格式")
            
    except Exception as e:
        print(f"请求失败: {e}")

def check_api_endpoints():
    """检查可能的API端点"""
    base_url = "http://localhost:9872"
    
    # 更多可能的端点
    endpoints = [
        "/api/tts",
        "/api/synthesize",
        "/api/generate",
        "/tts",
        "/synthesize",
        "/generate",
        "/infer",
        "/predict",
        "/api",
        "/health",
        "/status"
    ]
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        try:
            # GET请求
            response = requests.get(url, timeout=5)
            print(f"GET {endpoint}: {response.status_code}")
            
            # POST请求
            test_data = {"text": "测试"}
            response = requests.post(url, json=test_data, timeout=5)
            print(f"POST {endpoint}: {response.status_code}")
            
            if response.status_code in [200, 201]:
                print(f"✅ 可能的端点: {endpoint}")
                print(f"响应内容: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ {endpoint}: {e}")

def test_with_different_formats():
    """测试不同的请求格式"""
    base_url = "http://localhost:9872"
    
    # 测试不同的数据格式
    test_cases = [
        {"text": "测试"},
        {"input": "测试"},
        {"message": "测试"},
        {"content": "测试"},
        {"data": "测试"},
        "测试"  # 直接字符串
    ]
    
    endpoints = ["/api/tts", "/tts", "/synthesize", "/generate"]
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        print(f"\n🔍 测试端点: {endpoint}")
        
        for i, test_data in enumerate(test_cases):
            try:
                if isinstance(test_data, str):
                    # 直接发送字符串
                    response = requests.post(url, data=test_data, timeout=5)
                else:
                    # 发送JSON
                    response = requests.post(url, json=test_data, timeout=5)
                
                print(f"  格式{i+1}: {response.status_code}")
                
                if response.status_code in [200, 201]:
                    print(f"  ✅ 成功! 响应长度: {len(response.content)}")
                    
            except Exception as e:
                print(f"  格式{i+1}: 失败 - {e}")

def main():
    """主函数"""
    print("🔍 检查GPT-SOVITs API端点")
    print("=" * 50)
    
    print("\n1. 检查根端点:")
    check_root_endpoint()
    
    print("\n2. 检查常见API端点:")
    check_api_endpoints()
    
    print("\n3. 测试不同请求格式:")
    test_with_different_formats()
    
    print("\n💡 建议:")
    print("- 查看GPT-SOVITs服务的文档")
    print("- 检查服务启动时的日志输出")
    print("- 确认正确的API端点和请求格式")

if __name__ == "__main__":
    main() 