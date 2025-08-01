# 时间戳绑定功能说明

## 概述

时间戳绑定功能实现了聊天记录与音频文件的精确绑定，通过时间戳来关联每条消息和对应的音频文件。

## 功能特性

### 1. 时间戳生成
- 用户消息和助手消息都有独立的时间戳
- 时间戳格式：Unix时间戳（整数）
- 音频文件命名：`response_{timestamp}.wav`

### 2. 聊天记录格式

#### 新格式（包含时间戳）
```json
{
  "role": "user",
  "content": "用户消息",
  "timestamp": 1754040482
},
{
  "role": "assistant",
  "content": "助手回复",
  "timestamp": 1754040482,
  "audio_file": "response_1754040482.wav",
  "audio_exists": true
}
```

#### 旧格式（向后兼容）
```json
{
  "role": "user",
  "content": "用户消息"
},
{
  "role": "assistant",
  "content": "助手回复",
  "audio_file": "response_1754038556.wav"
}
```

### 3. 向后兼容性
- 自动为旧格式消息添加时间戳
- 验证音频文件是否存在
- 保持原有功能不受影响

## 实现细节

### 1. 消息处理流程
1. 用户发送消息 → 生成用户时间戳
2. AI生成回复 → 生成助手时间戳
3. TTS生成音频 → 使用助手时间戳命名
4. 保存聊天记录 → 包含时间戳和音频信息

### 2. 音频文件管理
- 位置：`./output/` 目录
- 命名规则：`response_{timestamp}.wav`
- 验证机制：检查文件是否存在

### 3. API端点

#### 获取音频文件信息
```
GET /audio-info
```
返回音频文件统计信息：
```json
{
  "total_files": 143,
  "existing_files": 143,
  "missing_files": 0,
  "files": [
    {
      "filename": "response_1754040482.wav",
      "exists": true,
      "size": 912384,
      "path": "./output/response_1754040482.wav"
    }
  ]
}
```

#### 获取音频文件
```
GET /audio/{filename}
```
返回音频文件内容。

## 使用方法

### 1. 发送消息
```python
from chat_manager import ChatManager

chat_manager = ChatManager()
result = chat_manager.process_message("你好")

print(f"用户时间戳: {result['user_timestamp']}")
print(f"助手时间戳: {result['assistant_timestamp']}")
print(f"音频文件: {result['audio_path']}")
```

### 2. 获取聊天记录
```python
history = chat_manager.get_history()
for message in history:
    if message['role'] == 'assistant' and 'audio_file' in message:
        print(f"消息: {message['content']}")
        print(f"音频: {message['audio_file']}")
        print(f"时间戳: {message['timestamp']}")
```

### 3. 验证音频文件
```python
# 检查音频文件是否存在
audio_exists = chat_manager.verify_audio_file("response_1754040482.wav")
print(f"音频文件存在: {audio_exists}")

# 获取音频文件完整路径
audio_path = chat_manager.get_audio_file_path("response_1754040482.wav")
print(f"音频文件路径: {audio_path}")
```

### 4. 获取音频文件统计
```python
audio_info = chat_manager.get_audio_files_info()
print(f"总文件数: {audio_info['total_files']}")
print(f"存在文件: {audio_info['existing_files']}")
print(f"缺失文件: {audio_info['missing_files']}")
```

## 测试

运行测试脚本验证功能：
```bash
python test_timestamp_binding.py
```

测试内容包括：
1. 消息处理和时间戳生成
2. 聊天记录格式检查
3. 音频文件信息统计
4. 向后兼容性验证

## 注意事项

1. **时间戳精度**：使用秒级时间戳，同一秒内的消息可能时间戳相同
2. **文件命名**：音频文件使用时间戳命名，确保唯一性
3. **文件验证**：自动检查音频文件是否存在，避免引用不存在的文件
4. **向后兼容**：旧格式聊天记录会自动添加时间戳字段

## 未来改进

1. **毫秒级精度**：考虑使用毫秒级时间戳提高精度
2. **文件压缩**：对音频文件进行压缩以节省存储空间
3. **自动清理**：定期清理过期的音频文件
4. **备份机制**：为音频文件添加备份和恢复功能 