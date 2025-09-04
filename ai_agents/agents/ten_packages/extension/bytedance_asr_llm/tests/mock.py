#
# This file is part of TEN Framework, an open source project.
# Licensed under the Apache License, Version 2.0.
# See the LICENSE file for more information.
#

from types import SimpleNamespace
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
import asyncio
import json


@pytest.fixture(scope="function")
def patch_volcengine_ws():
    """Mock Volcengine ASR WebSocket client and related components."""

    patch_target = "ten_packages.extension.bytedance_asr_llm.extension.VolcengineASRClient"

    def _fake_ctor(url, app_key, access_key, config):
        class _FakeClient:
            def __init__(self, url, app_key, access_key, config):
                self.url = url
                self.app_key = app_key
                self.access_key = access_key
                self.config = config
                self.connected = False
                self.on_result_callback = None
                self.on_error_callback = None
                self.on_connected_callback = None
                self.on_disconnected_callback = None

            def set_on_result_callback(self, callback):
                self.on_result_callback = callback

            def set_on_error_callback(self, callback):
                self.on_error_callback = callback

            def set_on_connected_callback(self, callback):
                self.on_connected_callback = callback

            def set_on_disconnected_callback(self, callback):
                self.on_disconnected_callback = callback

            async def connect(self):
                print("[mock] VolcengineASRClient.connect called")
                self.connected = True

                # Trigger connected callback
                if self.on_connected_callback:
                    self.on_connected_callback()

                # Schedule result emission
                async def _emit_results():
                    print("[mock] _emit_results task started")
                    await asyncio.sleep(0.5)  # Give more time for audio to be sent

                    # Emit interim result
                    if self.on_result_callback:
                        print("[mock] About to emit interim result")
                        try:
                            from ten_packages.extension.bytedance_asr_llm.volcengine_asr_client import ASRResponse
                            from ten_packages.extension.bytedance_asr_llm.volcengine_asr_client import Utterance
                            interim_result = ASRResponse(
                                text="hello",
                                final=False,
                                code=0,
                                event=1,
                                is_last_package=False,
                                payload_sequence=1,
                                payload_size=0,
                                payload_msg={
                                    "result": [{
                                        "text": "hello",
                                        "utterances": [{
                                            "text": "hello",
                                            "start_time": 0,
                                            "end_time": 1000,
                                            "definite": False
                                        }]
                                    }]
                                },
                                result={
                                    "text": "hello",
                                    "utterances": [{
                                        "text": "hello",
                                        "start_time": 0,
                                        "end_time": 1000,
                                        "definite": False
                                    }]
                                },
                                utterances=[Utterance(
                                    text="hello",
                                    start_time=0,
                                    end_time=1000,
                                    definite=False
                                )],
                                start_ms=0,
                                duration_ms=1000,
                                language="zh-CN",
                                confidence=0.9
                            )
                            print("[mock] emitting interim asr_result")
                            await self.on_result_callback(interim_result)
                            print("[mock] interim result emitted successfully")
                        except Exception as e:
                            print(f"[mock] Error emitting interim result: {e}")
                    else:
                        print("[mock] No on_result_callback set for interim result")

                    await asyncio.sleep(0.5)

                    # Emit final result
                    if self.on_result_callback:
                        print("[mock] About to emit final result")
                        try:
                            final_result = ASRResponse(
                                text="hello world",
                                final=True,
                                code=0,
                                event=1,
                                is_last_package=True,
                                payload_sequence=2,
                                payload_size=0,
                                payload_msg={
                                    "result": [{
                                        "text": "hello world",
                                        "utterances": [{
                                            "text": "hello world",
                                            "start_time": 0,
                                            "end_time": 2000,
                                            "definite": True
                                        }]
                                    }]
                                },
                                result={
                                    "text": "hello world",
                                    "utterances": [{
                                        "text": "hello world",
                                        "start_time": 0,
                                        "end_time": 2000,
                                        "definite": True
                                    }]
                                },
                                utterances=[Utterance(
                                    text="hello world",
                                    start_time=0,
                                    end_time=2000,
                                    definite=True
                                )],
                                start_ms=0,
                                duration_ms=2000,
                                language="zh-CN",
                                confidence=0.95
                            )
                            print("[mock] emitting final asr_result")
                            await self.on_result_callback(final_result)
                            print("[mock] final result emitted successfully")
                        except Exception as e:
                            print(f"[mock] Error emitting final result: {e}")
                    else:
                        print("[mock] No on_result_callback set for final result")

                print("[mock] Creating _emit_results task")
                task = asyncio.create_task(_emit_results())
                print(f"[mock] Task created: {task}")
                return None

            async def disconnect(self):
                print("[mock] VolcengineASRClient.disconnect called")
                self.connected = False
                if self.on_disconnected_callback:
                    self.on_disconnected_callback()
                return None

            async def send_audio(self, audio_data, session_id):
                print(f"[mock] send_audio called with {len(audio_data)} bytes")
                return None

            async def listen(self):
                print("[mock] listen called")
                return None

        return _FakeClient(url, app_key, access_key, config)

    with patch(patch_target) as MockClient:
        MockClient.side_effect = _fake_ctor
        yield MockClient
