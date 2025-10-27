import pytest
from fastapi import status


def test_create_organization(client, test_building, test_activities):
    payload = {
        "name": "ООО Рога и Копыта",
        "building_id": test_building["id"],
        "phones": [{"number": "8-923-666-13-13"}],
        "activity_ids": [a["id"] for a in test_activities],
    }
    response = client.post("/organizations/", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["building"]["id"] == payload["building_id"]
    assert len(data["phones"]) == 1
    assert len(data["activities"]) == len(payload["activity_ids"])


def test_get_organizations(client):
    response = client.get("/organizations/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_get_organization_by_id(client, test_organization):
    response = client.get(f"/organizations/{test_organization['id']}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == test_organization["id"]
    assert "building" in data
    assert "activities" in data


def test_update_organization_name(client, test_organization):
    new_name = "ООО Хвост и Копыто"
    response = client.put(
        f"/organizations/{test_organization['id']}",
        json={"name": new_name},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == new_name


def test_update_organization_activities(client, test_organization, test_activities):
    new_activities = [a["id"] for a in test_activities]
    response = client.put(
        f"/organizations/{test_organization['id']}",
        json={"activity_ids": new_activities},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    returned_ids = [a["id"] for a in data["activities"]]
    assert set(returned_ids) == set(new_activities)


def test_get_organizations_by_building(client, test_building):
    response = client.get(f"/organizations/by_building/{test_building['id']}")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_get_organizations_by_activity(client, test_activities):
    activity_id = test_activities[0]["id"]
    response = client.get(f"/organizations/by_activity/{activity_id}")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_get_organizations_by_name(client, test_organization):
    name = test_organization["name"]
    response = client.get(f"/organizations/by_name/{name}")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
    assert any(org["name"] == name for org in response.json())


def test_get_organizations_in_bbox(client):
    response = client.get(
        "/organizations/in_bbox/",
        params={
            "min_latitude": 55.0,
            "max_latitude": 56.0,
            "min_longitude": 37.0,
            "max_longitude": 38.0,
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_get_organizations_in_radius(client):
    response = client.get(
        "/organizations/in_radius/",
        params={"center_lat": 55.75, "center_lon": 37.61, "radius": 10},
    )
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_delete_organization(client, test_organization):
    org_id = test_organization["id"]
    response = client.delete(f"/organizations/{org_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    follow_up = client.get(f"/organizations/{org_id}")
    assert follow_up.status_code == status.HTTP_404_NOT_FOUND
