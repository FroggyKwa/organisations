from fastapi import status


def test_create_building(client):
    payload = {"address": "ул. Ленина 1", "latitude": 55.75, "longitude": 37.62}
    response = client.post("/buildings/", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["address"] == payload["address"]
    assert data["latitude"] == payload["latitude"]
    assert data["longitude"] == payload["longitude"]
    assert "id" in data


def test_get_buildings(client):
    response = client.get("/buildings/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)


def test_get_building_by_id(client):
    payload = {"address": "ул. Тверская 10", "latitude": 55.76, "longitude": 37.62}
    create_resp = client.post("/buildings/", json=payload)
    building_id = create_resp.json()["id"]

    response = client.get(f"/buildings/{building_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == building_id
    assert data["address"] == payload["address"]


def test_update_building(client):
    payload = {"address": "ул. Арбат 5", "latitude": 55.75, "longitude": 37.61}
    create_resp = client.post("/buildings/", json=payload)
    building_id = create_resp.json()["id"]

    update_payload = {"address": "ул. Арбат 6", "latitude": 55.751, "longitude": 37.611}
    response = client.put(f"/buildings/{building_id}", json=update_payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["address"] == update_payload["address"]
    assert data["latitude"] == update_payload["latitude"]
    assert data["longitude"] == update_payload["longitude"]


def test_delete_building(client):
    payload = {"address": "ул. Пушкина 12", "latitude": 55.75, "longitude": 37.60}
    create_resp = client.post("/buildings/", json=payload)
    building_id = create_resp.json()["id"]

    response = client.delete(f"/buildings/{building_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    get_resp = client.get(f"/buildings/{building_id}")
    assert get_resp.status_code == status.HTTP_404_NOT_FOUND
