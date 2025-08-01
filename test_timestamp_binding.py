#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试时间戳绑定功能
验证聊天记录与音频文件的时间戳绑定是否正常工作
"""

import os
import json
import time
from datetime import datetime
from chat_manager import ChatManager

def test_timestamp_binding():
    """测试时间戳绑定功能"""
    print("🧪 开始测试时间戳绑定功能...")
    
    # 创建聊天管理器实例
    chat_manager = ChatManager()
    
    # 测试1: 发送消息并检查时间戳
    print("\n📝 测试1: 发送消息并检查时间戳")
    test_message = "你好，这是时间戳绑定测试"
    result = chat_manager.process_message(test_message)
    
    if result["success"]:
        print(f"✅ 消息处理成功")
        print(f"📊 用户时间戳: {result.get('user_timestamp')}")
        print(f"📊 助手时间戳: {result.get('assistant_timestamp')}")
        print(f"🎵 音频文件: {result.get('audio_path')}")
    else:
        print(f"❌ 消息处理失败: {result.get('error')}")
        return
    
    # 测试2: 检查聊天记录格式
    print("\n📋 测试2: 检查聊天记录格式")
    history = chat_manager.get_history()
    
    if len(history) >= 2:
        user_msg = history[-2]  # 倒数第二条是用户消息
        assistant_msg = history[-1]  # 最后一条是助手消息
        
        print(f"👤 用户消息: {user_msg}")
        print(f"🤖 助手消息: {assistant_msg}")
        
        # 检查时间戳
        if 'timestamp' in user_msg and 'timestamp' in assistant_msg:
            print("✅ 时间戳字段存在")
            
            # 检查音频文件
            if 'audio_file' in assistant_msg:
                print(f"✅ 音频文件字段存在: {assistant_msg['audio_file']}")
                
                # 验证音频文件是否存在
                audio_exists = chat_manager.verify_audio_file(assistant_msg['audio_file'])
                print(f"📁 音频文件存在: {audio_exists}")
            else:
                print("⚠️ 音频文件字段不存在")
        else:
            print("❌ 时间戳字段缺失")
    
    # 测试3: 检查音频文件信息
    print("\n🎵 测试3: 检查音频文件信息")
    audio_info = chat_manager.get_audio_files_info()
    print(f"📊 音频文件统计:")
    print(f"   总文件数: {audio_info['total_files']}")
    print(f"   存在文件: {audio_info['existing_files']}")
    print(f"   缺失文件: {audio_info['missing_files']}")
    
    # 显示最近的几个音频文件
    if audio_info['files']:
        print(f"\n📁 最近的音频文件:")
        recent_files = sorted(audio_info['files'], key=lambda x: x['filename'], reverse=True)[:5]
        for file_info in recent_files:
            status = "✅" if file_info['exists'] else "❌"
            size_mb = file_info['size'] / (1024 * 1024) if file_info['size'] > 0 else 0
            print(f"   {status} {file_info['filename']} ({size_mb:.2f}MB)")
    
    # 测试4: 测试向后兼容性
    print("\n🔄 测试4: 测试向后兼容性")
    
    # 创建一个模拟的旧格式聊天记录
    old_format_data = {
        "date": "2025-08-01",
        "messages": [
            {
                "role": "user",
                "content": "这是旧格式的用户消息"
            },
            {
                "role": "assistant", 
                "content": "这是旧格式的助手消息",
                "audio_file": "response_1754038556.wav"
            }
        ]
    }
    
    # 保存旧格式数据
    test_file = "./chat_history/test_backward_compatibility.json"
    os.makedirs("./chat_history", exist_ok=True)
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(old_format_data, f, ensure_ascii=False, indent=2)
    
    print(f"📝 创建测试文件: {test_file}")
    
    # 模拟加载旧格式数据
    try:
        with open(test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            messages = data.get('messages', [])
            
            # 处理向后兼容性
            processed_messages = []
            base_timestamp = int(time.time()) - len(messages) * 10
            
            for i, message in enumerate(messages):
                processed_message = message.copy()
                
                # 如果没有时间戳，添加一个
                if 'timestamp' not in processed_message:
                    processed_message['timestamp'] = base_timestamp + i * 10
                
                # 对于assistant消息，检查音频文件是否存在
                if processed_message.get('role') == 'assistant' and 'audio_file' in processed_message:
                    audio_filename = processed_message['audio_file']
                    audio_full_path = os.path.join(chat_manager.tts_client.output_path, audio_filename)
                    processed_message['audio_exists'] = os.path.exists(audio_full_path)
                
                processed_messages.append(processed_message)
            
            print(f"✅ 向后兼容性处理完成")
            print(f"📊 处理后的消息:")
            for msg in processed_messages:
                print(f"   {msg}")
    
    except Exception as e:
        print(f"❌ 向后兼容性测试失败: {e}")
    
    # 清理测试文件
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f"🧹 清理测试文件: {test_file}")
    
    print("\n🎉 时间戳绑定功能测试完成！")

if __name__ == "__main__":
    test_timestamp_binding() 