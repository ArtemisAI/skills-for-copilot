# Path Operations

Path operations (routes) in FastAPI using decorators and automatic validation.

## Basic Path Operation

```python
from fastapi import APIRouter, Depends, Query
from typing import List

router = APIRouter(prefix="/items", tags=["items"])

@router.get("", response_model=List[ItemResponse])
async def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    db: AsyncSession = Depends(get_db)
):
    """List items with pagination."""
    items = await item_service.list_items(db, skip, limit)
    return items
```

## Path Parameters

```python
@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: int,  # Path parameter
    db: AsyncSession = Depends(get_db)
):
    """Get item by ID."""
    return await item_service.get_item(db, item_id)
```

## Query Parameters

```python
@router.get("", response_model=List[ItemResponse])
async def search_items(
    q: str = Query(None, min_length=3),  # Optional
    category: str = Query(...),  # Required
    limit: int = Query(10, le=100)  # With default
):
    """Search items."""
    return await item_service.search(q, category, limit)
```

## Request Body

```python
@router.post("", response_model=ItemResponse)
async def create_item(
    item_in: ItemCreate,  # Request body (Pydantic model)
    db: AsyncSession = Depends(get_db)
):
    """Create new item."""
    return await item_service.create(db, item_in)
```

## Response Models

```python
@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    # FastAPI automatically validates response matches ItemResponse
    return item

# Multiple response models
@router.post("", response_model=ItemResponse, status_code=201)
@router.post("", responses={400: {"model": ErrorResponse}})
```

## Status Codes

```python
from fastapi import status

@router.post("", status_code=status.HTTP_201_CREATED)
@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
@router.patch("", status_code=status.HTTP_200_OK)
```

See [complete-examples.md](complete-examples.md) for full CRUD examples.
