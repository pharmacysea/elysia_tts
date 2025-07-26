# 爱莉希雅的化妆间 🌸

一个基于DeepSeek API和GPT-SOVITs的AI对话系统，支持文本对话和语音合成。

## ✨ 功能特性

- 🤖 **智能对话**：基于DeepSeek API的自然语言对话
- 🎤 **语音合成**：集成GPT-SOVITs进行语音生成
- 💬 **实时聊天**：Web界面支持实时对话
- 📚 **历史记录**：自动保存和查看聊天历史
- 🎨 **美观界面**：现代化的Web界面设计
- 🔧 **命令行模式**：支持CLI交互

## 🚀 快速开始

### 环境要求

- Python 3.8+
- GPT-SOVITs模型（本地或HTTP服务）
- DeepSeek API密钥

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/your-username/elysia-chat.git
cd elysia-chat
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，填入你的配置
```

4. **启动GPT-SOVITs服务**
```bash
# 启动你的GPT-SOVITs HTTP服务
# 默认端口：9872
```

5. **运行应用**
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
# DeepSeek API密钥
DEEPSEEK_API_KEY=your_api_key_here

# TTS模型配置（HTTP服务推荐）
TTS_MODEL_PATH=http://localhost:9872
TTS_CONFIG_PATH=http://localhost:9872

# 音频输出路径
AUDIO_OUTPUT_PATH=./output

# 服务器配置
HOST=0.0.0.0
PORT=8000
```

### GPT-SOVITs集成

支持两种集成方式：

1. **HTTP服务**（推荐）：
   - 启动GPT-SOVITs的Gradio界面
   - 设置 `TTS_MODEL_PATH=http://localhost:9872`

2. **本地文件**：
   - 设置模型文件路径
   - 配置相应的调用方式

## 📁 项目结构

```
elysia-chat/
├── main.py              # 主应用文件
├── config.py            # 配置管理
├── deepseek_client.py   # DeepSeek API客户端
├── tts_client.py        # TTS客户端
├── chat_manager.py      # 对话管理器
├── requirements.txt     # Python依赖
├── .env.example        # 环境变量模板
├── .gitignore          # Git忽略文件
├── README.md           # 项目说明
├── output/             # 音频输出目录
└── chat_history/       # 聊天历史记录
```

## 🎯 使用指南

### Web界面

1. 启动服务：`python main.py`
2. 访问：`http://localhost:8000`
3. 开始对话！

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
- `GET /status`：获取系统状态
- `POST /clear-history`：清空历史
- `GET /history`：获取历史记录
- `GET /audio/{filename}`：获取音频文件

## 🔧 故障排除

### 常见问题

1. **TTS API连接失败**
   - 检查GPT-SOVITs服务是否启动
   - 确认端口配置正确

2. **DeepSeek API错误**
   - 验证API密钥是否正确
   - 检查网络连接

3. **音频播放问题**
   - 确认浏览器支持音频格式
   - 检查音频文件路径

### 调试模式

运行测试脚本检查系统状态：
```bash
python test_system.py
```

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- [DeepSeek](https://platform.deepseek.com/) - 提供强大的AI API
- [GPT-SOVITs](https://github.com/RVC-Boss/GPT-SoVITS) - 优秀的语音合成项目
- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的Web框架

## 📞 联系方式

如有问题或建议，请提交 Issue 或 Pull Request。

---

**注意**：本项目仅供学习和个人使用，请遵守相关API的使用条款。 