#!/usr/bin/env python3
"""
测试GPT-SOVITs API的不同请求格式
"""

import requests
import json

def test_api_formats():
    """测试不同的API请求格式"""
    url = "http://localhost:9872/api/tts"
    
    # 测试不同的请求格式
    test_cases = [
        # 基本格式
        {"text": "测试文本"},
        {"input": "测试文本"},
        {"message": "测试文本"},
        {"content": "测试文本"},
        
        # 带额外参数
        {"text": "测试文本", "speed": 1.0},
        {"text": "测试文本", "pitch": 0},
        {"text": "测试文本", "volume": 1.0},
        {"text": "测试文本", "speaker": "default"},
        
        # 不同字段名
        {"input_text": "测试文本"},
        {"sentence": "测试文本"},
        {"words": "测试文本"},
        {"prompt": "测试文本"},
        
        # 数组格式
        {"text": ["测试", "文本"]},
        {"inputs": ["测试", "文本"]},
        
        # 嵌套格式
        {"data": {"text": "测试文本"}},
        {"request": {"text": "测试文本"}},
        
        # 其他可能的格式
        {"text": "测试文本", "model": "default"},
        {"text": "测试文本", "voice": "default"},
        {"text": "测试文本", "language": "zh"},
        {"text": "测试文本", "format": "wav"},
    ]
    
    print(f"🔍 测试API端点: {url}")
    print("=" * 60)
    
    for i, test_data in enumerate(test_cases):
        try:
            print(f"\n📝 测试格式 {i+1}: {test_data}")
            
            response = requests.post(url, json=test_data, timeout=10)
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                print(f"✅ 成功! 响应长度: {len(response.content)} 字节")
                return test_data
            elif response.status_code == 422:
                # 尝试解析错误信息
                try:
                    error_data = response.json()
                    print(f"❌ 422错误: {error_data}")
                except:
                    print(f"❌ 422错误: {response.text[:200]}")
            else:
                print(f"❌ 状态码: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 请求失败: {e}")
    
    return None

def test_with_headers():
    """测试不同的请求头"""
    url = "http://localhost:9872/api/tts"
    test_data = {"text": "测试文本"}
    
    headers_variants = [
        {"Content-Type": "application/json"},
        {"Content-Type": "application/json", "Accept": "audio/wav"},
        {"Content-Type": "application/json", "Accept": "audio/*"},
        {"Content-Type": "application/json", "Accept": "*/*"},
        {"Content-Type": "application/json", "User-Agent": "TTS-Client"},
    ]
    
    print(f"\n🔍 测试不同请求头: {url}")
    print("=" * 60)
    
    for i, headers in enumerate(headers_variants):
        try:
            print(f"\n📝 测试请求头 {i+1}: {headers}")
            
            response = requests.post(url, json=test_data, headers=headers, timeout=10)
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                print(f"✅ 成功! 响应长度: {len(response.content)} 字节")
                return headers
            else:
                print(f"❌ 状态码: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 请求失败: {e}")
    
    return None

def check_api_documentation():
    """检查API文档端点"""
    base_url = "http://localhost:9872"
    
    doc_endpoints = [
        "/docs",
        "/api/docs",
        "/swagger",
        "/api/swagger",
        "/openapi.json",
        "/api/openapi.json",
        "/schema",
        "/api/schema"
    ]
    
    print(f"\n🔍 检查API文档端点")
    print("=" * 60)
    
    for endpoint in doc_endpoints:
        url = f"{base_url}{endpoint}"
        try:
            response = requests.get(url, timeout=5)
            print(f"{endpoint}: {response.status_code}")
            
            if response.status_code == 200:
                print(f"✅ 找到文档: {url}")
                print(f"内容预览: {response.text[:200]}...")
                
        except Exception as e:
            print(f"{endpoint}: 失败 - {e}")

def main():
    """主函数"""
    print("🧪 测试GPT-SOVITs API格式")
    print("=" * 60)
    
    # 测试不同的请求格式
    working_format = test_api_formats()
    
    if working_format:
        print(f"\n🎉 找到工作格式: {working_format}")
    else:
        print("\n❌ 未找到工作格式")
    
    # 测试不同的请求头
    working_headers = test_with_headers()
    
    if working_headers:
        print(f"\n🎉 找到工作请求头: {working_headers}")
    else:
        print("\n❌ 未找到工作请求头")
    
    # 检查API文档
    check_api_documentation()
    
    print("\n💡 建议:")
    print("1. 查看GPT-SOVITs服务的Web界面")
    print("2. 检查服务启动时的日志")
    print("3. 查看项目文档或README")

if __name__ == "__main__":
    main() 