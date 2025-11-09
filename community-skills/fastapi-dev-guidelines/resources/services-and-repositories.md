# Services and Repositories

Separation of business logic (services) and data access (repositories).

## Service Layer

```python
class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(
        self,
        db: AsyncSession,
        user_data: UserCreate
    ) -> User:
        # Business logic: check email exists
        existing = await self.repository.find_by_email(db, user_data.email)
        if existing:
            raise HTTPException(400, "Email already registered")

        # Business logic: hash password
        hashed_password = hash_password(user_data.password)

        # Delegate to repository
        user = await self.repository.create(db, user_data, hashed_password)
        await db.commit()
        return user

    async def get_user(self, db: AsyncSession, user_id: int) -> User:
        user = await self.repository.find_by_id(db, user_id)
        if not user:
            raise HTTPException(404, "User not found")
        return user
```

## Repository Layer

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

    async def find_by_email(
        self,
        db: AsyncSession,
        email: str
    ) -> Optional[User]:
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def create(
        self,
        db: AsyncSession,
        user_data: UserCreate,
        hashed_password: str
    ) -> User:
        db_user = User(
            email=user_data.email,
            name=user_data.name,
            hashed_password=hashed_password
        )
        db.add(db_user)
        await db.flush()
        await db.refresh(db_user)
        return db_user

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
```

## Base Repository

```python
from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        result = await db.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def list(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        result = await db.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

# Usage
class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)
```

See [complete-examples.md](complete-examples.md) for full implementation.
