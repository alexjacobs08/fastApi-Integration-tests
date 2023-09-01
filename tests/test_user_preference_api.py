
def test_get_user_preferences(client):
    response = client.get("/users/me/preferences")
    assert response.status_code == 200
    assert response.json() == {"city": "Amsterdam"}


def test_post_user_preferences(client, mock_s3_bucket):
    response = client.post("/users/me/preferences", json={"city": "Berlin"})
    assert response.status_code == 200
    assert response.json() == {"detail": "success"} 


def test_get_updated_user_preferences(client):
    response = client.get("/users/me/preferences")
    assert response.status_code == 200
    assert response.json() == {"city": "Berlin"}
