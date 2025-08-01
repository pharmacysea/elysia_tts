import asyncio
import uvicorn
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from typing import Dict, Any
from chat_manager import ChatManager
from config import Config
import time
from baidu_speech import BaiduSpeechRecognition

# 创建FastAPI应用
app = FastAPI(title="爱莉希雅的闺房", description="与爱莉希雅一起度过美好时光的AI对话系统")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建聊天管理器实例
chat_manager = ChatManager()

# 挂载静态文件目录
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    """返回主页HTML"""
    html_content = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
        <meta http-equiv="Pragma" content="no-cache">
        <meta http-equiv="Expires" content="0">
        <title>爱莉希雅的化妆间</title>
        <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Noto Sans SC', sans-serif;
                background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 25%, #fecfef 75%, #ff9a9e 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            
            .container {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 25px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(255, 154, 158, 0.3);
                backdrop-filter: blur(10px);
                max-width: 900px;
                width: 100%;
                position: relative;
                overflow: hidden;
            }
            
            .container::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 5px;
                background: linear-gradient(90deg, #ff9a9e, #fecfef, #ff9a9e);
                border-radius: 25px 25px 0 0;
            }
            
            .header {
                text-align: center;
                margin-bottom: 30px;
                position: relative;
            }
            
            .title {
                font-size: 2.5em;
                font-weight: 700;
                background: linear-gradient(45deg, #ff6b9d, #c44569);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 10px;
                text-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .subtitle {
                color: #666;
                font-size: 1.1em;
                font-weight: 300;
                margin-bottom: 20px;
            }
            
            .chat-container {
                height: 450px;
                border: 2px solid #ffe0e6;
                border-radius: 20px;
                padding: 20px;
                overflow-y: auto;
                margin-bottom: 25px;
                background: linear-gradient(135deg, #fff5f7 0%, #fff 100%);
                box-shadow: inset 0 2px 10px rgba(255, 154, 158, 0.1);
                scrollbar-width: thin;
                scrollbar-color: #ff9a9e #fff5f7;
            }
            
            .chat-container::-webkit-scrollbar {
                width: 8px;
            }
            
            .chat-container::-webkit-scrollbar-track {
                background: #fff5f7;
                border-radius: 4px;
            }
            
            .chat-container::-webkit-scrollbar-thumb {
                background: #ff9a9e;
                border-radius: 4px;
            }
            
            .message {
                margin-bottom: 20px;
                padding: 15px 20px;
                border-radius: 20px;
                max-width: 85%;
                min-width: 60px;
                width: fit-content;
                position: relative;
                animation: fadeInUp 0.5s ease-out;
                word-wrap: break-word;
                white-space: pre-wrap;
                display: inline-block;
            }
            
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .user-message {
                background: linear-gradient(135deg, #ff6b9d, #c44569);
                color: white;
                margin-left: auto;
                margin-right: 0;
                text-align: right;
                box-shadow: 0 4px 15px rgba(255, 107, 157, 0.3);
                float: right;
                clear: both;
            }
            
            .ai-message {
                background: linear-gradient(135deg, #fff, #f8f9ff);
                color: #333;
                border: 1px solid #ffe0e6;
                box-shadow: 0 4px 15px rgba(0,0,0,0.05);
                margin-right: auto;
                margin-left: 0;
                text-align: left;
                float: left;
                clear: both;
            }
            
            .ai-message::before {
                content: '🌸';
                position: absolute;
                left: -10px;
                top: 50%;
                transform: translateY(-50%);
                font-size: 1.2em;
            }
            
            .input-container {
                display: flex;
                gap: 15px;
                margin-bottom: 25px;
                align-items: flex-start;
            }
            
            .button-group {
                display: flex;
                flex-direction: column;
                gap: 10px;
            }
            
            input[type="text"] {
                flex: 1;
                padding: 18px 25px;
                border: 2px solid #ffe0e6;
                border-radius: 25px;
                font-size: 16px;
                background: white;
                transition: all 0.3s ease;
                box-shadow: 0 2px 10px rgba(255, 154, 158, 0.1);
            }
            
            input[type="text"]:focus {
                outline: none;
                border-color: #ff6b9d;
                box-shadow: 0 0 0 3px rgba(255, 107, 157, 0.1);
                transform: translateY(-2px);
            }
            
            textarea {
                flex: 1;
                padding: 18px 25px;
                border: 2px solid #ffe0e6;
                border-radius: 25px;
                font-size: 16px;
                background: white;
                transition: all 0.3s ease;
                box-shadow: 0 2px 10px rgba(255, 154, 158, 0.1);
                resize: vertical;
                min-height: 60px;
                max-height: 120px;
                font-family: 'Noto Sans SC', sans-serif;
                line-height: 1.5;
                overflow-y: auto;
            }
            
            textarea:focus {
                outline: none;
                border-color: #ff6b9d;
                box-shadow: 0 0 0 3px rgba(255, 107, 157, 0.1);
                transform: translateY(-2px);
            }
            
            textarea::-webkit-scrollbar {
                width: 6px;
            }
            
            textarea::-webkit-scrollbar-track {
                background: #fff5f7;
                border-radius: 3px;
            }
            
            textarea::-webkit-scrollbar-thumb {
                background: #ff9a9e;
                border-radius: 3px;
            }
            
            .send-btn {
                padding: 18px 30px;
                background: linear-gradient(135deg, #ff6b9d, #c44569);
                color: white;
                border: none;
                border-radius: 25px;
                cursor: pointer;
                font-size: 16px;
                font-weight: 500;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(255, 107, 157, 0.3);
                display: flex;
                align-items: center;
                gap: 8px;
            }
            
            .send-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(255, 107, 157, 0.4);
            }
            
            .send-btn:active {
                transform: translateY(0);
            }
            
            .voice-btn {
                padding: 18px 20px;
                background: linear-gradient(135deg, #4ecdc4, #44a08d);
                color: white;
                border: none;
                border-radius: 25px;
                cursor: pointer;
                font-size: 16px;
                font-weight: 500;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(78, 205, 196, 0.3);
                display: flex;
                align-items: center;
                gap: 8px;
            }
            
            .voice-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(78, 205, 196, 0.4);
            }
            
            .voice-btn:active {
                transform: translateY(0);
            }
            
            .voice-btn.recording {
                background: linear-gradient(135deg, #ff6b6b, #ee5a52);
                animation: pulse 1.5s infinite;
            }
            
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); }
            }
            
            .voice-status {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: rgba(0, 0, 0, 0.8);
                color: white;
                padding: 20px 30px;
                border-radius: 15px;
                font-size: 18px;
                display: none;
                z-index: 1000;
                backdrop-filter: blur(10px);
            }
            
            .controls {
                display: flex;
                gap: 15px;
                justify-content: center;
                flex-wrap: wrap;
            }
            
            .control-btn {
                padding: 12px 24px;
                background: linear-gradient(135deg, #f8f9ff, #fff);
                color: #666;
                border: 2px solid #ffe0e6;
                border-radius: 20px;
                cursor: pointer;
                font-size: 14px;
                font-weight: 500;
                transition: all 0.3s ease;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            }
            
            .control-btn:hover {
                background: linear-gradient(135deg, #ff6b9d, #c44569);
                color: white;
                border-color: #ff6b9d;
                transform: translateY(-2px);
                box-shadow: 0 4px 15px rgba(255, 107, 157, 0.3);
            }
            
            .status {
                text-align: center;
                margin-top: 25px;
                padding: 15px;
                background: linear-gradient(135deg, #fff5f7, #fff);
                border-radius: 15px;
                border: 1px solid #ffe0e6;
                color: #666;
                font-size: 14px;
            }
            
            .audio-controls {
                margin-top: 10px;
                text-align: center;
            }
            
            .audio-btn {
                background: linear-gradient(135deg, #ff6b9d, #c44569);
                color: white;
                border: none;
                border-radius: 15px;
                padding: 8px 16px;
                margin: 5px;
                cursor: pointer;
                font-size: 12px;
                transition: all 0.3s ease;
                box-shadow: 0 2px 10px rgba(255, 107, 157, 0.2);
            }
            
            .audio-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 15px rgba(255, 107, 157, 0.3);
            }
            
            .audio-btn:active {
                transform: translateY(0);
            }
            
            .loading {
                display: none;
                text-align: center;
                color: #ff6b9d;
                font-style: italic;
                margin: 10px 0;
            }
            
            .typing-indicator {
                padding: 15px 20px;
                background: linear-gradient(135deg, #fff, #f8f9ff);
                border-radius: 20px;
                color: #666;
                font-style: italic;
                margin-bottom: 20px;
                border: 1px solid #ffe0e6;
                max-width: 85%;
                min-width: 60px;
                width: fit-content;
                position: relative;
                margin-right: auto;
                margin-left: 0;
                text-align: left;
                word-wrap: break-word;
                white-space: pre-wrap;
                display: inline-block;
                float: left;
                clear: both;
            }
            
            .typing-indicator::before {
                content: '🌸';
                position: absolute;
                left: -10px;
                top: 50%;
                transform: translateY(-50%);
                font-size: 1.2em;
            }
            
            .typing-dots {
                display: inline-block;
                animation: typing 1.4s infinite;
            }
            
            @keyframes typing {
                0%, 20% { content: "爱莉正在输入中"; }
                40% { content: "爱莉正在输入中."; }
                60% { content: "爱莉正在输入中.."; }
                80%, 100% { content: "爱莉正在输入中..."; }
            }
            
            .welcome-message {
                text-align: center;
                color: #666;
                font-style: italic;
                margin-bottom: 20px;
                padding: 20px;
                background: linear-gradient(135deg, #fff5f7, #fff);
                border-radius: 15px;
                border: 1px solid #ffe0e6;
            }
            
            .history-modal {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.5);
                z-index: 1000;
                backdrop-filter: blur(5px);
            }
            
            .history-content {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: white;
                border-radius: 20px;
                padding: 30px;
                max-width: 600px;
                width: 90%;
                max-height: 80vh;
                overflow-y: auto;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            }
            
            .history-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
                padding-bottom: 15px;
                border-bottom: 2px solid #ffe0e6;
            }
            
            .history-title {
                font-size: 1.5em;
                font-weight: 600;
                color: #ff6b9d;
            }
            
            .close-btn {
                background: none;
                border: none;
                font-size: 1.5em;
                cursor: pointer;
                color: #666;
                padding: 5px;
                border-radius: 50%;
                transition: all 0.3s ease;
            }
            
            .close-btn:hover {
                background: #ffe0e6;
                color: #ff6b9d;
            }
            
            .history-item {
                padding: 15px;
                margin: 10px 0;
                border: 1px solid #ffe0e6;
                border-radius: 15px;
                background: linear-gradient(135deg, #fff5f7, #fff);
                cursor: pointer;
                transition: all 0.3s ease;
            }
            
            .history-item:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(255, 107, 157, 0.2);
                border-color: #ff6b9d;
            }
            
            .history-date {
                font-weight: 600;
                color: #ff6b9d;
                margin-bottom: 5px;
            }
            
            .history-count {
                color: #666;
                font-size: 0.9em;
            }
            
            .history-actions {
                display: flex;
                gap: 10px;
                margin-top: 10px;
            }
            
            .history-btn {
                padding: 5px 10px;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                font-size: 0.8em;
                transition: all 0.3s ease;
            }
            
            .view-btn {
                background: linear-gradient(135deg, #4ecdc4, #44a08d);
                color: white;
            }
            
            .delete-btn {
                background: linear-gradient(135deg, #ff6b6b, #ee5a52);
                color: white;
            }
            
            .history-btn:hover {
                transform: translateY(-1px);
                box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
            }
            
            @media (max-width: 768px) {
                .container {
                    padding: 20px;
                    margin: 10px;
                }
                
                .title {
                    font-size: 2em;
                }
                
                .chat-container {
                    height: 350px;
                }
                
                .controls {
                    flex-direction: column;
                }
            }
            .inline-audio-btn {
                background: linear-gradient(135deg, #ff6b9d, #c44569);
                color: white;
                border: none;
                border-radius: 50%;
                width: 24px;
                height: 24px;
                margin-left: 8px;
                cursor: pointer;
                font-size: 12px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                transition: all 0.3s ease;
                box-shadow: 0 2px 8px rgba(255, 107, 157, 0.3);
                vertical-align: middle;
            }
            
            .inline-audio-btn:hover {
                transform: scale(1.1);
                box-shadow: 0 4px 12px rgba(255, 107, 157, 0.4);
            }
            
            .inline-audio-btn:active {
                transform: scale(0.95);
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1 class="title">🌸 爱莉希雅的化妆间🌸</h1>
                <p class="subtitle">与爱莉希雅一起度过美好时光</p>
            </div>
            
            <div class="welcome-message">
                💕 亲爱的，欢迎来到我的秘密基地～有什么想和我聊的吗？
            </div>
            
            <div class="chat-container" id="chatContainer">
                <!-- 思考指示器将在JavaScript中动态添加和移除 -->
            </div>
            
            <div class="input-container">
                <textarea id="messageInput" placeholder="和爱莉希雅说说话吧..." onkeypress="handleKeyPress(event)"></textarea>
                <div class="button-group">
                    <button class="voice-btn" onclick="toggleVoiceInput()" id="voiceBtn" title="语音输入（可选功能）">
                        🎤 语音
                    </button>
                    <button class="send-btn" onclick="sendMessage()">
                        💕 发送
                    </button>
                </div>
            </div>
            
            <div class="controls">
                <button class="control-btn" onclick="clearHistory()">🗑️ 清空历史</button>
                <button class="control-btn" onclick="showHistory()">📚 历史记录</button>
                <button class="control-btn" onclick="checkStatus()">🔍 检查状态</button>
                <button class="control-btn" onclick="toggleAudio()">🔊 音频开关</button>
            </div>
            
            <div class="loading" id="loading">正在等待爱莉希雅的回复...</div>
            
            <div class="voice-status" id="voiceStatus">
                🎤 正在听你说话...
            </div>
            
            <div class="status" id="status"></div>
        </div>

        <!-- 历史记录弹窗 -->
        <div class="history-modal" id="historyModal">
            <div class="history-content">
                <div class="history-header">
                    <h2 class="history-title">📚 聊天历史记录</h2>
                    <button class="close-btn" onclick="closeHistory()">&times;</button>
                </div>
                <div id="historyList">
                    <!-- 历史记录列表将在这里动态生成 -->
                </div>
            </div>
        </div>

        <script>
            // 版本号：v1.1 - 强制刷新缓存
            console.log('🎯 JavaScript已加载 - 版本 v1.1');
            
            let currentAudio = null;
            let audioEnabled = true;
            let recognition = null;
            let isRecording = false;
            let mediaRecorder = null;
            let audioChunks = [];
            
            console.log('🎯 变量初始化完成 - isRecording:', isRecording);

            function handleKeyPress(event) {
                if (event.key === 'Enter' && !event.ctrlKey) {
                    event.preventDefault();
                    sendMessage();
                }
            }

            function showTypingIndicator() {
                console.log('🎯 显示思考指示器');
                const container = document.getElementById('chatContainer');
                const typingDiv = document.createElement('div');
                typingDiv.className = 'typing-indicator';
                typingDiv.id = 'typingIndicator';
                typingDiv.innerHTML = '<span class="typing-dots">爱莉正在输入中...</span>';
                container.appendChild(typingDiv);
                container.scrollTop = container.scrollHeight;
                console.log('✅ 思考指示器已添加');
            }

            function hideTypingIndicator() {
                const typingIndicator = document.getElementById('typingIndicator');
                if (typingIndicator) {
                    typingIndicator.remove();
                }
            }

            function addMessageWithAudio(text, audioPath) {
                const container = document.getElementById('chatContainer');
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message ai-message';
                
                // 创建文字内容
                const textSpan = document.createElement('span');
                textSpan.textContent = text;
                messageDiv.appendChild(textSpan);
                
                // 添加音频播放按钮（内嵌在文字后面）
                if (audioPath && audioEnabled) {
                    const playButton = document.createElement('button');
                    playButton.className = 'inline-audio-btn';
                    playButton.innerHTML = '🔊';
                    playButton.title = '播放音频';
                    
                    // 创建音频对象并存储
                    const audio = new Audio('/audio/' + audioPath);
                    let isPlaying = false;
                    
                    playButton.onclick = () => {
                        if (isPlaying) {
                            // 暂停音频
                            audio.pause();
                            playButton.innerHTML = '🔊';
                            playButton.title = '播放音频';
                            isPlaying = false;
                        } else {
                            // 播放音频
                            if (currentAudio) {
                                currentAudio.pause();
                            }
                            currentAudio = audio;
                            audio.play().catch(error => {
                                console.log('音频播放失败:', error);
                            });
                            playButton.innerHTML = '⏸️';
                            playButton.title = '暂停音频';
                            isPlaying = true;
                        }
                    };
                    
                    // 监听音频结束事件
                    audio.addEventListener('ended', () => {
                        playButton.innerHTML = '🔊';
                        playButton.title = '播放音频';
                        isPlaying = false;
                    });
                    
                    // 将按钮添加到消息div中，紧跟在文字后面
                    messageDiv.appendChild(playButton);
                    
                    // 自动播放
                    setTimeout(() => {
                        playButton.click();
                    }, 500);
                }
                
                container.appendChild(messageDiv);
                container.scrollTop = container.scrollHeight;
            }

            function playAudio(audioPath) {
                if (currentAudio) {
                    currentAudio.pause();
                    currentAudio = null;
                }
                
                currentAudio = new Audio(audioPath);
                currentAudio.play().catch(error => {
                    console.log('音频播放失败:', error);
                });
            }

            function toggleVoiceInput() {
                try {
                    console.log('🎤 语音按钮被点击 - 开始调试');
                    console.log('当前录音状态:', isRecording);
                    console.log('mediaRecorder状态:', mediaRecorder);
                    
                    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                        console.log('❌ 浏览器不支持getUserMedia');
                        addMessage('❌ 您的浏览器不支持语音识别功能', 'ai');
                        return;
                    }
                    
                    console.log('✅ 浏览器支持getUserMedia，准备开始录音');
                    console.log('🎤 检查录音状态，isRecording =', isRecording);
                    
                    if (isRecording) {
                        // 停止录音
                        console.log('🛑 当前正在录音，准备停止');
                        stopRecording();
                    } else {
                        // 开始录音
                        console.log('🎤 准备开始录音，调用startRecording()');
                        startRecording();
                        console.log('🎤 startRecording()调用完成');
                    }
                } catch (error) {
                    console.error('❌ toggleVoiceInput函数出错:', error);
                    addMessage('❌ 语音功能出现错误: ' + error.message, 'ai');
                }
            }

            function startRecording() {
                console.log('🎤 startRecording函数被调用');
                navigator.mediaDevices.getUserMedia({ audio: true })
                    .then(stream => {
                        console.log('✅ 麦克风权限获取成功，开始录音');
                        console.log('🎵 音频流获取成功，轨道数量:', stream.getTracks().length);
                        isRecording = true;
                        audioChunks = [];
                        
                        // 更新按钮状态
                        const voiceBtn = document.getElementById('voiceBtn');
                        console.log('🎛️ 准备更新按钮状态');
                        voiceBtn.innerHTML = '⏹️ 停止';
                        voiceBtn.style.background = 'linear-gradient(135deg, #ff6b6b, #ee5a52)';
                        console.log('✅ 按钮状态已更新');
                        
                        // 创建录音器
                        console.log('🎙️ 准备创建MediaRecorder');
                        mediaRecorder = new MediaRecorder(stream, {
                            mimeType: 'audio/webm;codecs=opus'
                        });
                        console.log('✅ MediaRecorder创建成功');
                        
                        mediaRecorder.ondataavailable = (event) => {
                            console.log('📊 收到音频数据:', event.data.size, 'bytes');
                            if (event.data.size > 0) {
                                audioChunks.push(event.data);
                            }
                        };
                        
                        mediaRecorder.onstop = () => {
                            console.log('🎤 录音结束，处理音频数据');
                            processAudioData();
                        };
                        
                        // 开始录音
                        console.log('🎤 开始录音...');
                        mediaRecorder.start();
                        // 移除状态消息
                        // addMessage('🎤 开始录音，请说话...', 'ai');
                        console.log('✅ 录音已开始');
                        
                        // 10秒后自动停止
                        setTimeout(() => {
                            if (isRecording) {
                                console.log('⏰ 10秒时间到，自动停止录音');
                                stopRecording();
                            }
                        }, 10000);
                    })
                    .catch(error => {
                        console.log('❌ 麦克风权限获取失败:', error);
                        if (error.name === 'NotAllowedError') {
                            addMessage('❌ 请允许麦克风权限，然后刷新页面重试', 'ai');
                        } else if (error.name === 'NotFoundError') {
                            addMessage('❌ 未找到麦克风设备', 'ai');
                        } else {
                            addMessage('❌ 麦克风访问失败，请检查设备设置', 'ai');
                        }
                    });
            }

            function stopRecording() {
                if (mediaRecorder && isRecording) {
                    console.log('🛑 停止录音');
                    isRecording = false;
                    mediaRecorder.stop();
                    
                    // 恢复按钮状态
                    const voiceBtn = document.getElementById('voiceBtn');
                    voiceBtn.innerHTML = '🎤 语音';
                    voiceBtn.style.background = 'linear-gradient(135deg, #4ecdc4, #44a08d)';
                    
                    // 停止所有音频轨道
                    if (mediaRecorder.stream) {
                        mediaRecorder.stream.getTracks().forEach(track => track.stop());
                    }
                }
            }

            function processAudioData() {
                console.log('🎵 processAudioData函数被调用');
                if (audioChunks.length === 0) {
                    console.log('❌ 没有录到音频数据');
                    addMessage('❌ 没有录到音频数据', 'ai');
                    return;
                }
                
                console.log('🎵 处理音频数据，大小:', audioChunks.length);
                // 移除状态消息
                // addMessage('🎵 正在处理音频...', 'ai');
                
                // 创建音频blob
                const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                console.log('📊 音频文件大小:', audioBlob.size, 'bytes');
                
                // 发送音频到后端
                console.log('📤 准备调用sendAudioToBackend');
                sendAudioToBackend(audioBlob);
                console.log('📤 sendAudioToBackend调用完成');
            }

            async function sendAudioToBackend(audioBlob) {
                try {
                    console.log('📤 准备发送音频到后端');
                    // 移除状态消息
                    // addMessage('📤 正在发送音频进行识别...', 'ai');
                    
                    // 创建FormData对象
                    const formData = new FormData();
                    formData.append('audio', audioBlob, 'recording.webm');
                    
                    // 发送到后端
                    const response = await fetch('/speech-to-text', {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    console.log('📥 收到后端响应:', result);
                    
                    if (result.success) {
                        const recognizedText = result.text;
                        console.log('🎯 识别结果:', recognizedText);
                        // 移除状态消息
                        // addMessage(`🎯 识别结果: "${recognizedText}"`, 'ai');
                        
                        // 将识别结果作为用户消息发送给DeepSeek
                        await sendRecognizedText(recognizedText);
                    } else {
                        console.error('❌ 语音识别失败:', result.error);
                        addMessage('❌ 语音识别失败: ' + result.error, 'ai');
                    }
                } catch (error) {
                    console.error('❌ 发送音频失败:', error);
                    addMessage('❌ 发送音频失败，请重试', 'ai');
                }
            }

            async function sendRecognizedText(text) {
                try {
                    console.log('📝 发送识别文本到DeepSeek:', text);
                    // 移除状态消息
                    // addMessage(`📝 正在处理: "${text}"`, 'ai');
                    
                    // 显示用户消息
                    addMessage(text, 'user');
                    
                    // 显示思考指示器
                    showTypingIndicator();
                    
                    // 发送到聊天API
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            message: text,
                            generate_audio: audioEnabled
                        })
                    });
                    
                    const result = await response.json();
                    console.log('🎯 收到DeepSeek响应:', result);
                    
                    // 隐藏思考指示器
                    hideTypingIndicator();
                    
                    if (result.success) {
                        if (result.audio_path && audioEnabled) {
                            console.log('🎯 准备添加带音频的消息:', result.audio_path);
                            addMessageWithAudio(result.text_response, result.audio_path);
                        } else {
                            addMessage(result.text_response, 'ai');
                        }
                    } else {
                        addMessage('抱歉，我遇到了一些问题...', 'ai');
                    }
                } catch (error) {
                    hideTypingIndicator();
                    addMessage('网络连接出现问题，请稍后再试...', 'ai');
                }
            }

            function toggleAudio() {
                audioEnabled = !audioEnabled;
                const btn = event.target;
                if (audioEnabled) {
                    btn.innerHTML = '🔊 音频开';
                } else {
                    btn.innerHTML = '🔇 音频关';
                }
            }

            async function sendMessage() {
                console.log('🎯 sendMessage函数被调用');
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                
                if (!message) return;
                
                addMessage(message, 'user');
                input.value = '';
                
                // 显示思考指示器
                console.log('🎯 准备显示思考指示器');
                showTypingIndicator();
                
                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            message: message,
                            generate_audio: audioEnabled
                        })
                    });
                    
                    const result = await response.json();
                    console.log('🎯 收到服务器响应:', result);
                    
                    // 隐藏思考指示器
                    hideTypingIndicator();
                    
                    if (result.success) {
                        if (result.audio_path && audioEnabled) {
                            console.log('🎯 准备添加带音频的消息:', result.audio_path);
                            addMessageWithAudio(result.text_response, result.audio_path);
                        } else {
                            addMessage(result.text_response, 'ai');
                        }
                    } else {
                        addMessage('抱歉，我遇到了一些问题...', 'ai');
                    }
                } catch (error) {
                    hideTypingIndicator();
                    addMessage('网络连接出现问题，请稍后再试...', 'ai');
                }
            }

            function addMessage(text, sender) {
                const container = document.getElementById('chatContainer');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${sender}-message`;
                messageDiv.textContent = text;
                container.appendChild(messageDiv);
                container.scrollTop = container.scrollHeight;
            }

            async function clearHistory() {
                try {
                    const response = await fetch('/clear-history', {
                        method: 'POST'
                    });
                    const result = await response.json();
                    
                    if (result.success) {
                        document.getElementById('chatContainer').innerHTML = '';
                        addMessage('对话历史已清空～', 'ai');
                    }
                } catch (error) {
                    addMessage('清空历史时出现问题...', 'ai');
                }
            }

            async function checkStatus() {
                try {
                    const response = await fetch('/status');
                    const status = await response.json();
                    
                    let statusText = '系统状态：';
                    if (status.deepseek_api_key_configured) {
                        statusText += '✅ DeepSeek API已配置 ';
                    } else {
                        statusText += '❌ DeepSeek API未配置 ';
                    }
                    
                    if (status.services_status && status.services_status.tts_model) {
                        statusText += '✅ TTS模型正常 ';
                    } else {
                        statusText += '❌ TTS模型异常 ';
                    }
                    
                    document.getElementById('status').textContent = statusText;
                } catch (error) {
                    document.getElementById('status').textContent = '无法获取系统状态';
                }
            }

            async function showHistory() {
                try {
                    const response = await fetch('/history');
                    const result = await response.json();
                    
                    if (result.success) {
                        displayHistoryList(result.history_files);
                        document.getElementById('historyModal').style.display = 'block';
                    } else {
                        alert('获取历史记录失败');
                    }
                } catch (error) {
                    alert('获取历史记录时出现错误');
                }
            }

            function closeHistory() {
                document.getElementById('historyModal').style.display = 'none';
            }

            function displayHistoryList(historyFiles) {
                const historyList = document.getElementById('historyList');
                
                if (historyFiles.length === 0) {
                    historyList.innerHTML = '<p style="text-align: center; color: #666; padding: 20px;">暂无历史记录</p>';
                    return;
                }
                
                let html = '';
                historyFiles.forEach(file => {
                    const date = file.date;
                    const count = file.message_count;
                    const isToday = date === new Date().toISOString().split('T')[0];
                    
                    html += `
                        <div class="history-item">
                            <div class="history-date">
                                ${date} ${isToday ? '(今天)' : ''}
                            </div>
                            <div class="history-count">
                                ${count} 条消息
                            </div>
                            <div class="history-actions">
                                <button class="history-btn view-btn" onclick="viewHistory('${date}')">
                                    👁️ 查看
                                </button>
                                <button class="history-btn delete-btn" onclick="deleteHistory('${date}')">
                                    🗑️ 删除
                                </button>
                            </div>
                        </div>
                    `;
                });
                
                historyList.innerHTML = html;
            }

            async function viewHistory(date) {
                try {
                    const response = await fetch(`/history/${date}`);
                    const result = await response.json();
                    
                    if (result.success) {
                        // 清空当前聊天记录
                        document.getElementById('chatContainer').innerHTML = '';
                        
                        // 按顺序添加历史消息
                        for (let i = 0; i < result.messages.length; i += 2) {
                            if (i < result.messages.length) {
                                // 添加用户消息
                                addMessage(result.messages[i].content, 'user');
                            }
                            if (i + 1 < result.messages.length) {
                                // 添加AI回复（只显示文本，不包含音频）
                                addMessage(result.messages[i + 1].content, 'ai');
                            }
                        }
                        
                        closeHistory();
                        addMessage(`📚 已加载 ${date} 的聊天记录`, 'ai');
                    } else {
                        alert('加载历史记录失败');
                    }
                } catch (error) {
                    alert('加载历史记录时出现错误');
                }
            }

            async function deleteHistory(date) {
                if (!confirm(`确定要删除 ${date} 的聊天记录吗？`)) {
                    return;
                }
                
                try {
                    const response = await fetch(`/history/${date}`, {
                        method: 'DELETE'
                    });
                    const result = await response.json();
                    
                    if (result.success) {
                        // 刷新历史记录列表
                        showHistory();
                        addMessage(`🗑️ 已删除 ${date} 的聊天记录`, 'ai');
                    } else {
                        alert('删除历史记录失败');
                    }
                } catch (error) {
                    alert('删除历史记录时出现错误');
                }
            }

            // 页面加载时检查状态
            window.onload = function() {
                console.log('页面加载完成');
                addMessage('嗨，想我了吗？', 'ai');
                checkStatus();
            };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/chat")
async def chat_endpoint(request: Dict[str, Any]):
    """处理聊天请求"""
    message = request.get("message", "")
    if not message:
        raise HTTPException(status_code=400, detail="消息不能为空")
    
    result = chat_manager.process_message(message)
    return result

@app.post("/clear-history")
async def clear_history():
    """清空对话历史"""
    return chat_manager.clear_history()

@app.get("/status")
async def get_status():
    """获取系统状态"""
    return chat_manager.get_status()

@app.get("/history")
async def get_history_list():
    """获取历史记录列表"""
    history_files = chat_manager.get_history_files()
    return {
        "success": True,
        "history_files": history_files
    }

@app.get("/history/{date}")
async def get_history_by_date(date: str):
    """获取指定日期的历史记录"""
    messages = chat_manager.load_history_by_date(date)
    return {
        "success": True,
        "date": date,
        "messages": messages
    }

@app.delete("/history/{date}")
async def delete_history_by_date(date: str):
    """删除指定日期的历史记录"""
    success = chat_manager.delete_history_by_date(date)
    return {
        "success": success,
        "message": f"历史记录删除{'成功' if success else '失败'}"
    }

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    """获取音频文件"""
    audio_path = os.path.join(Config.AUDIO_OUTPUT_PATH, filename)
    if os.path.exists(audio_path):
        return FileResponse(audio_path, media_type="audio/wav")
    else:
        raise HTTPException(status_code=404, detail="音频文件不存在")

@app.post("/speech-to-text")
async def speech_to_text(audio: UploadFile = File(...)):
    """处理语音转文字请求"""
    try:
        print(f"🎤 收到音频文件: {audio.filename}, 大小: {audio.size} bytes")
        
        # 保存音频文件
        temp_audio_path = f"./temp_audio_{int(time.time())}.webm"
        with open(temp_audio_path, "wb") as f:
            content = await audio.read()
            f.write(content)
        
        print(f"💾 音频文件已保存: {temp_audio_path}")
        
        # 检查百度API配置
        if not Config.BAIDU_API_KEY or not Config.BAIDU_SECRET_KEY:
            print("❌ 百度API密钥未配置")
            return {
                "success": False,
                "error": "百度API密钥未配置"
            }
        
        # 使用百度语音识别
        baidu_recognizer = BaiduSpeechRecognition()
        recognized_text = await baidu_recognizer.recognize_audio(temp_audio_path)
        
        print(f"🎯 百度语音识别结果: {recognized_text}")
        
        # 清理临时文件
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
        
        if recognized_text:
            return {
                "success": True,
                "text": recognized_text,
                "file_size": len(content)
            }
        else:
            return {
                "success": False,
                "error": "语音识别失败，请重试"
            }
        
    except Exception as e:
        print(f"❌ 语音识别处理失败: {e}")
        return {
            "success": False,
            "error": str(e)
        }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket端点，用于实时对话"""
    await websocket.accept()
    try:
        while True:
            # 接收消息
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # 处理消息
            result = chat_manager.process_message(message_data.get("message", ""))
            
            # 发送回复
            await websocket.send_text(json.dumps(result))
            
    except WebSocketDisconnect:
        print("WebSocket连接断开")
    except Exception as e:
        print(f"WebSocket错误: {e}")

def run_cli():
    """运行命令行界面"""
    print("🤖 AI对话系统 - 命令行模式")
    print("输入 'quit' 或 'exit' 退出")
    print("输入 'clear' 清空对话历史")
    print("输入 'status' 查看系统状态")
    print("-" * 50)
    
    while True:
        try:
            user_input = input("你: ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                print("再见！")
                break
            elif user_input.lower() == 'clear':
                result = chat_manager.clear_history()
                print(f"系统: {result['message']}")
                continue
            elif user_input.lower() == 'status':
                status = chat_manager.get_status()
                print(f"系统状态: {status}")
                continue
            elif not user_input:
                continue
            
            # 处理用户消息
            result = chat_manager.process_message(user_input)
            
            if result['success']:
                print(f"AI: {result['text_response']}")
                if result['audio_path']:
                    print(f"音频文件: {result['audio_path']}")
            else:
                print(f"错误: {result.get('error', '未知错误')}")
                
        except KeyboardInterrupt:
            print("\n再见！")
            break
        except Exception as e:
            print(f"发生错误: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        # 命令行模式
        run_cli()
    else:
        # Web服务器模式
        print(f"🚀 启动AI对话系统服务器...")
        print(f"📱 Web界面: http://localhost:8000")
        print(f"🔧 API文档: http://localhost:8000/docs")
        print(f"💡 使用 --cli 参数启动命令行模式")
        print(f"💡 注意：HTTP模式下麦克风权限可能受限")
        
        uvicorn.run(
            "main:app",
            host=Config.HOST,
            port=Config.PORT,
            reload=False
        ) 