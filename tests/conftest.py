import pytest
from fastapi.testclient import TestClient
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette import status

from src.database import get_db
from src.dependencies import get_api_key
from src.models import Base
from src.main import app


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

API_KEY = "test_api_key"


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)

    connection = engine.connect()

    session = TestingSessionLocal(bind=connection)
    session.begin_nested()

    yield session

    session.close()
    connection.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def override_dependencies(db_session):
    async def _mock_get_api_key(
        api_key_header: str = Security(APIKeyHeader(name="X-API-Key", auto_error=False))
    ):
        if api_key_header == API_KEY:
            return api_key_header
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API Key",
        )

    def _get_db():
        yield db_session

    app.dependency_overrides[get_api_key] = _mock_get_api_key
    app.dependency_overrides[get_db] = _get_db

    yield

    app.dependency_overrides.clear()


@pytest.fixture
def client():
    return TestClient(app, headers={"X-API-Key": API_KEY})


@pytest.fixture
def test_building(client):
    payload = {"address": "Москва, Тверская 1", "latitude": 55.75, "longitude": 37.61}
    r = client.post("/buildings/", json=payload)
    assert r.status_code == 200
    return r.json()


@pytest.fixture
def test_activities(client):
    data = []
    for name in ["Парикмахерская", "Кофейня"]:
        r = client.post("/activities/", json={"name": name})
        assert r.status_code == 200
        data.append(r.json())
    return data


@pytest.fixture
def test_organization(client, test_building, test_activities):
    payload = {
        "name": "ООО Пример",
        "building_id": test_building["id"],
        "phones": [{"number": "8-999-111-22-33"}],
        "activity_ids": [a["id"] for a in test_activities],
    }
    r = client.post("/organizations/", json=payload)
    assert r.status_code == 200
    return r.json()
