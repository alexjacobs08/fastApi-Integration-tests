import pytest

from app.auth import get_auth
from app.models import TokenData
from app.main import app


def test_login(client):
    response = client.post("/login", json={"username": "alexjacobs", "password": "secret"})
    assert response.status_code == 200
    assert "jwt" in response.json()


def test_get_me_patched_auth(client):
    # auth works without real jwt because we patched it in the client fixture
    response = client.get("/users/me", headers={"Authorization": "Bearer " + 'fake.jwt'})
    assert response.status_code == 200
    assert response.json() == {'username': 'alexjacobs', 'email': 'alex@example.com'}


def test_get_me_unpatched_auth(client_unpatched_auth):
    # auth fails without real jwt because we're using the unpatched client fixture
    response = client_unpatched_auth.get("/users/me", headers={"Authorization": "Bearer " + 'fake.jwt'})
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


def test_get_me_path_auth_in_fn(client_unpatched_auth):
    # auth works because we patch it in this test (not in the client fixture)
    def mock_get_auth():
        return TokenData(username="alexjacobs")
    app.dependency_overrides[get_auth] = mock_get_auth

    response = client_unpatched_auth.get("/users/me", headers={"Authorization": "Bearer " + 'fake.jwt'})
    assert response.status_code == 200
    # app.dependency_overrides.clear()


def test_get_me_patch_auth_with_fixture(client_unpatched_auth, mock_get_auth_factory):
    # auth works because we patch it with a fixture instead of in the client fixture
    # Note: the fixture is a factory function that returns a function because that's how we have to pass it in
    app.dependency_overrides[get_auth] = mock_get_auth_factory
    response = client_unpatched_auth.get("/users/me", headers={"Authorization": "Bearer " + 'fake.jwt'})
    assert response.status_code == 200
    # app.dependency_overrides.clear()

