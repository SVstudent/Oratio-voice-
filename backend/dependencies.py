"""Shared dependencies for FastAPI application — MOCK VERSION for hackathon demo."""

from typing import Annotated, Optional
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timezone
import logging

from models.user import UserProfile
from config import settings

logger = logging.getLogger(__name__)

# HTTP Bearer token scheme
security = HTTPBearer()

MOCK_USER = UserProfile(
    user_id="mock-user-123",
    email="mock@oratio.dev",
    name="Mock User",
    subscription_tier="free",
    created_at=int(datetime.now(timezone.utc).timestamp()),
)


async def get_current_user(
    credentials: Annotated[
        Optional[HTTPAuthorizationCredentials],
        Depends(HTTPBearer(auto_error=False))
    ] = None,
) -> UserProfile:
    """Always return mock user — bypasses JWT validation for hackathon demo."""
    return MOCK_USER


async def get_current_user_id(
    current_user: Annotated[UserProfile, Depends(get_current_user)]
) -> str:
    return current_user.user_id


async def get_current_user_optional(
    credentials: Annotated[
        Optional[HTTPAuthorizationCredentials],
        Depends(HTTPBearer(auto_error=False))
    ] = None,
) -> Optional[UserProfile]:
    """Always return mock user for optional auth."""
    return MOCK_USER


def get_user_id_from_token(token: str) -> str:
    return "mock-user-123"


# --- Service dependency stubs (other routers import these) ---

from services.agent_service import AgentService
from services.api_key_service import APIKeyService
from services.agent_invocation_service import AgentInvocationService
from aws.dynamodb_client import DynamoDBClient


def get_dynamodb_client() -> DynamoDBClient:
    return DynamoDBClient()


def get_agent_service(
    dynamodb_client: Annotated[DynamoDBClient, Depends(get_dynamodb_client)]
) -> AgentService:
    return AgentService(
        dynamodb_client=dynamodb_client,
        table_name=settings.AGENTS_TABLE,
    )


def get_api_key_service(
    dynamodb_client: Annotated[DynamoDBClient, Depends(get_dynamodb_client)]
) -> APIKeyService:
    return APIKeyService(
        dynamodb_client=dynamodb_client,
        table_name=settings.API_KEYS_TABLE,
    )


def get_agent_invocation_service() -> AgentInvocationService:
    return AgentInvocationService(region=settings.BEDROCK_REGION)
