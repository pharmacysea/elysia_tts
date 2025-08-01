# 爱莉希雅的化妆间 🌸

一个基于DeepSeek API和GPT-SOVITs的智能语音对话系统，支持实时语音识别、自然语言对话和语音合成。（至于为什么选dpsk而不是OpenAI，当然是因为我懒，以及dpsk可以dan）

## ✨ 功能特性

- 🤖 **智能对话**：基于DeepSeek API的自然语言处理
- 🎤 **语音识别**：集成百度语音识别API，支持实时语音转文字
- 🎵 **语音合成**：集成GPT-SOVITs进行高质量语音生成
- 💬 **实时交互**：Web界面支持实时语音和文本对话
- 📚 **历史管理**：自动保存和查看聊天历史记录
- 🎨 **美观界面**：现代化的响应式Web界面设计
- 🔧 **命令行模式**：支持CLI交互
- 🔐 **安全配置**：环境变量管理敏感信息

## 🚀 快速开始

### 环境要求

- **Python** 3.8+
- **ffmpeg** (用于音频格式转换)
- **GPT-SOVITs模型** (本地或HTTP服务)
- **DeepSeek API密钥**
- **百度语音识别API密钥**

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/pharmacysea/elysia_tts.git
cd elysia_tts
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **安装ffmpeg** (音频处理必需)
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# Windows
# 下载并安装ffmpeg，添加到PATH
```

4. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的API密钥和配置
```

5. **启动GPT-SOVITs服务**（这个是必须的，详情可以参考https://github.com/RVC-Boss/GPT-SoVITS/blob/main/docs/cn/README.md，一定要有这个才行，我这个毕竟只是个本地项目）
```bash
# 启动你的GPT-SOVITs HTTP服务
# 默认端口：9872
```

6. **运行应用**
```bash
# Web界面模式
python main.py

# 命令行模式
python main.py --cli
```

## ⚙️ 配置说明

### 环境变量配置

复制 `.env.example` 为 `.env` 并配置：

```bash
# DeepSeek API配置
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# 百度语音识别API配置
BAIDU_API_KEY=your_baidu_api_key_here
BAIDU_SECRET_KEY=your_baidu_secret_key_here

# TTS模型配置
TTS_MODEL_PATH=http://localhost:9872
TTS_CONFIG_PATH=http://localhost:9872

# 音频输出配置
AUDIO_OUTPUT_PATH=./output

# 服务器配置
HOST=0.0.0.0
PORT=8000

# 系统提示词配置（可选）
SYSTEM_PROMPT=your_custom_system_prompt
```

### API密钥获取

1. **DeepSeek API**：
   - 访问 [DeepSeek Platform](https://platform.deepseek.com/)
   - 注册账号并获取API密钥

2. **百度语音识别API**：
   - 访问 [百度智能云](https://console.bce.baidu.com/ai/#/ai/speech/overview/index)
   - 创建应用并获取API密钥和Secret Key

### GPT-SOVITs集成

支持两种集成方式：

1. **HTTP服务**（推荐）：
   - 启动GPT-SOVITs的Gradio界面
   - 设置 `TTS_MODEL_PATH=http://localhost:9872`（9872端口就是GPT-SOVITs的推理端口）

2. **本地文件**：
   - 设置模型文件路径
   - 配置相应的调用方式

## 📁 项目结构
（很混乱，纯vibe coding）
```
elysia_tts/
├── main.py                 # FastAPI主应用
├── config.py              # 配置管理
├── deepseek_client.py     # DeepSeek API客户端
├── tts_client.py          # TTS客户端
├── chat_manager.py        # 对话管理器
├── baidu_speech.py        # 百度语音识别模块
├── requirements.txt       # Python依赖
├── .env.example          # 环境变量模板
├── .gitignore            # Git忽略文件
├── README.md             # 项目说明
├── output/               # 音频输出目录
└── chat_history/         # 聊天历史记录
```

## 🎯 使用指南

### Web界面

1. 启动服务：`python main.py`
2. 访问：`http://localhost:8000`
3. 开始对话！

**功能说明**：
- **文本输入**：直接在输入框中输入文字
- **语音输入**：点击🎤按钮进行语音识别
- **音频播放**：AI回复后自动播放语音，可重复播放
- **历史记录**：自动保存聊天历史，支持查看和删除（是能删除，但是只能删除全部，还没做删除某一条消息）

### 命令行模式

```bash
python main.py --cli
```

支持的命令：
- `quit` / `exit`：退出
- `clear`：清空历史
- `status`：查看状态

### API端点

- `POST /chat`：发送消息
- `POST /speech-to-text`：语音转文字
- `GET /status`：获取系统状态
- `POST /clear-history`：清空历史
- `GET /history`：获取历史记录
- `GET /audio/{filename}`：获取音频文件

## 🔧 故障排除

### 常见问题

1. **ffmpeg未安装**
   ```
   错误：音频格式转换失败
   解决：安装ffmpeg并确保在PATH中
   ```

2. **API密钥错误**
   ```
   错误：语音识别失败
   解决：检查.env文件中的API密钥配置
   ```

3. **TTS服务连接失败**
   ```
   错误：TTS模型异常
   解决：确保GPT-SOVITs服务正在运行
   ```

4. **麦克风权限问题**
   ```
   错误：请允许麦克风权限
   解决：在浏览器中允许麦克风访问
   ```

### 调试模式

运行测试脚本检查系统状态：
```bash
python test_system.py
```

## 🛠️ 开发指南

### 本地开发

1. **克隆项目**
```bash
git clone https://github.com/pharmacysea/elysia_tts.git
cd elysia_tts
```

2. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境**
```bash
cp .env.example .env
# 编辑 .env 文件
```

### 代码结构

- **FastAPI应用**：`main.py` - Web服务器和API端点
- **语音识别**：`baidu_speech.py` - 百度语音识别集成
- **对话管理**：`chat_manager.py` - 对话历史和状态管理
- **TTS集成**：`tts_client.py` - GPT-SOVITs语音合成
- **配置管理**：`config.py` - 环境变量和配置

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [DeepSeek](https://platform.deepseek.com/) - 提供强大的AI API
- [GPT-SOVITs](https://github.com/RVC-Boss/GPT-SoVITS) - 优秀的语音合成项目
- [百度智能云](https://cloud.baidu.com/) - 语音识别服务
- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的Web框架

## 📞 联系方式

- **项目地址**：https://github.com/pharmacysea/elysia_tts
- **问题反馈**：请提交 [Issue](https://github.com/pharmacysea/elysia_tts/issues)
- **功能建议**：欢迎提交 Pull Request

---

**注意**：本项目仅供学习和个人使用，请遵守相关API的使用条款和法律法规。 