# FastAPI Framework Reference

> Source: Context7 — FastAPI official documentation
> Libraries: /websites/fastapi_tiangolo, /fastapi/fastapi

---

## Path Operations

### GET Decorator — Full Parameters

The `@app.get()` decorator supports comprehensive configuration:

- **response_model**: Pydantic model for serialization, filtering, and validation
- **status_code**: Default HTTP status code
- **tags**: List of tags for OpenAPI grouping
- **dependencies**: List of `Depends()` for the operation
- **summary / description**: OpenAPI documentation
- **response_description**: Description for the default response
- **responses**: Additional response schemas
- **deprecated**: Mark as deprecated in docs
- **response_class**: Custom response class (default: JSONResponse)
- **callbacks**: OpenAPI callback definitions
- **openapi_extra**: Extra OpenAPI schema metadata

### POST with APIRouter and Pydantic

```python
from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None

app = FastAPI()
router = APIRouter()

@router.post("/items/")
def create_item(item: Item):
    return {"message": "Item created"}

app.include_router(router)
```

---

## Dependency Injection

### Basic Dependencies

```python
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()

async def common_parameters(
    q: str | None = None,
    skip: int = 0,
    limit: int = 100,
):
    return {"q": q, "skip": skip, "limit": limit}

CommonDeps = Annotated[dict, Depends(common_parameters)]

@app.get("/items/")
async def read_items(commons: CommonDeps):
    return commons

@app.get("/users/")
async def read_users(commons: CommonDeps):
    return commons
```

### Class-Based Dependencies

```python
class Paginator:
    def __init__(self, skip: int = 0, limit: int = 100):
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def read_items(pagination: Annotated[Paginator, Depends()]):
    return {"skip": pagination.skip, "limit": pagination.limit}
```

### Dependencies in Path Operation Decorators

```python
async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

@app.get("/items/", dependencies=[Depends(verify_token)])
async def read_items():
    return [{"item": "Foo"}]
```

---

## Security: OAuth2 with JWT

### Full Setup

```python
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel, ValidationError
```

### JWT Token Validation with Scopes

```python
async def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        scope: str = payload.get("scope", "")
        token_scopes = scope.split(" ")
        token_data = TokenData(scopes=token_scopes, username=username)
    except (InvalidTokenError, ValidationError):
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user
```

---

## WebSockets

### WebSocket with Dependencies and Authentication

```python
from typing import Annotated
from fastapi import (
    Cookie, Depends, FastAPI, Query, WebSocket,
    WebSocketException, status,
)
from fastapi.responses import HTMLResponse

app = FastAPI()

async def get_cookie_or_token(
    websocket: WebSocket,
    session: Annotated[str | None, Cookie()] = None,
    token: Annotated[str | None, Query()] = None,
):
    if session is None and token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return session or token

@app.websocket("/items/{item_id}/ws")
async def websocket_endpoint(
    *,
    websocket: WebSocket,
    item_id: str,
    q: int | None = None,
    cookie_or_token: Annotated[str, Depends(get_cookie_or_token)],
):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(
            f"Session cookie or query token value is: {cookie_or_token}"
        )
        if q is not None:
            await websocket.send_text(f"Query parameter q is: {q}")
        await websocket.send_text(
            f"Message text was: {data}, for item ID: {item_id}"
        )
```

---

## Database: SQLAlchemy / SQLModel Integration

### Session Management with Dependency Injection

Session management uses dependency injection through `Depends()`. A `get_session()` generator function creates a new database session for each request using a context manager, ensuring proper resource cleanup.

```python
from typing import Annotated
from fastapi import Depends, FastAPI
from sqlmodel import Session, SQLModel, create_engine

engine = create_engine("sqlite:///database.db")

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.post("/heroes/")
def create_hero(hero: Hero, session: SessionDep):
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

@app.get("/heroes/")
def read_heroes(session: SessionDep, offset: int = 0, limit: int = 100):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes
```

---

## Pydantic Models and Validation

```python
from pydantic import BaseModel, Field, EmailStr, field_validator

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    age: int | None = Field(None, ge=0, le=150)

    @field_validator('username')
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        assert v.isalnum(), 'must be alphanumeric'
        return v

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = {"from_attributes": True}

# In route
@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate):
    # response_model filters out password
    db_user = create_db_user(user)
    return db_user
```

---

## Background Tasks

```python
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()

def write_notification(email: str, message: str = ""):
    with open("log.txt", mode="a") as f:
        f.write(f"notification for {email}: {message}\n")

@app.post("/send-notification/{email}")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}

# Background tasks in dependencies
def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)

async def get_query(background_tasks: BackgroundTasks, q: str | None = None):
    if q:
        background_tasks.add_task(write_log, f"Query: {q}\n")
    return q
```

---

## Middleware and CORS

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import time

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start
        response.headers["X-Process-Time"] = str(duration)
        return response

app.add_middleware(TimingMiddleware)

# Function-based middleware
@app.middleware("http")
async def add_custom_header(request, call_next):
    response = await call_next(request)
    response.headers["X-Custom"] = "value"
    return response
```

---

## Error Handling

```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

# Raise HTTP exceptions
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return items[item_id]

# Custom exception handler
class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something."},
    )

# Override validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )
```

---

## Lifespan Events

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Starting up...")
    db = await connect_to_db()
    app.state.db = db
    yield
    # Shutdown
    print("Shutting down...")
    await db.close()

app = FastAPI(lifespan=lifespan)
```

---

## Testing

```python
from fastapi.testclient import TestClient
from myapp import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_item():
    response = client.post(
        "/items/",
        json={"name": "Foo", "price": 42.0},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Foo"

def test_read_item_not_found():
    response = client.get("/items/999")
    assert response.status_code == 404

# Async testing with httpx
import pytest
from httpx import AsyncClient, ASGITransport

@pytest.mark.anyio
async def test_async():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        response = await ac.get("/")
    assert response.status_code == 200

# Override dependencies in tests
def override_get_db():
    return test_db_session

app.dependency_overrides[get_db] = override_get_db
```

---

## Advanced Features Summary

FastAPI provides:

- **Path/Query/Body parameters** with automatic validation from type hints
- **Dependency injection** system with `Depends()` for reusable logic
- **Security**: OAuth2 with JWT, HTTP Basic, API keys, cookie-based auth
- **Pydantic integration**: Request/response validation, serialization, filtering
- **Automatic OpenAPI docs**: Interactive `/docs` (Swagger UI) and `/redoc`
- **Background tasks**: Simple async task execution
- **WebSockets**: Full WebSocket support with dependency injection
- **Middleware**: Custom middleware, CORS, sessions, GZip
- **Database**: SQLAlchemy, SQLModel, async database support
- **Testing**: TestClient (sync) and httpx AsyncClient for async tests
- **Lifespan events**: Startup/shutdown via async context manager
- **GraphQL**: Integration with Strawberry and other libraries
- **File uploads**: Single and multiple file handling
- **Streaming responses**: StreamingResponse for large data
- **Static files**: StaticFiles mount for serving static content
