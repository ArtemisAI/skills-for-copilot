# Database Patterns

Async SQLAlchemy patterns for FastAPI.

## Database Session

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Create engine
engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    echo=True,
    future=True
)

# Create session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency
async def get_db() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

## SQLAlchemy Models

```python
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

## Async Queries

```python
# Select
result = await db.execute(select(User).where(User.email == email))
user = result.scalar_one_or_none()

# Insert
db.add(new_user)
await db.flush()
await db.refresh(new_user)

# Update
await db.execute(
    update(User).where(User.id == id).values(name="New Name")
)

# Delete
await db.execute(delete(User).where(User.id == id))

# Commit
await db.commit()
```

## Transactions

```python
async with async_session() as session:
    async with session.begin():
        # Multiple operations in transaction
        db.add(user)
        db.add(profile)
        # Automatically commits or rolls back
```

See [complete-examples.md](complete-examples.md) for repository patterns.
