# Pydantic Models

Pydantic models for request/response validation in FastAPI.

## Base Patterns

```python
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

# Base schema (shared fields)
class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(min_length=1, max_length=100)
    is_active: bool = True

# Create schema (input only)
class UserCreate(UserBase):
    password: str = Field(min_length=8)

# Update schema (all optional)
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None

# Response schema (output)
class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # For SQLAlchemy models
```

## Field Validation

```python
class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    price: float = Field(gt=0, description="Price must be positive")
    quantity: int = Field(ge=0, le=1000)
    tags: List[str] = Field(default_factory=list, max_items=10)

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()

    @validator('tags')
    def tags_must_be_unique(cls, v):
        if len(v) != len(set(v)):
            raise ValueError('Tags must be unique')
        return v
```

## Field Types

```python
from pydantic import EmailStr, HttpUrl, UUID4, constr
from enum import Enum

class Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class UserSchema(BaseModel):
    email: EmailStr  # Validated email
    website: HttpUrl  # Validated URL
    uuid: UUID4  # UUID validation
    status: Status  # Enum
    phone: constr(regex=r'^\+?1?\d{9,15}$')  # Regex validation
```

## Config Options

```python
class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        from_attributes = True  # ORM mode (SQLAlchemy)
        str_strip_whitespace = True
        validate_assignment = True
        arbitrary_types_allowed = True
```

See [complete-examples.md](complete-examples.md) for full schema patterns.
