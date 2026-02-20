"""
Datadog Observability Configuration for Oratio Platform

This module configures Datadog APM, custom metrics, and LLM observability
for the AWS x Datadog GenAI Hackathon.
"""

import os
from typing import Any, Dict, Optional
from functools import wraps
import time

from ddtrace import tracer, patch_all
from ddtrace.llmobs import LLMObs
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi
from datadog_api_client.v1.model.metrics_payload import MetricsPayload
from datadog_api_client.v1.model.point import Point
from datadog_api_client.v1.model.series import Series


class DatadogConfig:
    """Datadog configuration and initialization"""

    def __init__(self):
        self.service_name = os.getenv("DD_SERVICE", "oratio-backend")
        self.env = os.getenv("DD_ENV", "hackathon")
        self.version = os.getenv("DD_VERSION", "1.0.0")
        self.api_key = os.getenv("DD_API_KEY", "")
        self.app_key = os.getenv("DD_APP_KEY", "")
        self.trace_enabled = os.getenv("DD_TRACE_ENABLED", "true").lower() == "true"
        self.llm_obs_enabled = os.getenv("DD_LLM_OBS_ENABLED", "true").lower() == "true"

        # Initialize Datadog
        self._init_datadog()

    def _init_datadog(self):
        """Initialize Datadog tracing and observability"""
        if not self.trace_enabled:
            print("⚠️  Datadog tracing is disabled")
            return

        # Patch all supported libraries
        patch_all()

        # Configure tracer
        tracer.configure(
            hostname="localhost",
            port=8126,
        )

        # Set global tags
        tracer.set_tags(
            {
                "service": self.service_name,
                "env": self.env,
                "version": self.version,
            }
        )

        # Initialize LLM Observability if enabled
        if self.llm_obs_enabled and self.api_key:
            try:
                LLMObs.enable(
                    ml_app=self.service_name,
                    api_key=self.api_key,
                    site="datadoghq.com",
                    env=self.env,
                )
                print("✅ Datadog LLM Observability enabled")
            except Exception as e:
                print(f"⚠️  Failed to enable LLM Observability: {e}")

        print(f"✅ Datadog APM initialized: {self.service_name} ({self.env})")

    def get_metrics_api(self) -> Optional[MetricsApi]:
        """Get Datadog Metrics API client"""
        if not self.api_key:
            return None

        configuration = Configuration()
        configuration.api_key["apiKeyAuth"] = self.api_key
        if self.app_key:
            configuration.api_key["appKeyAuth"] = self.app_key

        return MetricsApi(ApiClient(configuration))


# Global instance
datadog_config = DatadogConfig()


