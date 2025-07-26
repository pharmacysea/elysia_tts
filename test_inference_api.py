#!/usr/bin/env python3
"""
测试GPT-SOVITs的inference API端点
"""

import requests
import json

def test_inference_api():
    """测试inference API端点"""
    url = "http://localhost:9872/api/inference"
    
    # 根据Web界面配置，构建正确的请求数据
    test_data = {
        "data": [
            "测试文本",  # text
            "中文",      # text_lang
            None,        # ref_audio_path (需要上传音频文件)
            [],          # aux_ref_audio_paths
            "",          # prompt_text
            "中文",      # prompt_lang
            5,           # top_k
            1,           # top_p
            1,           # temperature
            "凑四句一切", # text_split_method
            20,          # batch_size
            1.0,         # speed_factor
            False,       # ref_text_free
            True,        # split_bucket
            0.3,         # fragment_interval
            -1,          # seed
            True,        # keep_random
            True,        # parallel_infer
            1.35,        # repetition_penalty
            32,          # sample_steps
            False        # super_sampling
        ]
    }
    
    print(f"🔍 测试inference API: {url}")
    print(f"请求数据: {json.dumps(test_data, indent=2, ensure_ascii=False)}")
    
    try:
        response = requests.post(url, json=test_data, timeout=60)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            print(f"✅ 成功! 响应长度: {len(response.content)} 字节")
            
            try:
                response_data = response.json()
                print(f"响应数据: {json.dumps(response_data, indent=2, ensure_ascii=False)}")
            except:
                print("响应不是JSON格式，可能是音频数据")
            
            return True
        else:
            print(f"❌ 状态码: {response.status_code}")
            try:
                error_data = response.json()
                print(f"错误信息: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
            except:
                print(f"错误信息: {response.text[:500]}")
            
            return False
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False

def test_simple_inference():
    """测试简化的inference请求"""
    url = "http://localhost:9872/api/inference"
    
    # 简化版本，只包含必要参数
    test_data = {
        "data": [
            "你好，这是一个测试。",  # text
            "中文",                  # text_lang
            None,                    # ref_audio_path
            [],                      # aux_ref_audio_paths
            "",                      # prompt_text
            "中文",                  # prompt_lang
            5,                       # top_k
            1,                       # top_p
            1,                       # temperature
            "凑四句一切",             # text_split_method
            20,                      # batch_size
            1.0,                     # speed_factor
            False,                   # ref_text_free
            True,                    # split_bucket
            0.3,                     # fragment_interval
            -1,                      # seed
            True,                    # keep_random
            True,                    # parallel_infer
            1.35,                    # repetition_penalty
            32,                      # sample_steps
            False                    # super_sampling
        ]
    }
    
    print(f"\n🔍 测试简化inference API: {url}")
    
    try:
        response = requests.post(url, json=test_data, timeout=60)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            print(f"✅ 成功! 响应长度: {len(response.content)} 字节")
            return True
        else:
            print(f"❌ 状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False

def main():
    """主函数"""
    print("🤖 测试GPT-SOVITs inference API")
    print("=" * 60)
    
    # 测试完整API
    success = test_inference_api()
    
    if not success:
        print("\n🔄 尝试简化版本...")
        success = test_simple_inference()
    
    if success:
        print("\n🎉 inference API测试成功！")
        print("现在可以更新TTS客户端配置了。")
    else:
        print("\n❌ inference API测试失败")
        print("请检查GPT-SOVITs服务是否正常运行")

if __name__ == "__main__":
    main() 