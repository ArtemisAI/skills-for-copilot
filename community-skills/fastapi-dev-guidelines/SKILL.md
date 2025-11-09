---
name: fastapi-dev-guidelines
description: Comprehensive FastAPI/Python backend development guide. Use when creating path operations, Pydantic models, dependency injection, async services, database access, error handling, or working with FastAPI APIs. Covers layered architecture (routers → services → repositories), async/await patterns, Pydantic validation, SQLAlchemy integration, and best practices.
---

# FastAPI Development Guidelines

## Purpose

Establish consistency and best practices for FastAPI backend services using modern Python async patterns, Pydantic validation, and dependency injection.

## When to Use This Skill

Automatically activates when working on:
- Creating or modifying FastAPI routes/endpoints
- Building path operations with decorators
- Implementing Pydantic models for validation
- Dependency injection with Depends()
- Database operations with SQLAlchemy
- Async services and repositories
- Error handling and custom exceptions
- Background tasks and async patterns
- API testing with pytest

---

## Quick Start

### New API Feature Checklist

- [ ] **Router**: APIRouter with prefix and tags
- [ ] **Path Operation**: Async function with decorators
- [ ] **Pydantic Models**: Request/response schemas
- [ ] **Service**: Business logic with async/await
- [ ] **Repository**: Database access (if needed)
- [ ] **Dependencies**: Use Depends() for injection
- [ ] **Error Handling**: HTTPException or custom errors
- [ ] **Tests**: pytest with TestClient
- [ ] **Docs**: Docstrings for OpenAPI

### New FastAPI Service Checklist

- [ ] Directory structure (see Quick Reference)
- [ ] Pydantic Settings for config
- [ ] Database connection (async SQLAlchemy)
- [ ] Base repository class
- [ ] Error handlers
- [ ] CORS middleware
- [ ] Testing framework (pytest + httpx)
- [ ] OpenAPI customization

---

## Architecture Overview

### Layered Architecture

```
HTTP Request
    ↓
Router (routing + validation)
    ↓
Dependencies (auth, db session)
    ↓
Services (business logic)
    ↓
Repositories (data access)
    ↓
Database (SQLAlchemy)
```

**Key Principle:** Each layer has ONE responsibility.

See [resources/architecture-overview.md](resources/architecture-overview.md) for complete details.

---

## Directory Structure

```
app/
├── api/
│   ├── v1/
│   │   ├── endpoints/       # Path operation routers
│   │   │   ├── users.py
│   │   │   └── posts.py
│   │   └── router.py        # Aggregate router
├── core/
│   ├── config.py            # Pydantic Settings
│   ├── security.py          # Auth utilities
│   └── deps.py              # Dependencies
├── models/                  # SQLAlchemy models
│   ├── user.py
│   └── post.py
├── schemas/                 # Pydantic schemas
│   ├── user.py
│   └── post.py
├── services/                # Business logic
│   ├── user_service.py
│   └── post_service.py
├── repositories/            # Data access
│   ├── base.py
│   ├── user_repository.py
│   └── post_repository.py
├── db/
│   ├── base.py              # Database session
│   └── init_db.py
├── tests/
│   ├── api/
│   ├── services/
│   └── conftest.py
├── main.py                  # FastAPI app
└── __init__.py
```

**Naming Conventions:**
- Routers: `snake_case + .py` - `users.py`, `posts.py`
- Services: `snake_case + _service.py` - `user_service.py`
- Repositories: `snake_case + _repository.py` - `user_repository.py`
- Models: `PascalCase` classes - `User`, `Post`
- Schemas: `PascalCase` classes - `UserCreate`, `UserResponse`

---

## Core Principles (7 Key Rules)

### 1. Routers Only Route, Services Handle Logic

```python
# ❌ NEVER: Business logic in routers
@router.post("/users")
async def create_user(data: dict):
    # 100 lines of validation and logic
    pass

# ✅ ALWAYS: Delegate to service
@router.post("/users", response_model=UserResponse)
async def create_user(
    user_in: UserCreate,
    service: UserService = Depends(get_user_service)
):
    return await service.create_user(user_in)
```

### 2. Use Pydantic for ALL Validation

```python
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    name: str = Field(min_length=1, max_length=100)

    class Config:
        from_attributes = True
```

### 3. Dependency Injection with Depends()

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Dependency
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

# Usage
@router.get("/users/{user_id}")
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    pass
```

### 4. Always Use Async/Await

```python
# ✅ ALWAYS: Async path operations
@router.get("/users")
async def get_users(
    db: AsyncSession = Depends(get_db)
):
    users = await user_service.get_all(db)
    return users

# ✅ ALWAYS: Async services
class UserService:
    async def get_all(self, db: AsyncSession):
        return await user_repository.find_all(db)
```

### 5. HTTPException for Error Handling

```python
from fastapi import HTTPException, status

# In service
if not user:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )

# Custom exception handler
@app.exception_handler(CustomException)
async def custom_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
```

### 6. Repository Pattern for Database Access

```python
# Service → Repository → Database
class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self, user_data: UserCreate):
        return await self.repository.create(user_data)

