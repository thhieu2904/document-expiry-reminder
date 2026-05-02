import pytest
import uuid
from app.main import app
from app.core.deps import get_current_user, require_admin
from app.models.user import User

from datetime import datetime, timezone

# Mock user data
mock_admin_user = User(
    id=uuid.uuid4(),
    full_name="Admin Test",
    email="admin@test.com",
    role="admin",
    can_login=True,
    status="active",
    created_at=datetime.now(timezone.utc),
    updated_at=datetime.now(timezone.utc)
)

async def override_get_current_user():
    return mock_admin_user

async def override_require_admin():
    return mock_admin_user

app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[require_admin] = override_require_admin

@pytest.mark.asyncio
async def test_get_me(client):
    """Test getting current user profile with mocked auth."""
    response = await client.get("/api/auth/me")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "admin@test.com"
    assert data["role"] == "admin"
