import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # DeepSeek API配置
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
    
    # TTS模型配置
    TTS_MODEL_PATH = os.getenv("TTS_MODEL_PATH", "./models/gpt-sovits")
    TTS_CONFIG_PATH = os.getenv("TTS_CONFIG_PATH", "./models/config.json")
    
    # 音频配置
    SAMPLE_RATE = 22050
    AUDIO_OUTPUT_PATH = "./output"
    
    # Web服务器配置
    HOST = "0.0.0.0"
    PORT = 8000
    
    # 对话配置
    MAX_HISTORY_LENGTH = 10
    
    # 系统prompt - 你可以在这里自定义AI助手的角色和行为
    SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "")
    
    # 百度语音识别API配置
    BAIDU_API_KEY = os.getenv("BAIDU_API_KEY", "")
    BAIDU_SECRET_KEY = os.getenv("BAIDU_SECRET_KEY", "")
    
    @classmethod
    def get_masked_api_key(cls) -> str:
        """获取隐藏的API key，只显示前4位和后4位"""
        if cls.DEEPSEEK_API_KEY and len(cls.DEEPSEEK_API_KEY) > 8:
            return cls.DEEPSEEK_API_KEY[:4] + "*" * (len(cls.DEEPSEEK_API_KEY) - 8) + cls.DEEPSEEK_API_KEY[-4:]
        elif cls.DEEPSEEK_API_KEY:
            return "*" * len(cls.DEEPSEEK_API_KEY)
        else:
            return "未设置" 