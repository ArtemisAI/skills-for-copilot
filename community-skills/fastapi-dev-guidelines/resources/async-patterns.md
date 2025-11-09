# Async Patterns

Async/await best practices and patterns for FastAPI.

## Async vs Sync

```python
# ✅ ALWAYS: Use async for I/O operations
@router.get("/users")
async def get_users(db: AsyncSession = Depends(get_db)):
    users = await user_repository.find_all(db)
    return users

# ❌ NEVER: Blocking I/O in async function
@router.get("/users")
async def get_users():
    users = requests.get("https://api.example.com/users")  # BLOCKS!
    return users.json()

# ✅ CORRECT: Use async HTTP client
import httpx

@router.get("/users")
async def get_users():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/users")
        return response.json()
```

## Background Tasks

```python
from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    # Send email (can be sync or async)
    pass

@router.post("/users")
async def create_user(
    user_in: UserCreate,
    background_tasks: BackgroundTasks
):
    user = await user_service.create(user_in)

    # Add background task
    background_tasks.add_task(send_email, user.email, "Welcome!")

    return user
```

## Concurrent Execution

```python
import asyncio

# Run multiple async operations concurrently
@router.get("/dashboard")
async def get_dashboard():
    # Execute in parallel
    users_task = asyncio.create_task(user_service.count())
    posts_task = asyncio.create_task(post_service.count())
    comments_task = asyncio.create_task(comment_service.count())

    # Wait for all to complete
    users_count = await users_task
    posts_count = await posts_task
    comments_count = await comments_task

    return {
        "users": users_count,
        "posts": posts_count,
        "comments": comments_count
    }

# Or use asyncio.gather
@router.get("/dashboard")
async def get_dashboard():
    results = await asyncio.gather(
        user_service.count(),
        post_service.count(),
        comment_service.count()
    )
    return {
        "users": results[0],
        "posts": results[1],
        "comments": results[2]
    }
```

## Async Context Managers

```python
async def process_file(file_path: str):
    async with aiofiles.open(file_path, 'r') as f:
        contents = await f.read()
        return contents

@router.post("/upload")
async def upload_file(file: UploadFile):
    async with aiofiles.open(f"./uploads/{file.filename}", "wb") as f:
        content = await file.read()
        await f.write(content)
    return {"filename": file.filename}
```

## Timeouts

```python
import asyncio

@router.get("/external-data")
async def get_external_data():
    try:
        async with asyncio.timeout(5):  # 5 second timeout
            data = await external_api.fetch_data()
            return data
    except asyncio.TimeoutError:
        raise HTTPException(408, "Request timeout")
```

## Error Handling in Async

```python
async def fetch_user(user_id: int):
    try:
        user = await user_repository.find_by_id(user_id)
        return user
    except Exception as e:
        logger.error(f"Error fetching user {user_id}: {e}")
        raise HTTPException(500, "Internal server error")
```

## Async Generators

```python
from typing import AsyncGenerator

async def fetch_items_stream() -> AsyncGenerator[Item, None]:
    async for item in db.stream(select(Item)):
        yield item

@router.get("/items/stream")
async def stream_items():
    async def generate():
        async for item in fetch_items_stream():
            yield f"{item.name}\n"

    return StreamingResponse(generate(), media_type="text/plain")
```
