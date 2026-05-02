"""
Auth API routes: login, refresh, change password, me.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from gotrue.errors import AuthApiError

from app.core.security import sign_in_with_password, refresh_session, update_auth_password
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.auth import (
    LoginRequest, LoginResponse,
    RefreshRequest, RefreshResponse,
    ChangePasswordRequest,
)
from app.schemas.user import UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Sign in with email and password. Returns JWT tokens."""
    try:
        result = await sign_in_with_password(request.email, request.password)
        return result
    except AuthApiError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Login failed: {str(e)}",
        )


@router.post("/refresh", response_model=RefreshResponse)
async def refresh(request: RefreshRequest):
    """Refresh an expired access token."""
    try:
        result = await refresh_session(request.refresh_token)
        return result
    except AuthApiError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Refresh failed: {str(e)}",
        )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get the currently authenticated user's profile."""
    return current_user


@router.post("/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
):
    """Change the current user's password."""
    try:
        await update_auth_password(str(current_user.id), request.new_password)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to change password: {str(e)}",
        )
