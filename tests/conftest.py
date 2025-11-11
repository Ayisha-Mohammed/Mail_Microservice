
import pytest
from fastapi.testclient import TestClient
from app.main import app
from types import SimpleNamespace
from app.routes import email

# -----------------------------
# Fixture: TestClient for logged-in user
# -----------------------------
@pytest.fixture()
def client_logged_in():
    """
    TestClient with a fake logged-in user.
    Overrides the get_current_user dependency.
    """
    def fake_get_current_user():
        return SimpleNamespace(id=1, email="tester@example.com")

    app.dependency_overrides[email.get_current_user] = fake_get_current_user

    with TestClient(app) as c:
        yield c

    # Clear overrides after test
    app.dependency_overrides = {}

# -----------------------------
# Fixture: TestClient without auth (for 401 test)
# -----------------------------
@pytest.fixture()
def client_unauthorized():
    """
    TestClient with NO overrides. Used to test 401 Unauthorized.
    """
    app.dependency_overrides = {}  # ensure no overrides

    with TestClient(app) as c:
        yield c
