#!/usr/bin/env python3
"""
测试GPT-SOVITs HTTP服务连接
"""

import requests
import json
from config import Config

def test_tts_service():
    """测试TTS服务连接"""
    print("🔍 测试GPT-SOVITs HTTP服务...")
    
    base_url = Config.TTS_MODEL_PATH
    print(f"基础URL: {base_url}")
    
    # 测试不同的API端点
    endpoints = [
        "/tts",
        "/synthesize", 
        "/generate",
        "/api/tts",
        "/infer",
        "/"
    ]
    
    for endpoint in endpoints:
        url = f"{base_url}{endpoint}"
        print(f"\n🔗 测试端点: {url}")
        
        try:
            # 先测试GET请求
            response = requests.get(url, timeout=5)
            print(f"  GET请求状态: {response.status_code}")
            
            # 测试POST请求
            test_data = {"text": "测试"}
            response = requests.post(url, json=test_data, timeout=10)
            print(f"  POST请求状态: {response.status_code}")
            
            if response.status_code == 200:
                print(f"  ✅ 端点 {endpoint} 工作正常")
                return True
            else:
                print(f"  ❌ 端点 {endpoint} 返回错误: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"  ❌ 连接失败: 无法连接到 {url}")
        except requests.exceptions.Timeout:
            print(f"  ⏰ 请求超时: {url}")
        except Exception as e:
            print(f"  ❌ 请求失败: {e}")
    
    return False

def test_simple_request():
    """测试简单请求"""
    print("\n🧪 测试简单文本转语音...")
    
    base_url = Config.TTS_MODEL_PATH.rstrip('/')
    test_endpoints = ["/tts", "/synthesize", "/generate"]
    
    for endpoint in test_endpoints:
        url = f"{base_url}{endpoint}"
        try:
            response = requests.post(
                url,
                json={"text": "你好，这是一个测试。"},
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"✅ 成功调用 {url}")
                print(f"响应内容长度: {len(response.content)} 字节")
                return True
            else:
                print(f"❌ {url} 返回状态码: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 调用 {url} 失败: {e}")
    
    return False

def main():
    """主函数"""
    print("🤖 GPT-SOVITs HTTP服务测试")
    print("=" * 50)
    
    # 检查配置
    print(f"TTS模型路径: {Config.TTS_MODEL_PATH}")
    print(f"TTS配置路径: {Config.TTS_CONFIG_PATH}")
    
    # 测试服务连接
    if test_tts_service():
        print("\n✅ 服务连接测试通过")
        
        # 测试实际功能
        if test_simple_request():
            print("✅ 文本转语音功能测试通过")
            print("\n🎉 你的GPT-SOVITs服务配置正确！")
        else:
            print("❌ 文本转语音功能测试失败")
    else:
        print("\n❌ 服务连接测试失败")
        print("\n🔧 故障排除建议:")
        print("1. 确认GPT-SOVITs服务正在9872端口运行")
        print("2. 检查防火墙设置")
        print("3. 确认服务API端点正确")
        print("4. 检查服务日志")

if __name__ == "__main__":
    main() 