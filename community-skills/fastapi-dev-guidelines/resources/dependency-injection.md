# Dependency Injection

FastAPI's dependency injection system using `Depends()`.

## Basic Dependency

```python
from fastapi import Depends

# Define dependency
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

# Use dependency
@router.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    # db is automatically injected
    return await user_service.get_all(db)
```

## Service Dependencies

```python
# Service dependency
def get_user_service(
    repository: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(repository)

# Usage
@router.post("/users")
async def create_user(
    user_in: UserCreate,
    service: UserService = Depends(get_user_service),
    db: AsyncSession = Depends(get_db)
):
    return await service.create(db, user_in)
```

## Authentication Dependency

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    # Validate token and return user
    user = await validate_token(token, db)
    if not user:
        raise HTTPException(401, "Invalid credentials")
    return user

# Usage
@router.get("/me")
async def read_users_me(
    current_user: User = Depends(get_current_user)
):
    return current_user
```

## Class-Based Dependencies

```python
class CommonQueryParams:
    def __init__(
        self,
        skip: int = Query(0, ge=0),
        limit: int = Query(100, le=100)
    ):
        self.skip = skip
        self.limit = limit

@router.get("/items")
async def read_items(
    commons: CommonQueryParams = Depends()
):
    return await get_items(commons.skip, commons.limit)
```

See [complete-examples.md](complete-examples.md) for full authentication example.
