# Testing Guide

Testing FastAPI applications with pytest.

## Test Setup

```python
# conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.core.deps import get_db

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
```

## API Tests

```python
def test_create_user(client):
    response = client.post(
        "/api/v1/users",
        json={"email": "test@example.com", "name": "Test", "password": "pass123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_get_user(client):
    # Create
    create_response = client.post("/api/v1/users", json={...})
    user_id = create_response.json()["id"]

    # Get
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200

def test_list_users(client):
    # Create multiple
    for i in range(3):
        client.post("/api/v1/users", json={...})

    # List
    response = client.get("/api/v1/users")
    assert len(response.json()) == 3
```

## Service Tests

```python
import pytest
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository

@pytest.fixture
def user_service():
    repository = UserRepository()
    return UserService(repository)

@pytest.mark.asyncio
async def test_create_user(user_service, db_session):
    user_data = UserCreate(
        email="test@example.com",
        name="Test User",
        password="password123"
    )
    user = await user_service.create_user(db_session, user_data)

    assert user.email == "test@example.com"
    assert user.id is not None

@pytest.mark.asyncio
async def test_get_user_not_found(user_service, db_session):
    with pytest.raises(HTTPException) as exc_info:
        await user_service.get_user(db_session, 9999)

    assert exc_info.value.status_code == 404
```

## Async Tests

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_async_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/users")

    assert response.status_code == 200
```

## Mocking

```python
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def mock_user_repository():
    repository = MagicMock(spec=UserRepository)
    repository.find_by_id = AsyncMock(return_value=User(id=1, email="test@example.com"))
    return repository

async def test_with_mock(mock_user_repository):
    service = UserService(mock_user_repository)
    user = await service.get_user(db_session, 1)

    assert user.email == "test@example.com"
    mock_user_repository.find_by_id.assert_called_once_with(db_session, 1)
```

## Fixtures

```python
@pytest.fixture
def sample_user():
    return User(
        id=1,
        email="test@example.com",
        name="Test User",
        is_active=True
    )

@pytest.fixture
async def created_user(client):
    response = client.post("/api/v1/users", json={...})
    return response.json()

def test_with_fixture(created_user):
    assert created_user["id"] is not None
```

See [complete-examples.md](complete-examples.md) for full test suite.