class UserRepository:
    async def create(self, user_data: UserCreate):
        db_user = User(**user_data.model_dump())
        # ... database operations
```

### 7. Comprehensive Testing with pytest

```python
from fastapi.testclient import TestClient

def test_create_user(client: TestClient):
    response = client.post(
        "/api/v1/users",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
```

---

## Common Imports

```python
# FastAPI
from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi import Query, Path, Body, Header, Cookie
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Pydantic
from pydantic import BaseModel, Field, EmailStr, validator
from pydantic_settings import BaseSettings

# SQLAlchemy (Async)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import select, update, delete

# Typing
from typing import Optional, List, Dict, Any
from datetime import datetime

# Testing
import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
```

---

## Quick Reference

### HTTP Status Codes

| Code | Use Case | FastAPI Constant |
|------|----------|------------------|
| 200 | Success | `status.HTTP_200_OK` |
| 201 | Created | `status.HTTP_201_CREATED` |
| 204 | No Content | `status.HTTP_204_NO_CONTENT` |
| 400 | Bad Request | `status.HTTP_400_BAD_REQUEST` |
| 401 | Unauthorized | `status.HTTP_401_UNAUTHORIZED` |
| 403 | Forbidden | `status.HTTP_403_FORBIDDEN` |
| 404 | Not Found | `status.HTTP_404_NOT_FOUND` |
| 422 | Validation Error | `status.HTTP_422_UNPROCESSABLE_ENTITY` |
| 500 | Server Error | `status.HTTP_500_INTERNAL_SERVER_ERROR` |

### Path Operation Decorators

```python
@router.get("/items")           # GET request
@router.post("/items")          # POST request
@router.put("/items/{id}")      # PUT request (full update)
@router.patch("/items/{id}")    # PATCH request (partial update)
@router.delete("/items/{id}")   # DELETE request
```

---

## Anti-Patterns to Avoid

❌ Synchronous (blocking) operations in async functions
❌ Business logic in path operations
❌ Direct database queries in routers
❌ Missing Pydantic validation
❌ Using `dict` instead of Pydantic models
❌ Blocking I/O without async
❌ Missing type hints
❌ No error handling

---

## Navigation Guide

| Need to... | Read this |
|------------|-----------|
| Understand architecture | [architecture-overview.md](resources/architecture-overview.md) |
| Create path operations | [path-operations.md](resources/path-operations.md) |
| Define Pydantic models | [pydantic-models.md](resources/pydantic-models.md) |
| Use dependency injection | [dependency-injection.md](resources/dependency-injection.md) |
| Organize services/repos | [services-and-repositories.md](resources/services-and-repositories.md) |
| Database integration | [database-patterns.md](resources/database-patterns.md) |
| Handle errors | [error-handling.md](resources/error-handling.md) |
| Add middleware/CORS | [middleware-and-cors.md](resources/middleware-and-cors.md) |
| Async patterns | [async-patterns.md](resources/async-patterns.md) |
| Write tests | [testing-guide.md](resources/testing-guide.md) |
| See examples | [complete-examples.md](resources/complete-examples.md) |

---

## Resource Files

### [architecture-overview.md](resources/architecture-overview.md)
Layered architecture, request lifecycle, separation of concerns

### [path-operations.md](resources/path-operations.md)
Router setup, decorators, path/query parameters, response models

### [pydantic-models.md](resources/pydantic-models.md)
Request/response schemas, validation, field types, config

### [dependency-injection.md](resources/dependency-injection.md)
Depends(), custom dependencies, database sessions, auth

### [services-and-repositories.md](resources/services-and-repositories.md)
Service layer patterns, repository pattern, separation of concerns

### [database-patterns.md](resources/database-patterns.md)
Async SQLAlchemy, models, sessions, transactions, repositories

### [error-handling.md](resources/error-handling.md)
HTTPException, custom exceptions, exception handlers, validation errors

### [middleware-and-cors.md](resources/middleware-and-cors.md)
Middleware, CORS configuration, request/response processing

### [async-patterns.md](resources/async-patterns.md)
Async/await best practices, background tasks, concurrency

### [testing-guide.md](resources/testing-guide.md)
pytest, TestClient, fixtures, mocking, async tests

### [complete-examples.md](resources/complete-examples.md)
Full API examples, CRUD operations, real-world patterns

---

## Modern FastAPI Template (Quick Copy)

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService
from app.core.deps import get_db, get_user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    service: UserService = Depends(get_user_service),
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """Create a new user."""
    user = await service.create_user(db, user_in)
    return user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """Get user by ID."""
    user = await service.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return user

@router.get("", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    service: UserService = Depends(get_user_service),
    db: AsyncSession = Depends(get_db)
) -> List[UserResponse]:
    """List all users with pagination."""
    users = await service.list_users(db, skip=skip, limit=limit)
    return users
```

---

## Related Skills

- **error-tracking**: Sentry integration for FastAPI
- **skill-developer**: Meta-skill for creating and managing skills

---

**Skill Status**: COMPLETE ✅
**Line Count**: < 500 ✅
**Progressive Disclosure**: 11 resource files ✅
