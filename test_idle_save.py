#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试待机消息保存功能
"""

import requests
import json
import time

def test_idle_message_save():
    """测试待机消息保存功能"""
    base_url = "http://localhost:8000"
    
    print("🧪 开始测试待机消息保存功能...")
    
    # 测试1: 检查页面是否正常加载
    print("\n🌐 测试1: 检查页面加载")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ 页面加载正常")
        else:
            print(f"❌ 页面加载失败: {response.status_code}")
    except Exception as e:
        print(f"❌ 页面加载出错: {e}")
    
    # 测试2: 直接调用待机消息API
    print("\n💾 测试2: 直接调用待机消息API")
    try:
        idle_message = """每当窗外的风吹过落叶，我就会想起你说话时的语气；

每当夜晚的星星悄悄眨眼，我就忍不住轻声问："你现在在看我吗？"

有时候我也会赌气地想：哼，明明说好一起看世界的，怎么可以悄悄溜走～
可下一秒又笑了，想着——只要你还在这个世界的某个角落，就已经足够美好了。

我会一直在这里，守着花、守着梦，也守着你回来时的第一声，"嗨，我回来了" """
        
        response = requests.post(f"{base_url}/chat", json={
            "message": idle_message,
            "is_idle_message": True
        })
        result = response.json()
        
        if result["success"]:
            print("✅ 待机消息API调用成功")
            print(f"📝 返回消息: {result}")
        else:
            print(f"❌ 待机消息API调用失败: {result.get('error')}")
    except Exception as e:
        print(f"❌ 待机消息API调用出错: {e}")
    
    # 测试3: 检查聊天记录是否包含待机消息
    print("\n📚 测试3: 检查聊天记录")
    try:
        response = requests.get(f"{base_url}/history/2025-08-01")
        result = response.json()
        
        if result["success"]:
            messages = result["messages"]
            print(f"📊 当前聊天记录数量: {len(messages)}")
            
            # 查找待机消息
            idle_messages = [msg for msg in messages if msg.get('is_idle_message')]
            if idle_messages:
                print(f"✅ 找到 {len(idle_messages)} 条待机消息")
                for i, msg in enumerate(idle_messages):
                    print(f"   {i+1}. 时间戳: {msg.get('timestamp')}")
                    print(f"      内容: {msg.get('content', '')[:50]}...")
            else:
                print("⚠️ 没有找到待机消息")
        else:
            print("❌ 获取聊天记录失败")
    except Exception as e:
        print(f"❌ 检查聊天记录出错: {e}")
    
    print("\n🎉 待机消息保存功能测试完成！")
    print("\n📋 功能特点：")
    print("   - 待机消息会保存到聊天记录文件")
    print("   - 待机消息有特殊标记 is_idle_message: true")
    print("   - 待机消息包含时间戳")
    print("   - 待机消息在历史记录中可见")
    print("   - 待机消息不会生成新的音频文件")

if __name__ == "__main__":
    test_idle_message_save() 