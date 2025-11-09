# Architecture Overview

## Layered Architecture

FastAPI applications follow a clean layered architecture with clear separation of concerns.

### Architecture Layers

```
┌─────────────────────────────────────┐
│         HTTP Request                │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│    Path Operations (Routers)        │
│  - Route definitions                │
│  - Request/response models          │
│  - Pydantic validation             │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│      Dependencies (Depends)         │
│  - Authentication                   │
│  - Database sessions                │
│  - Shared logic                     │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│      Services (Business Logic)      │
│  - Domain logic                     │
│  - Orchestration                    │
│  - Validation rules                 │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│    Repositories (Data Access)       │
│  - Database queries                 │
│  - CRUD operations                  │
│  - Data mapping                     │
└──────────────┬──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│        Database (SQLAlchemy)        │
│  - Models                           │
│  - Relationships                    │
│  - Migrations                       │
└─────────────────────────────────────┘
```

---

## Request Lifecycle

### 1. HTTP Request Arrives

```python
GET /api/v1/users/123
Headers: Authorization: Bearer <token>
```

### 2. Router Receives Request

```python
@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),  # Dependency
    db: AsyncSession = Depends(get_db),              # Dependency
    service: UserService = Depends(get_user_service) # Dependency
):
    return await service.get_user(db, user_id)
```

**Responsibilities:**
- Define route path and HTTP method
- Declare path/query/body parameters
- Specify response model (Pydantic)
- Inject dependencies
- Call service layer

### 3. Dependencies Execute

```python
# Authentication dependency
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    # Validate token
    # Fetch user from database
    return user

# Database session dependency
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
        await session.commit()
```

**Responsibilities:**
- Provide database sessions
- Handle authentication
- Validate permissions
- Inject shared resources

### 4. Service Processes Request

```python
class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def get_user(
        self,
        db: AsyncSession,
        user_id: int
    ) -> User:
        user = await self.repository.find_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User {user_id} not found"
            )
        return user
```

**Responsibilities:**
- Business logic
- Validation rules
- Error handling
- Orchestrate repository calls

### 5. Repository Accesses Data

```python
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
```

**Responsibilities:**
- Database queries
- Data access patterns
- Query optimization
- Return domain models

### 6. Response Returns

```python
{
    "id": 123,
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2025-01-01T00:00:00Z"
}
```

FastAPI automatically:
- Serializes with Pydantic
- Validates response schema
- Generates OpenAPI docs

---

## Separation of Concerns

### ✅ DO: Each Layer Has ONE Job

```python
# Router: Route and validate
@router.post("/users", response_model=UserResponse)
async def create_user(
    user_in: UserCreate,
    service: UserService = Depends()
):
    return await service.create(user_in)

# Service: Business logic
class UserService:
    async def create(self, user_data: UserCreate):
        # Validate business rules
        if await self.email_exists(user_data.email):
            raise ValueError("Email already exists")

        # Call repository
        return await self.repository.create(user_data)

# Repository: Data access
class UserRepository:
    async def create(self, user_data: UserCreate):
        db_user = User(**user_data.model_dump())
        db.add(db_user)
        await db.commit()
        return db_user
```

### ❌ DON'T: Mix Responsibilities

```python
# BAD: Everything in the router
@router.post("/users")
async def create_user(user_in: dict):
    # Validation in router - should be Pydantic
    if not user_in.get("email"):
        raise HTTPException(400, "Email required")

    # Business logic in router - should be service
    existing = await db.execute(...)
    if existing:
        raise HTTPException(400, "Email exists")

    # Database in router - should be repository
    db_user = User(**user_in)
    db.add(db_user)
    await db.commit()

    return db_user
```

---

## Project Structure

### Complete Directory Layout

```
my-fastapi-app/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py    # Aggregate router
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── users.py
│   │           ├── posts.py
│   │           └── auth.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # Settings (Pydantic)
│   │   ├── security.py      # Auth utilities
│   │   └── deps.py          # Dependencies
│   │
│   ├── models/              # SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── post.py
│   │
│   ├── schemas/             # Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── post.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── post_service.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── user_repository.py
│   │   └── post_repository.py
│   │
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py          # Base model
│   │   ├── session.py       # Database session
│   │   └── init_db.py       # Initialize database
│   │
│   └── tests/
│       ├── __init__.py
│       ├── conftest.py
│       ├── api/
│       │   └── test_users.py
│       └── services/
│           └── test_user_service.py
│
├── alembic/                 # Database migrations
│   ├── versions/
│   └── env.py
│
├── .env                     # Environment variables
├── alembic.ini
├── pyproject.toml
└── README.md
```

---

## Module Responsibilities

### `main.py` - Application Entry

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix=settings.API_V1_STR)
```

### `api/v1/router.py` - Aggregate Router

```python
from fastapi import APIRouter

from app.api.v1.endpoints import users, posts, auth

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
```

### `core/config.py` - Configuration

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "My FastAPI App"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
```

### `core/deps.py` - Dependencies

```python
from typing import Generator
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

def get_user_repository() -> UserRepository:
    return UserRepository()

def get_user_service(
    repository: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(repository)
```

---

## Design Principles

### 1. Dependency Injection Over Global State

```python
# ✅ GOOD: Injected dependencies
@router.get("/users/{user_id}")
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    return await service.get_user(user_id)

# ❌ BAD: Global service instance
user_service = UserService()  # Global

@router.get("/users/{user_id}")
async def get_user(user_id: int):
    return await user_service.get_user(user_id)
```

### 2. Async All The Way

```python
# ✅ GOOD: Async throughout
async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

# ❌ BAD: Mixing sync and async
async def get_user(db: Session, user_id: int):  # Sync Session
    return db.query(User).filter(User.id == user_id).first()  # Blocking!
```

### 3. Single Responsibility

Each module/class should have ONE reason to change.

```python
# ✅ GOOD: Separate concerns
class UserService:
    """Business logic only"""
    pass

class UserRepository:
    """Data access only"""
    pass

# ❌ BAD: Mixed responsibilities
class UserManager:
    """Does everything - business logic AND data access"""
    pass
```

---

## Summary

**Key Takeaways:**
1. **Layered architecture**: Routers → Dependencies → Services → Repositories → Database
2. **Separation of concerns**: Each layer has ONE job
3. **Dependency injection**: Use Depends() for all dependencies
4. **Async throughout**: async/await for all I/O operations
5. **Pydantic validation**: Request/response models
6. **Clear structure**: Organized directories by function

**See also:**
- [path-operations.md](path-operations.md) - Router patterns
- [dependency-injection.md](dependency-injection.md) - Depends() usage
- [services-and-repositories.md](services-and-repositories.md) - Business logic patterns
