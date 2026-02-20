"""
MiniMax Voice Service Integration

Provides voice interaction capabilities using MiniMax's voice models.
"""

import asyncio
import base64
import json
import os
from typing import AsyncGenerator, Optional, Dict, Any
import aiohttp

# Optional Datadog integration
try:
    from observability.datadog_config import trace_operation, metrics
    DATADOG_AVAILABLE = True
except ImportError:
    DATADOG_AVAILABLE = False
    # Create no-op decorators
    def trace_operation(name):
        def decorator(func):
            return func
        return decorator
    
    class MockMetrics:
        def error_occurred(self, *args, **kwargs):
            pass
    
    metrics = MockMetrics()


class MiniMaxVoiceService:
    """MiniMax voice service for real-time voice interactions"""

    def __init__(self):
        self.api_key = os.getenv("MINIMAX_API_KEY", "")
        self.group_id = os.getenv("MINIMAX_GROUP_ID", "")
        self.base_url = os.getenv(
            "MINIMAX_API_URL", "https://api.minimax.chat/v1/voice"
        )
        self.model = os.getenv("MINIMAX_VOICE_MODEL", "speech-01")

        if not self.api_key:
            print("⚠️  MINIMAX_API_KEY not set - MiniMax voice will not work")

    def is_available(self) -> bool:
        """Check if MiniMax service is configured"""
        return bool(self.api_key and self.group_id)

    @trace_operation("minimax.health_check")
    async def health_check(self) -> bool:
        """Check if MiniMax service is healthy"""
        if not self.is_available():
            return False

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.base_url}/health",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=aiohttp.ClientTimeout(total=5),
                ) as response:
                    return response.status == 200
        except Exception as e:
            print(f"⚠️  MiniMax health check failed: {e}")
            return False

    @trace_operation("minimax.text_to_speech")
    async def text_to_speech(
        self,
        text: str,
        voice_id: str = "default",
        sample_rate: int = 24000,
    ) -> Optional[bytes]:
        """
        Convert text to speech using MiniMax

        Args:
            text: Text to convert to speech
            voice_id: Voice ID to use
            sample_rate: Audio sample rate

        Returns:
            Audio bytes or None if failed
        """
        if not self.is_available():
            raise ValueError("MiniMax service not configured")

        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": self.model,
                    "text": text,
                    "voice_id": voice_id,
                    "sample_rate": sample_rate,
                    "group_id": self.group_id,
                }

                async with session.post(
                    f"{self.base_url}/tts",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as response:
                    if response.status == 200:
                        return await response.read()
                    else:
                        error_text = await response.text()
                        print(f"⚠️  MiniMax TTS failed: {error_text}")
                        return None
        except Exception as e:
            print(f"⚠️  MiniMax TTS error: {e}")
            metrics.error_occurred("minimax_tts_error", "minimax_service")
            return None

    @trace_operation("minimax.speech_to_text")
    async def speech_to_text(
        self,
        audio_data: bytes,
        language: str = "en",
    ) -> Optional[str]:
        """
        Convert speech to text using MiniMax

        Args:
            audio_data: Audio bytes to transcribe
            language: Language code

        Returns:
            Transcribed text or None if failed
        """
        if not self.is_available():
            raise ValueError("MiniMax service not configured")

        try:
            async with aiohttp.ClientSession() as session:
                # Encode audio as base64
                audio_base64 = base64.b64encode(audio_data).decode("utf-8")

                payload = {
                    "model": self.model,
                    "audio": audio_base64,
                    "language": language,
                    "group_id": self.group_id,
                }

                async with session.post(
                    f"{self.base_url}/stt",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("text", "")
                    else:
                        error_text = await response.text()
                        print(f"⚠️  MiniMax STT failed: {error_text}")
                        return None
        except Exception as e:
            print(f"⚠️  MiniMax STT error: {e}")
            metrics.error_occurred("minimax_stt_error", "minimax_service")
            return None

    @trace_operation("minimax.streaming_conversation")
    async def streaming_conversation(
        self,
        audio_stream: AsyncGenerator[bytes, None],
        agent_callback: callable,
        voice_id: str = "default",
        session_id: Optional[str] = None,
    ) -> AsyncGenerator[bytes, None]:
        """
        Handle streaming voice conversation with MiniMax

        Args:
            audio_stream: Async generator of incoming audio chunks
            agent_callback: Async function to get agent response from text
            voice_id: Voice ID for TTS
            session_id: Session ID for tracking

        Yields:
            Audio response chunks
        """
        if not self.is_available():
            raise ValueError("MiniMax service not configured")

        try:
            # Buffer for accumulating audio
            audio_buffer = bytearray()
            buffer_duration_ms = 1000  # Process every 1 second of audio

            async for audio_chunk in audio_stream:
                audio_buffer.extend(audio_chunk)

                # Process when buffer reaches threshold
                if len(audio_buffer) >= (16000 * 2 * buffer_duration_ms // 1000):
                    # Transcribe audio
                    transcription = await self.speech_to_text(bytes(audio_buffer))

                    if transcription:
                        print(f"🎤 User: {transcription}")

                        # Get agent response
                        agent_response = await agent_callback(transcription)
                        print(f"🤖 Agent: {agent_response}")

                        # Convert to speech
                        audio_response = await self.text_to_speech(
                            agent_response, voice_id
                        )

                        if audio_response:
                            # Yield audio chunks
                            chunk_size = 4096
                            for i in range(0, len(audio_response), chunk_size):
                                yield audio_response[i : i + chunk_size]

                    # Clear buffer
                    audio_buffer.clear()

        except Exception as e:
            print(f"⚠️  MiniMax streaming error: {e}")
            metrics.error_occurred("minimax_streaming_error", "minimax_service")
            raise

    @trace_operation("minimax.websocket_handler")
    async def handle_websocket(
        self,
        websocket,
        agent_id: str,
        session_id: str,
        agent_callback: callable,
    ):
        """
        Handle WebSocket connection for voice interaction

        Args:
            websocket: WebSocket connection
            agent_id: Agent ID
            session_id: Session ID
            agent_callback: Function to get agent response
        """
        metrics.voice_session_started(agent_id, session_id, "minimax")

        try:
            # Send initial greeting
            await websocket.send_json(
                {
                    "type": "session_start",
                    "session_id": session_id,
                    "provider": "minimax",
                }
            )

            # Handle incoming messages
            while True:
                message = await websocket.receive()

                if message["type"] == "websocket.disconnect":
                    break

                if message["type"] == "websocket.receive":
                    data = message.get("bytes") or message.get("text")

                    if isinstance(data, str):
                        # JSON message
                        msg = json.loads(data)

                        if msg.get("type") == "audio":
                            # Decode base64 audio
                            audio_data = base64.b64decode(msg["data"])

                            # Transcribe
                            transcription = await self.speech_to_text(audio_data)

                            if transcription:
                                # Send transcription
                                await websocket.send_json(
                                    {
                                        "type": "transcription",
                                        "text": transcription,
                                    }
                                )

                                # Get agent response
                                agent_response = await agent_callback(transcription)

                                # Send text response
                                await websocket.send_json(
                                    {
                                        "type": "agent_response",
                                        "text": agent_response,
                                    }
                                )

                                # Convert to speech
                                audio_response = await self.text_to_speech(
                                    agent_response
                                )

                                if audio_response:
                                    # Send audio response
                                    audio_base64 = base64.b64encode(
                                        audio_response
                                    ).decode("utf-8")
                                    await websocket.send_json(
                                        {
                                            "type": "audio_response",
                                            "data": audio_base64,
                                        }
                                    )

                                metrics.session_message(agent_id, session_id, "voice")

        except Exception as e:
            print(f"⚠️  WebSocket error: {e}")
            metrics.error_occurred("websocket_error", "minimax_service")
            await websocket.send_json(
                {
                    "type": "error",
                    "message": str(e),
                }
            )
        finally:
            metrics.voice_session_ended(agent_id, session_id, 0, "minimax")


# Global instance
minimax_service = MiniMaxVoiceService()
