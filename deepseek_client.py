import requests
import json
from typing import List, Dict, Any, Optional
from config import Config

class DeepSeekClient:
    def __init__(self):
        self.api_key = Config.DEEPSEEK_API_KEY
        self.api_url = Config.DEEPSEEK_API_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _mask_api_key(self, text: str) -> str:
        """隐藏API key，只显示前4位和后4位"""
        if self.api_key and len(self.api_key) > 8:
            masked_key = self.api_key[:4] + "*" * (len(self.api_key) - 8) + self.api_key[-4:]
            return text.replace(self.api_key, masked_key)
        return text
    
    def chat(self, message: str, history: List[Dict[str, str]] = None, 
             custom_prompt: Optional[str] = None, 
             temperature: float = 0.7,
             max_tokens: int = 1000) -> str:
        """
        发送消息到DeepSeek API并获取回复
        
        Args:
            message: 用户输入的消息
            history: 对话历史记录
            custom_prompt: 自定义系统prompt，如果为None则使用默认的
            temperature: 控制回复的随机性 (0.0-1.0)
            max_tokens: 最大回复长度
            
        Returns:
            str: AI的回复文本
        """
        if history is None:
            history = []
        
        # 使用自定义prompt或默认prompt
        system_prompt = custom_prompt if custom_prompt else Config.SYSTEM_PROMPT
        
        # 构建消息列表
        messages = [{"role": "system", "content": system_prompt}]
        
        # 添加历史对话
        for msg in history[-Config.MAX_HISTORY_LENGTH:]:
            messages.append(msg)
        
        # 添加当前用户消息
        messages.append({"role": "user", "content": message})
        
        # 构建请求数据
        data = {
            "model": "deepseek-chat",
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": False
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            ai_message = result["choices"][0]["message"]["content"]
            return ai_message.strip()
            
        except requests.exceptions.RequestException as e:
            error_msg = self._mask_api_key(str(e))
            print(f"API请求错误: {error_msg}")
            return "抱歉，我现在无法回答，请稍后再试。"
        except KeyError as e:
            print(f"API响应格式错误: {e}")
            return "抱歉，响应格式有误，请稍后再试。"
        except Exception as e:
            error_msg = self._mask_api_key(str(e))
            print(f"未知错误: {error_msg}")
            return "抱歉，发生了未知错误，请稍后再试。"
    
    def chat_with_context(self, message: str, context: str = "", 
                         history: List[Dict[str, str]] = None) -> str:
        """
        带上下文的对话，可以在prompt中加入特定上下文
        
        Args:
            message: 用户输入的消息
            context: 额外的上下文信息
            history: 对话历史记录
            
        Returns:
            str: AI的回复文本
        """
        # 构建包含上下文的prompt
        enhanced_prompt = Config.SYSTEM_PROMPT
        if context:
            enhanced_prompt += f"\n\n当前上下文：{context}\n请根据以上上下文回答用户的问题。"
        
        return self.chat(message, history, enhanced_prompt)
    
    def test_connection(self) -> bool:
        """测试API连接"""
        try:
            response = requests.get(
                "https://api.deepseek.com/v1/models",
                headers=self.headers,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            error_msg = self._mask_api_key(str(e))
            print(f"API连接测试失败: {error_msg}")
            return False 