import os
import json
import time
from datetime import datetime
from typing import List, Dict, Optional, Any
from deepseek_client import DeepSeekClient
from tts_client import TTSClient
from config import Config

class ChatManager:
    def __init__(self):
        self.deepseek_client = DeepSeekClient()
        self.tts_client = TTSClient()
        self.conversation_history: List[Dict[str, str]] = []
        self.custom_prompt: Optional[str] = None
        self.context: Optional[str] = None
        
        # 聊天记录保存相关
        self.chat_history_dir = "./chat_history"
        os.makedirs(self.chat_history_dir, exist_ok=True)
        
        # 加载今天的聊天记录
        self.load_today_history()
    
    def get_today_filename(self) -> str:
        """获取今天的聊天记录文件名"""
        today = datetime.now().strftime("%Y-%m-%d")
        return f"chat_{today}.json"
    
    def load_today_history(self):
        """加载今天的聊天记录"""
        filename = self.get_today_filename()
        filepath = os.path.join(self.chat_history_dir, filename)
        
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.conversation_history = data.get('messages', [])
                    print(f"✅ 已加载今天的聊天记录: {len(self.conversation_history)} 条消息")
            except Exception as e:
                print(f"❌ 加载聊天记录失败: {e}")
                self.conversation_history = []
        else:
            print(f"📝 今天还没有聊天记录，创建新文件: {filename}")
    
    def save_today_history(self):
        """保存今天的聊天记录"""
        filename = self.get_today_filename()
        filepath = os.path.join(self.chat_history_dir, filename)
        
        try:
            data = {
                'date': datetime.now().strftime("%Y-%m-%d"),
                'messages': self.conversation_history
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"💾 已保存聊天记录: {filename}")
        except Exception as e:
            print(f"❌ 保存聊天记录失败: {e}")
    
    def get_history_files(self) -> List[Dict[str, Any]]:
        """获取所有历史记录文件"""
        history_files = []
        
        if os.path.exists(self.chat_history_dir):
            for filename in os.listdir(self.chat_history_dir):
                if filename.startswith("chat_") and filename.endswith(".json"):
                    filepath = os.path.join(self.chat_history_dir, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            history_files.append({
                                'filename': filename,
                                'date': data.get('date', ''),
                                'message_count': len(data.get('messages', [])),
                                'filepath': filepath
                            })
                    except Exception as e:
                        print(f"❌ 读取历史文件失败 {filename}: {e}")
        
        # 按日期倒序排列
        history_files.sort(key=lambda x: x['date'], reverse=True)
        return history_files
    
    def load_history_by_date(self, date: str) -> List[Dict[str, str]]:
        """根据日期加载历史记录"""
        filename = f"chat_{date}.json"
        filepath = os.path.join(self.chat_history_dir, filename)
        
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('messages', [])
            except Exception as e:
                print(f"❌ 加载历史记录失败: {e}")
        
        return []
    
    def delete_history_by_date(self, date: str) -> bool:
        """删除指定日期的历史记录"""
        filename = f"chat_{date}.json"
        filepath = os.path.join(self.chat_history_dir, filename)
        
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                print(f"🗑️ 已删除历史记录: {filename}")
                return True
            except Exception as e:
                print(f"❌ 删除历史记录失败: {e}")
                return False
        else:
            print(f"❌ 历史记录不存在: {filename}")
            return False
    
    def set_custom_prompt(self, prompt: str):
        """设置自定义prompt"""
        self.custom_prompt = prompt
        return {"success": True, "message": "自定义prompt已设置"}
    
    def set_context(self, context: str):
        """设置对话上下文"""
        self.context = context
        return {"success": True, "message": "上下文已设置"}
    
    def process_message(self, message: str, custom_prompt: Optional[str] = None, context: Optional[str] = None) -> Dict[str, Any]:
        """处理用户消息"""
        try:
            # 使用传入的prompt和context，如果没有则使用存储的值
            used_prompt = custom_prompt if custom_prompt is not None else self.custom_prompt
            used_context = context if context is not None else self.context
            
            # 调用DeepSeek API
            if used_context:
                response = self.deepseek_client.chat_with_context(message, self.conversation_history, used_context)
            else:
                response = self.deepseek_client.chat(message, self.conversation_history, used_prompt)
            
            # 添加到对话历史
            self.conversation_history.append({"role": "user", "content": message})
            self.conversation_history.append({"role": "assistant", "content": response})
            
            # 生成音频
            audio_path = None
            if self.tts_client:
                audio_filename = f"response_{int(time.time())}.wav"
                audio_path = self.tts_client.text_to_speech(response, audio_filename)
                # 只返回文件名，不包含路径
                if audio_path:
                    audio_path = os.path.basename(audio_path)
            
            # 自动保存聊天记录
            self.save_today_history()
            
            return {
                "success": True,
                "text_response": response,
                "audio_path": audio_path,
                "used_prompt": used_prompt,
                "used_context": used_context
            }
            
        except Exception as e:
            print(f"处理消息时出错: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def clear_history(self) -> Dict[str, Any]:
        """清空对话历史"""
        try:
            self.conversation_history = []
            # 保存空的聊天记录
            self.save_today_history()
            return {"success": True, "message": "对话历史已清空"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_history(self) -> List[Dict[str, str]]:
        """获取对话历史"""
        return self.conversation_history.copy()
    
    def get_current_settings(self) -> Dict[str, any]:
        """获取当前设置"""
        return {
            "custom_prompt": self.custom_prompt,
            "context": self.context,
            "history_length": len(self.conversation_history)
        }
    
    def test_services(self) -> Dict[str, bool]:
        """测试所有服务是否正常"""
        results = {
            "deepseek_api": self.deepseek_client.test_connection(),
            "tts_model": self._test_tts_model()
        }
        return results
    
    def _test_tts_model(self) -> bool:
        """测试TTS模型"""
        try:
            # 尝试生成一个简单的测试音频
            test_text = "测试"
            test_filename = "test_tts.wav"
            result = self.tts_client.text_to_speech(test_text, test_filename)
            return result is not None
        except Exception as e:
            print(f"TTS模型测试失败: {e}")
            return False
    
    def get_status(self) -> Dict[str, any]:
        """获取系统状态"""
        return {
            "deepseek_api_key_configured": bool(Config.DEEPSEEK_API_KEY),
            "tts_model_path": Config.TTS_MODEL_PATH,
            "conversation_history_length": len(self.conversation_history),
            "services_status": self.test_services(),
            "custom_prompt_set": bool(self.custom_prompt),
            "context_set": bool(self.context)
        } 