class DatadogMetrics:
    """Custom metrics for Oratio platform"""

    def __init__(self):
        self.metrics_api = datadog_config.get_metrics_api()
        self.service = datadog_config.service_name
        self.env = datadog_config.env

    def _send_metric(
        self,
        metric_name: str,
        value: float,
        metric_type: str = "gauge",
        tags: Optional[list] = None,
    ):
        """Send a custom metric to Datadog"""
        if not self.metrics_api:
            return

        try:
            series = Series(
                metric=f"oratio.{metric_name}",
                type=metric_type,
                points=[Point([int(time.time()), value])],
                tags=tags or [],
            )

            body = MetricsPayload(series=[series])
            self.metrics_api.submit_metrics(body=body)
        except Exception as e:
            print(f"⚠️  Failed to send metric {metric_name}: {e}")

    # Agent Metrics
    def agent_created(self, agent_id: str, user_id: str):
        """Track agent creation"""
        self._send_metric(
            "agent.created",
            1,
            metric_type="count",
            tags=[f"agent_id:{agent_id}", f"user_id:{user_id}", f"env:{self.env}"],
        )

    def agent_creation_time(self, duration_seconds: float, agent_id: str):
        """Track agent creation duration"""
        self._send_metric(
            "agent.creation.duration",
            duration_seconds,
            metric_type="gauge",
            tags=[f"agent_id:{agent_id}", f"env:{self.env}"],
        )

    def agent_invocation(self, agent_id: str, session_id: str, mode: str):
        """Track agent invocation (text or voice)"""
        self._send_metric(
            "agent.invocation",
            1,
            metric_type="count",
            tags=[
                f"agent_id:{agent_id}",
                f"session_id:{session_id}",
                f"mode:{mode}",
                f"env:{self.env}",
            ],
        )

    # LLM Metrics
    def llm_request(
        self, model: str, tokens: int, duration_ms: float, success: bool
    ):
        """Track LLM request"""
        self._send_metric(
            "llm.request",
            1,
            metric_type="count",
            tags=[
                f"model:{model}",
                f"success:{success}",
                f"env:{self.env}",
            ],
        )

        self._send_metric(
            "llm.tokens",
            tokens,
            metric_type="gauge",
            tags=[f"model:{model}", f"env:{self.env}"],
        )

        self._send_metric(
            "llm.duration",
            duration_ms,
            metric_type="gauge",
            tags=[f"model:{model}", f"env:{self.env}"],
        )

    # Voice Metrics
    def voice_session_started(self, agent_id: str, session_id: str, provider: str):
        """Track voice session start"""
        self._send_metric(
            "voice.session.started",
            1,
            metric_type="count",
            tags=[
                f"agent_id:{agent_id}",
                f"session_id:{session_id}",
                f"provider:{provider}",
                f"env:{self.env}",
            ],
        )

    def voice_session_ended(
        self, agent_id: str, session_id: str, duration_seconds: float, provider: str
    ):
        """Track voice session end"""
        self._send_metric(
            "voice.session.ended",
            1,
            metric_type="count",
            tags=[
                f"agent_id:{agent_id}",
                f"session_id:{session_id}",
                f"provider:{provider}",
                f"env:{self.env}",
            ],
        )

        self._send_metric(
            "voice.session.duration",
            duration_seconds,
            metric_type="gauge",
            tags=[
                f"agent_id:{agent_id}",
                f"provider:{provider}",
                f"env:{self.env}",
            ],
        )

    def voice_provider_failover(self, from_provider: str, to_provider: str):
        """Track voice provider failover"""
        self._send_metric(
            "voice.failover",
            1,
            metric_type="count",
            tags=[
                f"from:{from_provider}",
                f"to:{to_provider}",
                f"env:{self.env}",
            ],
        )

    # Session Metrics
    def session_message(self, agent_id: str, session_id: str, mode: str):
        """Track session message"""
        self._send_metric(
            "session.message",
            1,
            metric_type="count",
            tags=[
                f"agent_id:{agent_id}",
                f"session_id:{session_id}",
                f"mode:{mode}",
                f"env:{self.env}",
            ],
        )

    # Error Metrics
    def error_occurred(self, error_type: str, component: str):
        """Track errors"""
        self._send_metric(
            "error.occurred",
            1,
            metric_type="count",
            tags=[
                f"error_type:{error_type}",
                f"component:{component}",
                f"env:{self.env}",
            ],
        )


# Global metrics instance
metrics = DatadogMetrics()


def trace_operation(operation_name: str, resource: Optional[str] = None):
    """Decorator to trace operations with Datadog"""

    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            with tracer.trace(
                operation_name,
                service=datadog_config.service_name,
                resource=resource or func.__name__,
            ) as span:
                try:
                    result = await func(*args, **kwargs)
                    span.set_tag("success", True)
                    return result
                except Exception as e:
                    span.set_tag("success", False)
                    span.set_tag("error.type", type(e).__name__)
                    span.set_tag("error.message", str(e))
                    raise

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            with tracer.trace(
                operation_name,
                service=datadog_config.service_name,
                resource=resource or func.__name__,
            ) as span:
                try:
                    result = func(*args, **kwargs)
                    span.set_tag("success", True)
                    return result
                except Exception as e:
                    span.set_tag("success", False)
                    span.set_tag("error.type", type(e).__name__)
                    span.set_tag("error.message", str(e))
                    raise

        # Return appropriate wrapper based on function type
        import asyncio

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator


def track_llm_operation(model: str):
    """Decorator to track LLM operations"""

    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            success = False
            tokens = 0

            try:
                result = await func(*args, **kwargs)
                success = True

                # Try to extract token count from result
                if isinstance(result, dict):
                    tokens = result.get("usage", {}).get("total_tokens", 0)

                return result
            finally:
                duration_ms = (time.time() - start_time) * 1000
                metrics.llm_request(model, tokens, duration_ms, success)

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            success = False
            tokens = 0

            try:
                result = func(*args, **kwargs)
                success = True

                # Try to extract token count from result
                if isinstance(result, dict):
                    tokens = result.get("usage", {}).get("total_tokens", 0)

                return result
            finally:
                duration_ms = (time.time() - start_time) * 1000
                metrics.llm_request(model, tokens, duration_ms, success)

        import asyncio

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator
