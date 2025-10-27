from starlette import status


def test_create_activity(client):
    response = client.post("/activities/", json={"name": "Test Activity"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Test Activity"
    assert "id" in data
    assert data["children"] == []


def test_get_activities(client):
    client.post("/activities/", json={"name": "Activity 1"})
    client.post("/activities/", json={"name": "Activity 2"})
    response = client.get("/activities/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_get_activity_by_id(client):
    response_create = client.post("/activities/", json={"name": "Single Activity"})
    activity_id = response_create.json()["id"]
    response = client.get(f"/activities/{activity_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == activity_id
    assert data["name"] == "Single Activity"


def test_update_activity(client):
    response_create = client.post("/activities/", json={"name": "Old Name"})
    activity_id = response_create.json()["id"]
    response = client.put(f"/activities/{activity_id}", json={"name": "New Name"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "New Name"


def test_delete_activity(client):
    response_create = client.post("/activities/", json={"name": "To Delete"})
    activity_id = response_create.json()["id"]
    response_delete = client.delete(f"/activities/{activity_id}")
    assert response_delete.status_code == status.HTTP_204_NO_CONTENT
    response_get = client.get(f"/activities/{activity_id}")
    assert response_get.status_code == status.HTTP_404_NOT_FOUND
