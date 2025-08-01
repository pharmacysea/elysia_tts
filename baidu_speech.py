import requests
import json
import os
import base64
from typing import Optional
from config import Config

class BaiduSpeechRecognition:
    def __init__(self):
        self.api_key = Config.BAIDU_API_KEY
        self.secret_key = Config.BAIDU_SECRET_KEY
        self.access_token = None
        
    def get_access_token(self) -> Optional[str]:
        """获取百度API访问令牌"""
        try:
            url = "https://aip.baidubce.com/oauth/2.0/token"
            params = {
                "grant_type": "client_credentials",
                "client_id": self.api_key,
                "client_secret": self.secret_key
            }
            
            response = requests.post(url, params=params)
            result = response.json()
            
            if "access_token" in result:
                self.access_token = result["access_token"]
                print(f"✅ 百度API访问令牌获取成功")
                return self.access_token
            else:
                print(f"❌ 百度API访问令牌获取失败: {result}")
                return None
                
        except Exception as e:
            print(f"❌ 获取百度API访问令牌时出错: {e}")
            return None
    
    def convert_webm_to_pcm(self, webm_file_path: str) -> Optional[str]:
        """将WebM音频转换为PCM格式"""
        try:
            import subprocess
            
            # 生成PCM文件路径
            pcm_file_path = webm_file_path.replace('.webm', '.pcm')
            
            # 使用ffmpeg转换音频格式
            cmd = [
                'ffmpeg', '-i', webm_file_path,
                '-f', 's16le',  # 16位小端序
                '-ac', '1',     # 单声道
                '-ar', '16000', # 16kHz采样率
                '-y',           # 覆盖输出文件
                pcm_file_path
            ]
            
            print(f"🔄 正在转换音频格式: {webm_file_path} → {pcm_file_path}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ 音频格式转换成功: {pcm_file_path}")
                return pcm_file_path
            else:
                print(f"❌ 音频格式转换失败: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ 音频格式转换时出错: {e}")
            return None
    
    def speech_to_text(self, audio_file_path: str) -> Optional[str]:
        """调用百度语音识别API"""
        try:
            # 获取访问令牌
            if not self.access_token:
                self.access_token = self.get_access_token()
                if not self.access_token:
                    return None
            
            # 转换音频格式
            pcm_file_path = self.convert_webm_to_pcm(audio_file_path)
            if not pcm_file_path:
                return None
            
            # 读取PCM文件
            with open(pcm_file_path, 'rb') as f:
                audio_data = f.read()
            
            # 转换为base64
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            
            # 调用百度API
            url = "https://vop.baidu.com/server_api"
            
            payload = {
                "format": "pcm",
                "rate": 16000,
                "channel": 1,
                "cuid": "elysia_chat_system",
                "token": self.access_token,
                "speech": audio_base64,
                "len": len(audio_data)
            }
            
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            print(f"📤 正在调用百度语音识别API...")
            response = requests.post(url, headers=headers, json=payload)
            result = response.json()
            
            print(f"📥 百度API响应: {result}")
            
            # 清理临时文件
            if os.path.exists(pcm_file_path):
                os.remove(pcm_file_path)
            
            if "result" in result and result["result"]:
                recognized_text = result["result"][0]
                print(f"✅ 语音识别成功: {recognized_text}")
                return recognized_text
            else:
                error_msg = result.get("err_msg", "未知错误")
                print(f"❌ 语音识别失败: {error_msg}")
                return None
                
        except Exception as e:
            print(f"❌ 语音识别过程中出错: {e}")
            return None 

    async def recognize_audio(self, audio_file_path: str) -> Optional[str]:
        """异步调用语音识别"""
        try:
            # 获取访问令牌
            if not self.access_token:
                self.access_token = self.get_access_token()
                if not self.access_token:
                    return None
            
            # 转换音频格式
            pcm_file_path = self.convert_webm_to_pcm(audio_file_path)
            if not pcm_file_path:
                return None
            
            # 读取PCM文件
            with open(pcm_file_path, 'rb') as f:
                audio_data = f.read()
            
            # 转换为base64
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            
            # 调用百度API
            url = "https://vop.baidu.com/server_api"
            
            payload = {
                "format": "pcm",
                "rate": 16000,
                "channel": 1,
                "cuid": "elysia_chat_system",
                "token": self.access_token,
                "speech": audio_base64,
                "len": len(audio_data)
            }
            
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            print(f"📤 正在调用百度语音识别API...")
            response = requests.post(url, headers=headers, json=payload)
            result = response.json()
            
            print(f"📥 百度API响应: {result}")
            
            # 清理临时文件
            if os.path.exists(pcm_file_path):
                os.remove(pcm_file_path)
            
            if "result" in result and result["result"]:
                recognized_text = result["result"][0]
                print(f"✅ 语音识别成功: {recognized_text}")
                return recognized_text
            else:
                error_msg = result.get("err_msg", "未知错误")
                print(f"❌ 语音识别失败: {error_msg}")
                return None
                
        except Exception as e:
            print(f"❌ 语音识别过程中出错: {e}")
            return None 