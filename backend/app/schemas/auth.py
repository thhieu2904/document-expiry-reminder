"""
Pydantic schemas for Auth API.
"""
from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Login with email and password."""
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Successful login response."""
    access_token: str
    refresh_token: str
    expires_in: int
    user: dict


class RefreshRequest(BaseModel):
    """Refresh token request."""
    refresh_token: str


class RefreshResponse(BaseModel):
    """Refreshed tokens response."""
    access_token: str
    refresh_token: str
    expires_in: int


class ChangePasswordRequest(BaseModel):
    """Change password request."""
    new_password: str
