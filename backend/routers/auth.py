"""Authentication API endpoints — MOCK VERSION for hackathon demo."""

from fastapi import APIRouter, status
from datetime import datetime, timedelta, timezone
import jwt
import logging

from models.user import (
    UserCreate,
    UserLogin,
    UserConfirm,
    TokenResponse,
    TokenRefresh,
    UserProfile,
)
from config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])

MOCK_USER = UserProfile(
    user_id="mock-user-123",
    email="mock@oratio.dev",
    name="Mock User",
    subscription_tier="free",
    created_at=int(datetime.now(timezone.utc).timestamp()),
)


def _make_mock_token(email: str = "mock@oratio.dev") -> str:
    payload = {
        "sub": "mock-user-123",
        "email": email,
        "name": "Mock User",
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def _token_response(email: str = "mock@oratio.dev") -> TokenResponse:
    token = _make_mock_token(email)
    return TokenResponse(
        access_token=token,
        id_token=token,
        refresh_token="mock-refresh-token",
        token_type="Bearer",
        expires_in=86400,
    )


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    return {
        "user_id": "mock-user-123",
        "email": user_data.email,
        "message": "User registered successfully. Please check your email for verification code.",
    }


@router.post("/confirm")
async def confirm_registration(confirm_data: UserConfirm):
    return {"message": "Email confirmed successfully. You can now log in."}


@router.post("/login", response_model=TokenResponse)
async def login(login_data: UserLogin):
    return _token_response(login_data.email)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(token_data: TokenRefresh):
    return _token_response()


@router.get("/me", response_model=UserProfile)
async def get_me():
    return MOCK_USER


@router.post("/change-password")
async def change_password():
    return {"message": "Password changed successfully."}


@router.post("/forgot-password")
async def forgot_password(email: str):
    return {"message": "If an account exists with this email, you will receive a password reset code."}


@router.post("/reset-password")
async def reset_password(email: str, confirmation_code: str, new_password: str):
    return {"message": "Password reset successfully. You can now log in with your new password."}


@router.post("/logout")
async def logout():
    return {"message": "Logged out successfully. Please remove tokens from client storage."}
