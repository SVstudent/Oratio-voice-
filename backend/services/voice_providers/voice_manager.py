"""
Voice Provider Manager with Failover Logic

Manages multiple voice providers (MiniMax primary, Gemini backup)
with automatic failover and health checking.
"""

import asyncio
from typing import Optional, Literal
from .minimax_service import minimax_service
from .gemini_service import gemini_service

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
        def voice_session_started(self, *args, **kwargs):
            pass
        def voice_session_ended(self, *args, **kwargs):
            pass
        def voice_provider_failover(self, *args, **kwargs):
            pass
        def session_message(self, *args, **kwargs):
            pass
        def error_occurred(self, *args, **kwargs):
            pass
    
    metrics = MockMetrics()


VoiceProvider = Literal["minimax", "gemini", "auto"]


class VoiceProviderManager:
    """Manages voice providers with automatic failover"""

    def __init__(self):
        self.primary_provider = minimax_service
        self.backup_provider = gemini_service
        self.current_provider = None
        self.health_check_interval = 60  # seconds
        self._health_check_task = None

    async def initialize(self):
        """Initialize voice provider manager"""
        # Check which providers are available
        minimax_available = self.primary_provider.is_available()
        gemini_available = self.backup_provider.is_available()

        print(f"🎤 Voice Providers Status:")
        print(f"   MiniMax: {'✅ Available' if minimax_available else '❌ Not configured'}")
        print(f"   Gemini: {'✅ Available' if gemini_available else '❌ Not configured'}")

        # Set current provider
        if minimax_available:
            self.current_provider = self.primary_provider
            print(f"✅ Using MiniMax as primary voice provider")
        elif gemini_available:
            self.current_provider = self.backup_provider
            print(f"⚠️  Using Gemini as fallback voice provider")
        else:
            print(f"❌ No voice providers configured!")

        # Start health check task
        self._health_check_task = asyncio.create_task(self._health_check_loop())

    async def shutdown(self):
        """Shutdown voice provider manager"""
        if self._health_check_task:
            self._health_check_task.cancel()
            try:
                await self._health_check_task
            except asyncio.CancelledError:
                pass

    async def _health_check_loop(self):
        """Periodically check provider health and failover if needed"""
        while True:
            try:
                await asyncio.sleep(self.health_check_interval)

                # Check primary provider health
                if self.primary_provider.is_available():
                    primary_healthy = await self.primary_provider.health_check()

                    if primary_healthy and self.current_provider != self.primary_provider:
                        # Failback to primary
                        print("✅ MiniMax is healthy - failing back to primary")
                        metrics.voice_provider_failover("gemini", "minimax")
                        self.current_provider = self.primary_provider

                    elif not primary_healthy and self.current_provider == self.primary_provider:
                        # Failover to backup
                        if self.backup_provider.is_available():
                            print("⚠️  MiniMax unhealthy - failing over to Gemini")
                            metrics.voice_provider_failover("minimax", "gemini")
                            self.current_provider = self.backup_provider

            except Exception as e:
                print(f"⚠️  Health check error: {e}")

    @trace_operation("voice.get_provider")
    def get_provider(self, preferred: VoiceProvider = "auto"):
        """
        Get voice provider based on preference and availability

        Args:
            preferred: Preferred provider ("minimax", "gemini", or "auto")

        Returns:
            Voice provider service
        """
        if preferred == "minimax" and self.primary_provider.is_available():
            return self.primary_provider
        elif preferred == "gemini" and self.backup_provider.is_available():
            return self.backup_provider
        elif preferred == "auto":
            return self.current_provider
        else:
            # Fallback to any available provider
            if self.primary_provider.is_available():
                return self.primary_provider
            elif self.backup_provider.is_available():
                return self.backup_provider
            else:
                raise ValueError("No voice providers available")

    @trace_operation("voice.text_to_speech")
    async def text_to_speech(
        self,
        text: str,
        voice_id: str = "default",
        sample_rate: int = 24000,
        preferred_provider: VoiceProvider = "auto",
    ) -> Optional[bytes]:
        """
        Convert text to speech with automatic failover

        Args:
            text: Text to convert
            voice_id: Voice ID
            sample_rate: Audio sample rate
            preferred_provider: Preferred provider

        Returns:
            Audio bytes or None
        """
        provider = self.get_provider(preferred_provider)

        try:
            result = await provider.text_to_speech(text, voice_id, sample_rate)
            if result:
                return result

            # Try backup if primary failed
            if provider == self.primary_provider and self.backup_provider.is_available():
                print("⚠️  Primary TTS failed, trying backup")
                metrics.voice_provider_failover("minimax", "gemini")
                return await self.backup_provider.text_to_speech(
                    text, voice_id, sample_rate
                )

        except Exception as e:
            print(f"⚠️  TTS error: {e}")
            metrics.error_occurred("tts_error", "voice_manager")

            # Try backup
            if provider == self.primary_provider and self.backup_provider.is_available():
                print("⚠️  Trying backup provider")
                metrics.voice_provider_failover("minimax", "gemini")
                return await self.backup_provider.text_to_speech(
                    text, voice_id, sample_rate
                )

        return None

    @trace_operation("voice.speech_to_text")
    async def speech_to_text(
        self,
        audio_data: bytes,
        language: str = "en",
        preferred_provider: VoiceProvider = "auto",
    ) -> Optional[str]:
        """
        Convert speech to text with automatic failover

        Args:
            audio_data: Audio bytes
            language: Language code
            preferred_provider: Preferred provider

        Returns:
            Transcribed text or None
        """
        provider = self.get_provider(preferred_provider)

        try:
            result = await provider.speech_to_text(audio_data, language)
            if result:
                return result

            # Try backup if primary failed
            if provider == self.primary_provider and self.backup_provider.is_available():
                print("⚠️  Primary STT failed, trying backup")
                metrics.voice_provider_failover("minimax", "gemini")
                return await self.backup_provider.speech_to_text(audio_data, language)

        except Exception as e:
            print(f"⚠️  STT error: {e}")
            metrics.error_occurred("stt_error", "voice_manager")

            # Try backup
            if provider == self.primary_provider and self.backup_provider.is_available():
                print("⚠️  Trying backup provider")
                metrics.voice_provider_failover("minimax", "gemini")
                return await self.backup_provider.speech_to_text(audio_data, language)

        return None

    @trace_operation("voice.handle_websocket")
    async def handle_websocket(
        self,
        websocket,
        agent_id: str,
        session_id: str,
        agent_callback: callable,
        preferred_provider: VoiceProvider = "auto",
    ):
        """
        Handle WebSocket connection with automatic failover

        Args:
            websocket: WebSocket connection
            agent_id: Agent ID
            session_id: Session ID
            agent_callback: Agent callback function
            preferred_provider: Preferred provider
        """
        provider = self.get_provider(preferred_provider)

        try:
            await provider.handle_websocket(
                websocket, agent_id, session_id, agent_callback
            )
        except Exception as e:
            print(f"⚠️  WebSocket error with {provider.__class__.__name__}: {e}")

            # Try backup if primary failed
            if provider == self.primary_provider and self.backup_provider.is_available():
                print("⚠️  Trying backup provider for WebSocket")
                metrics.voice_provider_failover("minimax", "gemini")

                # Send failover notification
                await websocket.send_json(
                    {
                        "type": "provider_failover",
                        "from": "minimax",
                        "to": "gemini",
                        "reason": str(e),
                    }
                )

                # Try with backup
                await self.backup_provider.handle_websocket(
                    websocket, agent_id, session_id, agent_callback
                )
            else:
                raise

    def get_current_provider_name(self) -> str:
        """Get name of current provider"""
        if self.current_provider == self.primary_provider:
            return "minimax"
        elif self.current_provider == self.backup_provider:
            return "gemini"
        else:
            return "none"

    def get_provider_status(self) -> dict:
        """Get status of all providers"""
        return {
            "current": self.get_current_provider_name(),
            "minimax": {
                "available": self.primary_provider.is_available(),
                "configured": bool(self.primary_provider.api_key),
            },
            "gemini": {
                "available": self.backup_provider.is_available(),
                "configured": bool(self.backup_provider.api_key),
            },
        }


# Global instance
voice_manager = VoiceProviderManager()
