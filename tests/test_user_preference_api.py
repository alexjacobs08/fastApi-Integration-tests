import base64

from app.main import app
from app.db import get_mongodb


def test_get_user_preferences_404(client, mock_mongodb):
    # should return 404 since no user preferences exist
    app.dependency_overrides[get_mongodb] = mock_mongodb
    response = client.get("/users/me/preferences")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Preferences not found'}


def test_get_user_preferences_initialized(client, mock_mongodb_initialized):
    # we're using our mock_mongodb_initialized fixture here which has our user preferences already set
    app.dependency_overrides[get_mongodb] = mock_mongodb_initialized
    response = client.get("/users/me/preferences")
    assert response.status_code == 200
    assert response.json() == {'city': 'Berlin'}


def test_post_user_preferences(client, mock_mongodb):
    app.dependency_overrides[get_mongodb] = mock_mongodb
    response = client.post("/users/me/preferences", json={"city": "Berlin"})
    assert response.status_code == 200
    assert response.json() == {"detail": "success"}


def test_get_user_profile_pic_404(client):
    response = client.get("/users/me/profile_pic")
    assert response.status_code == 404
    assert response.json() == {'detail': 'No profile pic found'}


def test_set_user_profile_pic(client):
    with open('tests/assets/duck.png', 'rb') as f:
        response = client.post("/users/me/profile_pic", files={"picture": ("duck.png", f, "image/png")})

    assert response.status_code == 200
    assert response.json() == {'detail': 'success'}


def test_get_user_profile_pic(client):
    response = client.get("/users/me/profile_pic")
    assert response.status_code == 200
    with open('tests/assets/duck.png', 'rb') as f:
        original_image_data = f.read()
        original_base64 = base64.b64encode(original_image_data).decode('utf-8')

    assert response.json()['image'] == original_base64
