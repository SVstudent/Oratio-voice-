"""
Google Gemini Voice Service Integration (Backup)

Provides voice interaction capabilities using Google's Gemini models as a backup.
"""

import asyncio
import base64
import json
import os
from typing import AsyncGenerator, Optional
import google.generativeai as genai

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


class GeminiVoiceService:
    """Gemini voice service as backup for MiniMax"""

    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY", "")
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")

        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
        else:
            print("⚠️  GOOGLE_API_KEY not set - Gemini backup will not work")
            self.model = None

    def is_available(self) -> bool:
        """Check if Gemini service is configured"""
        return bool(self.api_key and self.model)

    @trace_operation("gemini.health_check")
    async def health_check(self) -> bool:
        """Check if Gemini service is healthy"""
        if not self.is_available():
            return False

        try:
            # Simple test generation
            response = await asyncio.to_thread(
                self.model.generate_content,
                "Hello",
            )
            return bool(response.text)
        except Exception as e:
            print(f"⚠️  Gemini health check failed: {e}")
            return False

    @trace_operation("gemini.text_to_speech")
    async def text_to_speech(
        self,
        text: str,
        voice_id: str = "default",
        sample_rate: int = 24000,
    ) -> Optional[bytes]:
        """
        Convert text to speech using Gemini

        Note: Gemini doesn't have native TTS, so this is a placeholder
        that would need integration with Google Cloud TTS API.

        Args:
            text: Text to convert to speech
            voice_id: Voice ID to use
            sample_rate: Audio sample rate

        Returns:
            Audio bytes or None if failed
        """
        # TODO: Integrate with Google Cloud Text-to-Speech API
        # For now, return None to indicate TTS not available
        print(f"⚠️  Gemini TTS not implemented - text: {text}")
        return None

    @trace_operation("gemini.speech_to_text")
    async def speech_to_text(
        self,
        audio_data: bytes,
        language: str = "en",
    ) -> Optional[str]:
        """
        Convert speech to text using Gemini

        Args:
            audio_data: Audio bytes to transcribe
            language: Language code

        Returns:
            Transcribed text or None if failed
        """
        if not self.is_available():
            raise ValueError("Gemini service not configured")

        try:
            # Encode audio as base64
            audio_base64 = base64.b64encode(audio_data).decode("utf-8")

            # Create audio part for Gemini
            audio_part = {
                "mime_type": "audio/wav",
                "data": audio_base64,
            }

            # Generate transcription
            response = await asyncio.to_thread(
                self.model.generate_content,
                [
                    "Transcribe this audio to text. Only return the transcription, nothing else.",
                    audio_part,
                ],
            )

            return response.text.strip()

        except Exception as e:
            print(f"⚠️  Gemini STT error: {e}")
            metrics.error_occurred("gemini_stt_error", "gemini_service")
            return None

    @trace_operation("gemini.generate_response")
    async def generate_response(
        self,
        prompt: str,
        context: Optional[str] = None,
    ) -> Optional[str]:
        """
        Generate text response using Gemini

        Args:
            prompt: User prompt
            context: Optional context/history

        Returns:
            Generated response or None if failed
        """
        if not self.is_available():
            raise ValueError("Gemini service not configured")

        try:
            full_prompt = prompt
            if context:
                full_prompt = f"{context}\n\nUser: {prompt}\nAssistant:"

            response = await asyncio.to_thread(
                self.model.generate_content,
                full_prompt,
            )

            return response.text.strip()

        except Exception as e:
            print(f"⚠️  Gemini generation error: {e}")
            metrics.error_occurred("gemini_generation_error", "gemini_service")
            return None

    @trace_operation("gemini.websocket_handler")
    async def handle_websocket(
        self,
        websocket,
        agent_id: str,
        session_id: str,
        agent_callback: callable,
    ):
        """
        Handle WebSocket connection for voice interaction (backup mode)

        Args:
            websocket: WebSocket connection
            agent_id: Agent ID
            session_id: Session ID
            agent_callback: Function to get agent response
        """
        metrics.voice_session_started(agent_id, session_id, "gemini")

        try:
            # Send initial greeting
            await websocket.send_json(
                {
                    "type": "session_start",
                    "session_id": session_id,
                    "provider": "gemini",
                    "note": "Using Gemini backup - limited voice features",
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

                            # Transcribe using Gemini
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

                                # Send text response (no audio in backup mode)
                                await websocket.send_json(
                                    {
                                        "type": "agent_response",
                                        "text": agent_response,
                                        "note": "Audio response not available in backup mode",
                                    }
                                )

                                metrics.session_message(agent_id, session_id, "voice")

                        elif msg.get("type") == "text":
                            # Handle text-only messages
                            user_text = msg.get("text", "")

                            # Get agent response
                            agent_response = await agent_callback(user_text)

                            # Send text response
                            await websocket.send_json(
                                {
                                    "type": "agent_response",
                                    "text": agent_response,
                                }
                            )

                            metrics.session_message(agent_id, session_id, "text")

        except Exception as e:
            print(f"⚠️  Gemini WebSocket error: {e}")
            metrics.error_occurred("websocket_error", "gemini_service")
            await websocket.send_json(
                {
                    "type": "error",
                    "message": str(e),
                }
            )
        finally:
            metrics.voice_session_ended(agent_id, session_id, 0, "gemini")


# Global instance
gemini_service = GeminiVoiceService()
