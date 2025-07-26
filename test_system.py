#!/usr/bin/env python3
"""
系统测试脚本
用于测试DeepSeek API和TTS模型是否正常工作
"""

import os
import sys
from dotenv import load_dotenv
from deepseek_client import DeepSeekClient
from tts_client import TTSClient
from chat_manager import ChatManager
import requests
from config import Config

def test_deepseek_api():
    """测试DeepSeek API连接"""
    print("🔍 测试DeepSeek API连接...")
    
    client = DeepSeekClient()
    
    # 检查API密钥
    if not client.api_key:
        print("❌ DeepSeek API密钥未配置")
        print("请在.env文件中设置DEEPSEEK_API_KEY")
        return False
    
    # 测试连接
    if client.test_connection():
        print("✅ DeepSeek API连接正常")
        return True
    else:
        print("❌ DeepSeek API连接失败")
        return False

def test_tts_model():
    """测试TTS模型"""
    print("🔍 测试TTS模型...")
    
    try:
        # 检查TTS模型路径
        if Config.TTS_MODEL_PATH.startswith('http'):
            # HTTP服务方式
            print(f"TTS模型路径: {Config.TTS_MODEL_PATH} (HTTP服务)")
            
            # 测试HTTP连接
            try:
                response = requests.get(Config.TTS_MODEL_PATH, timeout=5)
                if response.status_code == 200:
                    print("✅ TTS HTTP服务连接正常")
                    return True
                else:
                    print(f"❌ TTS HTTP服务连接失败: {response.status_code}")
                    return False
            except Exception as e:
                print(f"❌ TTS HTTP服务连接失败: {e}")
                return False
        else:
            # 本地文件方式
            if os.path.exists(Config.TTS_MODEL_PATH):
                print(f"✅ TTS模型路径存在: {Config.TTS_MODEL_PATH}")
                return True
            else:
                print(f"❌ TTS模型路径不存在: {Config.TTS_MODEL_PATH}")
                print("请检查TTS_MODEL_PATH配置")
                return False
                
    except Exception as e:
        print(f"❌ TTS模型测试失败: {e}")
        return False

def test_chat_system():
    """测试完整对话系统"""
    print("🔍 测试完整对话系统...")
    
    chat_manager = ChatManager()
    
    # 测试状态
    status = chat_manager.get_status()
    print(f"系统状态: {status}")
    
    # 测试简单对话
    test_message = "你好"
    result = chat_manager.process_message(test_message)
    
    if result['success']:
        print(f"✅ 对话测试成功")
        print(f"AI回复: {result['text_response']}")
        return True
    else:
        print(f"❌ 对话测试失败: {result.get('error', '未知错误')}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始系统测试...")
    print("=" * 50)
    
    # 加载环境变量
    load_dotenv()
    
    tests = [
        ("DeepSeek API", test_deepseek_api),
        ("TTS模型", test_tts_model),
        ("对话系统", test_chat_system)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n📋 测试: {test_name}")
        print("-" * 30)
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ 测试过程中发生错误: {e}")
            results[test_name] = False
    
    # 输出测试结果
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    print("=" * 50)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 所有测试通过！系统可以正常使用。")
        print("\n💡 使用说明:")
        print("  - Web界面: python main.py")
        print("  - 命令行: python main.py --cli")
    else:
        print("⚠️  部分测试失败，请检查配置和依赖。")
        print("\n🔧 故障排除:")
        print("  1. 检查.env文件配置")
        print("  2. 确认GPT-SOVITs模型路径")
        print("  3. 验证DeepSeek API密钥")
        print("  4. 检查网络连接")

if __name__ == "__main__":
    main() 