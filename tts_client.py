import os
import subprocess
import tempfile
import json
from typing import Optional
from config import Config

class TTSClient:
    def __init__(self):
        self.model_path = Config.TTS_MODEL_PATH
        self.config_path = Config.TTS_CONFIG_PATH
        self.output_path = Config.AUDIO_OUTPUT_PATH
        
        # 确保输出目录存在
        os.makedirs(self.output_path, exist_ok=True)
    
    def text_to_speech(self, text: str, output_filename: Optional[str] = None) -> Optional[str]:
        """
        将文本转换为语音
        
        Args:
            text: 要转换的文本
            output_filename: 输出文件名（可选）
            
        Returns:
            str: 生成的音频文件路径，失败时返回None
        """
        if not output_filename:
            import time
            output_filename = f"tts_output_{int(time.time())}.wav"
        
        output_path = os.path.join(self.output_path, output_filename)
        
        try:
            # 这里需要根据你的GPT-SOVITs具体实现来调用
            # 以下是几种常见的调用方式，你需要根据实际情况调整
            
            # 方式1: 如果GPT-SOVITs提供了Python API
            if self._has_python_api():
                return self._call_python_api(text, output_path)
            
            # 方式2: 如果GPT-SOVITs提供了命令行接口
            elif self._has_cli_interface():
                return self._call_cli_interface(text, output_path)
            
            # 方式3: 如果GPT-SOVITs提供了HTTP API
            elif self._has_http_api():
                return self._call_http_api(text, output_path)
            
            else:
                print("未找到可用的TTS接口，请检查模型配置")
                return None
                
        except Exception as e:
            print(f"TTS生成失败: {e}")
            return None
    
    def _has_python_api(self) -> bool:
        """检查是否有Python API"""
        try:
            # 这里需要根据你的GPT-SOVITs实现来检查
            # 例如检查特定的模块是否存在
            import importlib
            importlib.import_module("gpt_sovits")  # 替换为实际的模块名
            return True
        except ImportError:
            return False
    
    def _has_cli_interface(self) -> bool:
        """检查是否有命令行接口"""
        # 检查是否存在可执行文件
        possible_paths = [
            os.path.join(self.model_path, "infer.py"),
            os.path.join(self.model_path, "inference.py"),
            os.path.join(self.model_path, "gpt-sovits"),
            os.path.join(self.model_path, "tts.py")
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return True
        return False
    
    def _has_http_api(self) -> bool:
        """检查是否有HTTP API"""
        # 检查model_path是否是HTTP URL
        if self.model_path.startswith('http'):
            return True
            
        # 检查是否有配置文件指示HTTP服务
        config_files = [
            os.path.join(self.model_path, "config.json"),
            os.path.join(self.model_path, "server_config.json"),
            self.config_path
        ]
        
        for config_file in config_files:
            if os.path.exists(config_file):
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                        if 'http_server' in config or 'api_port' in config:
                            return True
                except:
                    continue
        return False
    
    def _call_python_api(self, text: str, output_path: str) -> Optional[str]:
        """调用Python API"""
        try:
            # 这里需要根据你的GPT-SOVITs Python API来调用
            # 以下是示例代码，需要根据实际情况修改
            
            # 示例1: 如果GPT-SOVITs提供了类似这样的API
            # from gpt_sovits import TTSModel
            # model = TTSModel(self.model_path)
            # audio = model.synthesize(text)
            # model.save_audio(audio, output_path)
            
            # 示例2: 如果使用torch或其他框架
            # import torch
            # model = torch.load(self.model_path)
            # audio = model.generate(text)
            # torchaudio.save(output_path, audio, Config.SAMPLE_RATE)
            
            print("请根据你的GPT-SOVITs Python API实现具体的调用逻辑")
            return None
            
        except Exception as e:
            print(f"Python API调用失败: {e}")
            return None
    
    def _call_cli_interface(self, text: str, output_path: str) -> Optional[str]:
        """调用命令行接口"""
        try:
            # 查找可执行文件
            possible_scripts = [
                os.path.join(self.model_path, "infer.py"),
                os.path.join(self.model_path, "inference.py"),
                os.path.join(self.model_path, "tts.py")
            ]
            
            script_path = None
            for script in possible_scripts:
                if os.path.exists(script):
                    script_path = script
                    break
            
            if not script_path:
                print("未找到TTS脚本文件")
                return None
            
            # 构建命令
            cmd = [
                "python", script_path,
                "--text", text,
                "--output", output_path,
                "--model_path", self.model_path
            ]
            
            # 执行命令
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0 and os.path.exists(output_path):
                return output_path
            else:
                print(f"CLI执行失败: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"CLI接口调用失败: {e}")
            return None
    
    def _call_http_api(self, text: str, output_path: str) -> Optional[str]:
        """调用HTTP API"""
        try:
            import requests
            
            # 检查model_path是否是HTTP URL
            if self.model_path.startswith('http'):
                # 直接使用model_path作为基础URL
                base_url = self.model_path.rstrip('/')
                
                # 尝试GPT-SOVITs的inference API
                api_url = f"{base_url}/api/inference"
                
                # 构建GPT-SOVITs所需的参数格式 - 简化版本
                inference_data = {
                    "data": [
                        text,                    # text
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
                
                print(f"调用GPT-SOVITs API: {api_url}")
                print(f"请求数据: {inference_data}")
                
                try:
                    response = requests.post(api_url, json=inference_data, timeout=120)
                    
                    print(f"响应状态码: {response.status_code}")
                    print(f"响应头: {dict(response.headers)}")
                    
                    if response.status_code == 200:
                        response_data = response.json()
                        print(f"响应数据: {response_data}")
                        
                        # 检查响应是否包含音频文件路径
                        if 'data' in response_data and len(response_data['data']) > 0:
                            audio_info = response_data['data'][0]
                            
                            if 'url' in audio_info:
                                # 下载音频文件
                                audio_url = audio_info['url']
                                print(f"下载音频文件: {audio_url}")
                                
                                audio_response = requests.get(audio_url, timeout=30)
                                if audio_response.status_code == 200:
                                    # 保存音频文件
                                    with open(output_path, 'wb') as f:
                                        f.write(audio_response.content)
                                    print(f"✅ 音频文件已保存: {output_path}")
                                    return output_path
                                else:
                                    print(f"❌ 下载音频文件失败: {audio_response.status_code}")
                                    return None
                            else:
                                print(f"❌ 响应中没有音频URL: {audio_info}")
                                return None
                        else:
                            print(f"❌ 响应格式不正确: {response_data}")
                            return None
                    else:
                        print(f"❌ API调用失败: {response.status_code}")
                        try:
                            error_data = response.json()
                            print(f"错误信息: {error_data}")
                        except:
                            print(f"错误信息: {response.text[:200]}")
                        return None
                            
                except requests.exceptions.RequestException as e:
                    print(f"❌ 网络连接问题 💡 请检查网络连接")
                    return None
                
                # 如果inference API失败，尝试其他端点
                possible_endpoints = [
                    "/tts",
                    "/synthesize", 
                    "/generate",
                    "/api/tts",
                    "/infer",
                    "/"
                ]
                
                for endpoint in possible_endpoints:
                    api_url = f"{base_url}{endpoint}"
                    try:
                        print(f"尝试API端点: {api_url}")
                        
                        # 发送POST请求
                        response = requests.post(
                            api_url,
                            json={"text": text},
                            timeout=30
                        )
                        
                        if response.status_code == 200:
                            # 保存音频文件
                            with open(output_path, 'wb') as f:
                                f.write(response.content)
                            print(f"✅ API调用成功: {api_url}")
                            return output_path
                        else:
                            print(f"❌ API调用失败: {response.status_code}")
                            
                    except requests.exceptions.RequestException as e:
                        print(f"❌ API请求失败: {e}")
                        continue
                
                print("所有HTTP API端点都失败了")
                return None
            else:
                # 原有的本地配置文件逻辑
                config_file = self.config_path if os.path.exists(self.config_path) else None
                
                if config_file:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                        api_url = config.get('api_url', 'http://localhost:8000/tts')
                else:
                    api_url = 'http://localhost:8000/tts'  # 默认地址
                
                # 发送请求
                response = requests.post(
                    api_url,
                    json={"text": text},
                    timeout=60
                )
                
                if response.status_code == 200:
                    # 保存音频文件
                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                    return output_path
                else:
                    print(f"HTTP API调用失败: {response.status_code}")
                    return None
                    
        except Exception as e:
            print(f"HTTP API调用失败: {e}")
            return None
    
    def get_audio_duration(self, audio_path: str) -> float:
        """获取音频文件时长"""
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_file(audio_path)
            return len(audio) / 1000.0  # 转换为秒
        except Exception as e:
            print(f"获取音频时长失败: {e}")
            return 0.0 