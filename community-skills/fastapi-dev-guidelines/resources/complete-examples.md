# Complete FastAPI Examples

Full working examples demonstrating FastAPI best practices with async patterns, Pydantic validation, dependency injection, and layered architecture.

---

## Example 1: Complete CRUD API

### Pydantic Schemas (`schemas/user.py`)

```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)
    is_active: bool = True

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### SQLAlchemy Model (`models/user.py`)

```python
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

### Repository (`repositories/user_repository.py`)

```python
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.sql import func

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

class UserRepository:
    async def find_by_id(
        self,
        db: AsyncSession,
        user_id: int
    ) -> Optional[User]:
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def find_by_email(
        self,
        db: AsyncSession,
        email: str
    ) -> Optional[User]:
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def find_all(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        result = await db.execute(
            select(User).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def create(
        self,
        db: AsyncSession,
        user_data: UserCreate,
        hashed_password: str
    ) -> User:
        db_user = User(
            email=user_data.email,
            name=user_data.name,
            hashed_password=hashed_password,
            is_active=user_data.is_active
        )
        db.add(db_user)
        await db.flush()
        await db.refresh(db_user)
        return db_user

    async def update(
        self,
        db: AsyncSession,
        user_id: int,
        user_data: UserUpdate
    ) -> Optional[User]:
        await db.execute(
            update(User)
            .where(User.id == user_id)
            .values(**user_data.model_dump(exclude_unset=True))
        )
        return await self.find_by_id(db, user_id)

    async def delete(
        self,
        db: AsyncSession,
        user_id: int
    ) -> bool:
        result = await db.execute(
            delete(User).where(User.id == user_id)
        )
        return result.rowcount > 0

    async def count(self, db: AsyncSession) -> int:
        result = await db.execute(select(func.count(User.id)))
        return result.scalar_one()
```

### Service (`services/user_service.py`)

```python
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def _hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    async def create_user(
        self,
        db: AsyncSession,
        user_data: UserCreate
    ) -> User:
        # Check if email exists
        existing_user = await self.repository.find_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Hash password
        hashed_password = self._hash_password(user_data.password)

        # Create user
        user = await self.repository.create(db, user_data, hashed_password)
        await db.commit()
        return user

    async def get_user(
        self,
        db: AsyncSession,
        user_id: int
    ) -> User:
        user = await self.repository.find_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        return user

    async def list_users(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        return await self.repository.find_all(db, skip, limit)

    async def update_user(
        self,
        db: AsyncSession,
        user_id: int,
        user_data: UserUpdate
    ) -> User:
        # Check user exists
        await self.get_user(db, user_id)

        # Check email uniqueness if updating email
        if user_data.email:
            existing = await self.repository.find_by_email(db, user_data.email)
            if existing and existing.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already in use"
                )

        # Update
        user = await self.repository.update(db, user_id, user_data)
        await db.commit()
        return user

    async def delete_user(
        self,
        db: AsyncSession,
        user_id: int
    ) -> None:
        # Check user exists
        await self.get_user(db, user_id)

        # Delete
        deleted = await self.repository.delete(db, user_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete user"
            )
        await db.commit()
```

### Router (`api/v1/endpoints/users.py`)

```python
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.user_service import UserService
from app.core.deps import get_db, get_user_service

router = APIRouter()

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
    service: UserService = Depends(get_user_service)
) -> UserResponse:
    """Create a new user."""
    user = await service.create_user(db, user_in)
    return user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    service: UserService = Depends(get_user_service)
) -> UserResponse:
    """Get user by ID."""
    user = await service.get_user(db, user_id)
    return user

@router.get("", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    service: UserService = Depends(get_user_service)
) -> List[UserResponse]:
    """List all users with pagination."""
    users = await service.list_users(db, skip, limit)
    return users

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db),
    service: UserService = Depends(get_user_service)
) -> UserResponse:
    """Update user by ID."""
    user = await service.update_user(db, user_id, user_in)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    service: UserService = Depends(get_user_service)
) -> None:
    """Delete user by ID."""
    await service.delete_user(db, user_id)
```

---

## Example 2: Database Setup

### Database Configuration (`db/session.py`)

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.core.config import settings

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True
)

# Create async session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Base class for models
Base = declarative_base()

# Dependency
async def get_db() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

---

## Example 3: Authentication

### Security Utilities (`core/security.py`)

```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt
```

### Authentication Dependency (`core/deps.py`)

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    repository = UserRepository()
    user = await repository.find_by_id(db, int(user_id))

    if user is None:
        raise credentials_exception

    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user
```

### Auth Router (`api/v1/endpoints/auth.py`)

```python
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.core.deps import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.auth import Token

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """Login endpoint."""
    repository = UserRepository()
    user = await repository.find_by_email(db, form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
```

---

## Example 4: Testing

### Test Configuration (`tests/conftest.py`)

```python
import pytest
import asyncio
from typing import Generator, AsyncGenerator
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.core.deps import get_db

# Test database URL
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Create test engine
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)

# Create test session factory
test_async_session = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Create session
    async with test_async_session() as session:
        yield session

    # Drop tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="function")
def client(db_session: AsyncSession) -> Generator:
    # Override dependency
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
```

### API Tests (`tests/api/test_users.py`)

```python
import pytest
from fastapi.testclient import TestClient

def test_create_user(client: TestClient):
    response = client.post(
        "/api/v1/users",
        json={
            "email": "test@example.com",
            "name": "Test User",
            "password": "password123"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert "id" in data

def test_get_user(client: TestClient):
    # Create user
    create_response = client.post(
        "/api/v1/users",
        json={
            "email": "test@example.com",
            "name": "Test User",
            "password": "password123"
        }
    )
    user_id = create_response.json()["id"]

    # Get user
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == "test@example.com"

def test_get_user_not_found(client: TestClient):
    response = client.get("/api/v1/users/9999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

def test_list_users(client: TestClient):
    # Create multiple users
    for i in range(3):
        client.post(
            "/api/v1/users",
            json={
                "email": f"user{i}@example.com",
                "name": f"User {i}",
                "password": "password123"
            }
        )

    # List users
    response = client.get("/api/v1/users")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

def test_update_user(client: TestClient):
    # Create user
    create_response = client.post(
        "/api/v1/users",
        json={
            "email": "test@example.com",
            "name": "Test User",
            "password": "password123"
        }
    )
    user_id = create_response.json()["id"]

    # Update user
    response = client.put(
        f"/api/v1/users/{user_id}",
        json={"name": "Updated Name"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"

def test_delete_user(client: TestClient):
    # Create user
    create_response = client.post(
        "/api/v1/users",
        json={
            "email": "test@example.com",
            "name": "Test User",
            "password": "password123"
        }
    )
    user_id = create_response.json()["id"]

    # Delete user
    response = client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 204

    # Verify deleted
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 404
```

---

## Summary

**Key Takeaways:**
1. **Layered architecture**: Routers → Services → Repositories
2. **Pydantic everywhere**: Request/response validation
3. **Async throughout**: All I/O operations use async/await
4. **Dependency injection**: Services and database sessions
5. **Comprehensive testing**: Unit and integration tests
6. **Type safety**: Full type hints

**See also:**
- [architecture-overview.md](architecture-overview.md) - Architecture patterns
- [path-operations.md](path-operations.md) - Router details
- [pydantic-models.md](pydantic-models.md) - Schema patterns
- [testing-guide.md](testing-guide.md) - Testing strategies
