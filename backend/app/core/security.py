"""
Supabase Auth integration for JWT verification.
Uses supabase-py client to verify tokens from Supabase Auth.
"""
from supabase import create_client, Client
from gotrue.errors import AuthApiError

from app.core.config import settings

# Supabase client with service role key (for admin operations)
supabase_admin: Client = create_client(
    settings.supabase_url,
    settings.supabase_service_role_key,
)

# Supabase client with anon key (for auth operations)
supabase_client: Client = create_client(
    settings.supabase_url,
    settings.supabase_anon_key,
)


async def verify_token(access_token: str) -> dict | None:
    """
    Verify a Supabase Auth JWT token and return the user data.

    Returns:
        dict with user info if valid, None if invalid.
    """
    try:
        response = supabase_admin.auth.get_user(access_token)
        if response and response.user:
            return {
                "id": response.user.id,
                "email": response.user.email,
                "role": response.user.role,
            }
        return None
    except AuthApiError:
        return None
    except Exception:
        return None


async def sign_in_with_password(email: str, password: str) -> dict:
    """
    Sign in a user with email and password via Supabase Auth.

    Returns:
        dict with access_token, refresh_token, user info.
    Raises:
        AuthApiError if credentials are invalid.
    """
    response = supabase_client.auth.sign_in_with_password({
        "email": email,
        "password": password,
    })
    return {
        "access_token": response.session.access_token,
        "refresh_token": response.session.refresh_token,
        "expires_in": response.session.expires_in,
        "user": {
            "id": response.user.id,
            "email": response.user.email,
        },
    }


async def refresh_session(refresh_token: str) -> dict:
    """
    Refresh an expired access token.

    Returns:
        dict with new access_token, refresh_token.
    """
    response = supabase_client.auth.refresh_session(refresh_token)
    return {
        "access_token": response.session.access_token,
        "refresh_token": response.session.refresh_token,
        "expires_in": response.session.expires_in,
    }


async def create_auth_user(email: str, password: str) -> dict:
    """
    Create a new user in Supabase Auth (admin operation).

    Returns:
        dict with user id and email.
    """
    response = supabase_admin.auth.admin.create_user({
        "email": email,
        "password": password,
        "email_confirm": True,  # Auto-confirm email for internal system
    })
    return {
        "id": response.user.id,
        "email": response.user.email,
    }


async def update_auth_password(user_id: str, new_password: str) -> None:
    """Update a user's password in Supabase Auth (admin operation)."""
    supabase_admin.auth.admin.update_user_by_id(
        user_id,
        {"password": new_password},
    )
