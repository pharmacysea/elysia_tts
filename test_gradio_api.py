#!/usr/bin/env python3
"""
测试Gradio API的正确格式
"""

import requests
import json

def test_gradio_api():
    """测试Gradio API"""
    base_url = "http://localhost:9872"
    
    # 测试不同的API端点
    endpoints = [
        "/api/tts",
        "/call/tts", 
        "/api/synthesize",
        "/call/synthesize",
        "/api/generate",
        "/call/generate",
        "/api/infer",
        "/call/infer"
    ]
    
    # 测试不同的数据格式
    test_cases = [
        # 基本格式 - data字段包含文本
        {"data": ["测试文本"]},
        {"data": ["你好，这是一个测试。"]},
        
        # 带session_hash
        {"data": ["测试文本"], "session_hash": "test123"},
        
        # 简单格式
        {"data": ["测试文本"]},
        
        # 多个参数
        {"data": ["测试文本", 1.0, 0]},  # 文本, 速度, 音调
        {"data": ["测试文本", "default"]},  # 文本, 说话人
    ]
    
    print("🧪 测试Gradio API格式")
    print("=" * 60)
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        print(f"\n🔍 测试端点: {endpoint}")
        
        for i, test_data in enumerate(test_cases):
            try:
                print(f"  格式 {i+1}: {test_data}")
                
                response = requests.post(url, json=test_data, timeout=30)
                print(f"  状态码: {response.status_code}")
                
                if response.status_code == 200:
                    print(f"  ✅ 成功! 响应长度: {len(response.content)} 字节")
                    
                    # 检查响应内容
                    try:
                        response_data = response.json()
                        print(f"  响应数据: {response_data}")
                    except:
                        print(f"  响应不是JSON格式，可能是音频数据")
                    
                    return {
                        "endpoint": endpoint,
                        "format": test_data,
                        "url": url
                    }
                elif response.status_code == 422:
                    try:
                        error_data = response.json()
                        print(f"  ❌ 422错误: {error_data}")
                    except:
                        print(f"  ❌ 422错误: {response.text[:200]}")
                else:
                    print(f"  ❌ 状态码: {response.status_code}")
                    
            except Exception as e:
                print(f"  ❌ 请求失败: {e}")
    
    return None

def test_simple_call():
    """测试简单的call端点"""
    base_url = "http://localhost:9872"
    
    # 尝试不同的API名称
    api_names = ["tts", "synthesize", "generate", "infer", "text2speech", "speech"]
    
    for api_name in api_names:
        url = f"{base_url}/call/{api_name}"
        print(f"\n🔍 测试简单call端点: {url}")
        
        test_data = {"data": ["测试文本"]}
        
        try:
            response = requests.post(url, json=test_data, timeout=30)
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                print(f"✅ 成功! 响应长度: {len(response.content)} 字节")
                return {
                    "endpoint": f"/call/{api_name}",
                    "format": test_data,
                    "url": url
                }
            else:
                print(f"❌ 状态码: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 请求失败: {e}")
    
    return None

def main():
    """主函数"""
    print("🤖 测试Gradio API格式")
    print("=" * 60)
    
    # 测试标准API端点
    result = test_gradio_api()
    
    if result:
        print(f"\n🎉 找到工作配置:")
        print(f"端点: {result['endpoint']}")
        print(f"格式: {result['format']}")
        print(f"URL: {result['url']}")
    else:
        print("\n❌ 标准API端点测试失败")
        
        # 测试简单call端点
        result = test_simple_call()
        
        if result:
            print(f"\n🎉 找到工作配置:")
            print(f"端点: {result['endpoint']}")
            print(f"格式: {result['format']}")
            print(f"URL: {result['url']}")
        else:
            print("\n❌ 所有API端点测试失败")
            print("\n💡 建议:")
            print("1. 检查GPT-SOVITs服务的Web界面")
            print("2. 查看服务启动日志")
            print("3. 确认API名称")

if __name__ == "__main__":
    main() 