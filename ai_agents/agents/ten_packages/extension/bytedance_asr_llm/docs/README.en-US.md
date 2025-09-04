# Volcengine ASR LLM Extension

A Python extension for Volcengine ASR Large Language Model service, providing real-time bidirectional streaming speech recognition functionality with full asynchronous architecture support.

## Features

- **Bidirectional Streaming Recognition**: Supports real-time audio stream input and recognition result output
- **Large Model Support**: Based on Volcengine ASR Large Language Model for high-precision recognition
- **Full Asynchronous Support**: Complete asynchronous architecture for high-performance speech recognition
- **Real-time Audio Processing**: Low-latency real-time audio stream processing
- **Multiple Audio Formats**: Supports WAV, PCM and other audio formats
- **Smart Segmentation**: Automatic audio segmentation for optimized recognition performance
- **Audio Recording**: Optional audio recording for debugging and analysis
- **Error Handling**: Comprehensive error handling and automatic reconnection mechanism
- **Multi-language Support**: Supports Chinese and other language recognition

## Configuration Parameters

### Required Parameters

- `app_key`: Volcengine application key
- `access_key`: Volcengine access key

### Optional Parameters

- `api_url`: ASR service URL (default: wss://openspeech.bytedance.com/api/v3/sauc/bigmodel)
- `sample_rate`: Audio sample rate (default: 16000)
- `audio_format`: Audio format (default: wav)
- `codec`: Audio codec (default: raw)
- `bits`: Audio bit depth (default: 16)
- `channel`: Audio channel count (default: 1)
- `model_name`: ASR model name (default: bigmodel)
- `enable_itn`: Enable inverse text normalization (default: true)
- `enable_punc`: Enable punctuation (default: true)
- `enable_ddc`: Enable speaker diarization (default: true)
- `show_utterances`: Show utterance information (default: true)
- `enable_nonstream`: Enable non-streaming mode (default: false)
- `user_uid`: User ID (default: default_user)
- `max_retries`: Maximum reconnection attempts (default: 5)
- `base_delay`: Reconnection base delay (default: 0.3 seconds)
- `segment_duration_ms`: Audio segment duration (default: 200 milliseconds)
- `dump`: Enable audio recording (default: false)
- `dump_path`: Recording file path (default: current directory)
- `language`: Recognition language (default: zh-CN)

### Configuration Example

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

## API Interface

The extension implements the `AsyncASRBaseExtension` interface, providing the following key methods:

### Core Methods

- `on_init()`: Initialize ASR client and configuration
- `start_connection()`: Establish connection to Volcengine ASR service
- `stop_connection()`: Close ASR service connection
- `send_audio()`: Send audio frame for recognition
- `finalize()`: End current ASR session

### Event Handlers

- `on_asr_start()`: Called when ASR session starts
- `on_asr_result()`: Called when recognition result is received
- `on_asr_finalize()`: Called when ASR session ends
- `on_asr_error()`: Called when an error occurs

## Usage

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Parameters

Configure your Volcengine authentication information in `property.json`:

```json
{
  "app_key": "your_actual_app_key",
  "access_key": "your_actual_access_key"
}
```

### 3. Start Extension

The extension will automatically connect to the Volcengine ASR service and begin processing audio input.

## Technical Architecture

### Bidirectional Streaming Communication

The extension uses WebSocket protocol to establish bidirectional streaming connection with Volcengine ASR service:

1. **Connection Establishment**: Send authentication information and initialization configuration
2. **Audio Transmission**: Real-time audio data stream transmission
3. **Result Reception**: Asynchronous recognition result reception
4. **Session Management**: Support for session start, progress, and end

### Audio Processing Flow

```
Audio Input → Audio Segmentation → Compression Encoding → Network Transmission → ASR Recognition → Result Parsing → Output Processing
```

### Error Handling Mechanism

- **Network Exceptions**: Automatic reconnection and exponential backoff strategy
- **Service Exceptions**: Error code classification and corresponding handling
- **Configuration Errors**: Parameter validation and error prompts

## Performance Optimization

- **Audio Segmentation**: Intelligent audio segmentation for balanced latency and efficiency
- **Asynchronous Processing**: Complete asynchronous architecture supporting high concurrency
- **Connection Reuse**: WebSocket connection reuse to reduce connection overhead
- **Memory Management**: Audio buffer management to prevent memory leaks

## Troubleshooting

### Common Issues

1. **Connection Failure**: Check network connection and authentication information
2. **Recognition Delay**: Adjust audio segment duration parameters
3. **Memory Usage**: Check audio recording settings and buffer size

### Log Levels

The extension supports multiple log levels, adjustable through configuration:

- DEBUG: Detailed debug information
- INFO: General information
- WARNING: Warning information
- ERROR: Error information

## References

- [Volcengine ASR LLM Official Documentation](https://www.volcengine.com/docs/6561/1354869)
- [TEN Framework Development Guide](https://github.com/ten-framework/ten-framework)

## License

This extension is based on Apache License 2.0 open source license.
