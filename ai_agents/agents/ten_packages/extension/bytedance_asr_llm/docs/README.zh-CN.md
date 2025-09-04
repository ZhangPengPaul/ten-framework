# 火山引擎ASR大模型版扩展

一个用于火山引擎ASR大模型版服务的Python扩展，提供实时双向流式语音识别功能，完全支持异步架构。

## 功能特性

- **双向流式识别**: 支持实时音频流输入和识别结果输出
- **大模型支持**: 基于火山引擎ASR大模型版，提供高精度识别
- **完全异步支持**: 采用完整的异步架构，实现高性能语音识别
- **实时音频处理**: 支持低延迟的实时音频流处理
- **多种音频格式**: 支持WAV、PCM等音频格式
- **智能分段**: 自动音频分段，优化识别性能
- **音频录制**: 可选的音频录制功能，用于调试和分析
- **错误处理**: 全面的错误处理和自动重连机制
- **多语言支持**: 支持中文等多种语言识别

## 配置参数

### 必需参数

- `app_key`: 火山引擎应用密钥
- `access_key`: 火山引擎访问密钥

### 可选参数

- `api_url`: ASR服务地址（默认：wss://openspeech.bytedance.com/api/v3/sauc/bigmodel）
- `sample_rate`: 音频采样率（默认：16000）
- `audio_format`: 音频格式（默认：wav）
- `codec`: 音频编码（默认：raw）
- `bits`: 音频位深度（默认：16）
- `channel`: 音频声道数（默认：1）
- `model_name`: ASR模型名称（默认：bigmodel）
- `enable_itn`: 启用数字文本标准化（默认：true）
- `enable_punc`: 启用标点符号（默认：true）
- `enable_ddc`: 启用说话人分离（默认：true）
- `show_utterances`: 显示话语信息（默认：true）
- `enable_nonstream`: 启用非流式模式（默认：false）
- `user_uid`: 用户ID（默认：default_user）
- `max_retries`: 最大重连次数（默认：5）
- `base_delay`: 重连基础延迟（默认：0.3秒）
- `segment_duration_ms`: 音频分段时长（默认：200毫秒）
- `dump`: 启用音频录制（默认：false）
- `dump_path`: 录制文件路径（默认：当前目录）
- `language`: 识别语言（默认：zh-CN）

### 配置示例

```json
{
  "app_key": "your_app_key_here",
  "access_key": "your_access_key_here",
  "api_url": "wss://openspeech.bytedance.com/api/v3/sauc/bigmodel",
  "sample_rate": 16000,
  "audio_format": "wav",
  "enable_itn": true,
  "enable_punc": true,
  "enable_ddc": true,
  "dump": false,
  "language": "zh-CN"
}
```

## API接口

扩展实现了 `AsyncASRBaseExtension` 接口，提供以下关键方法：

### 核心方法

- `on_init()`: 初始化ASR客户端和配置
- `start_connection()`: 建立与火山引擎ASR服务的连接
- `stop_connection()`: 关闭ASR服务连接
- `send_audio()`: 发送音频帧进行识别
- `finalize()`: 结束当前识别会话

### 事件处理器

- `on_asr_start()`: ASR会话开始时调用
- `on_asr_result()`: 接收到识别结果时调用
- `on_asr_finalize()`: ASR会话结束时调用
- `on_asr_error()`: 发生错误时调用

## 使用方法

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置参数

在 `property.json` 中配置您的火山引擎认证信息：

```json
{
  "app_key": "your_actual_app_key",
  "access_key": "your_actual_access_key"
}
```

### 3. 启动扩展

扩展将自动连接到火山引擎ASR服务，并开始处理音频输入。

## 技术架构

### 双向流式通信

扩展使用WebSocket协议与火山引擎ASR服务建立双向流式连接：

1. **连接建立**: 发送认证信息和初始化配置
2. **音频传输**: 实时发送音频数据流
3. **结果接收**: 异步接收识别结果
4. **会话管理**: 支持会话开始、进行和结束

### 音频处理流程

```
音频输入 → 音频分段 → 压缩编码 → 网络传输 → ASR识别 → 结果解析 → 输出处理
```

### 错误处理机制

- **网络异常**: 自动重连和指数退避策略
- **服务异常**: 错误码分类和相应处理
- **配置错误**: 参数验证和错误提示

## 性能优化

- **音频分段**: 智能音频分段，平衡延迟和效率
- **异步处理**: 完全异步架构，支持高并发
- **连接复用**: WebSocket连接复用，减少连接开销
- **内存管理**: 音频缓冲区管理，防止内存泄漏

## 故障排除

### 常见问题

1. **连接失败**: 检查网络连接和认证信息
2. **识别延迟**: 调整音频分段时长参数
3. **内存占用**: 检查音频录制设置和缓冲区大小

### 日志级别

扩展支持多种日志级别，可通过配置调整：

- DEBUG: 详细调试信息
- INFO: 一般信息
- WARNING: 警告信息
- ERROR: 错误信息

## 参考文档

- [火山引擎ASR大模型版官方文档](https://www.volcengine.com/docs/6561/1354869)
- [TEN Framework开发指南](https://github.com/ten-framework/ten-framework)

## 许可证

本扩展基于Apache License 2.0开源协议。
