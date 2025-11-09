# Error Handling

Exception handling patterns in FastAPI.

## HTTPException

```python
from fastapi import HTTPException, status

# Basic usage
if not user:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )

# With headers
raise HTTPException(
    status_code=401,
    detail="Not authenticated",
    headers={"WWW-Authenticate": "Bearer"}
)
```

## Custom Exceptions

```python
class ItemNotFoundException(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id

class DuplicateItemException(Exception):
    def __init__(self, message: str):
        self.message = message
```

## Exception Handlers

```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(ItemNotFoundException)
async def item_not_found_handler(
    request: Request,
    exc: ItemNotFoundException
):
    return JSONResponse(
        status_code=404,
        content={"detail": f"Item {exc.item_id} not found"}
    )

@app.exception_handler(DuplicateItemException)
async def duplicate_item_handler(
    request: Request,
    exc: DuplicateItemException
):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message}
    )
```

## Validation Errors

FastAPI automatically handles Pydantic validation errors:

```python
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )
```

## Error Response Model

```python
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None

@router.post(
    "",
    response_model=ItemResponse,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse}
    }
)
```

See [complete-examples.md](complete-examples.md) for service-level error handling.
