# AI_MANIFEST.md

## System Architecture & Data Flow

- **Architecture Pattern**: Monolithic RESTful API service based on standard layer separation (Route Handlers -> Data Access/CRUD Layer -> SQLAlchemy ORM Layer -> Relational Database).
- **Core Technology Components**:
  - **Web Framework**: FastAPI (v0.115.12) running on Uvicorn ASGI server (v0.34.0).
  - **ORM**: SQLAlchemy (v2.0.40).
  - **Data Layer / Driver**: PostgreSQL accessed via `psycopg2-binary` (v2.9.10).
  - **Validation & Serialization**: Pydantic v2 (`pydantic` v2.11.2 / `pydantic_core` v2.33.1).
  - **Environment Configuration**: `python-dotenv` (v1.1.0).
- **Request / Response Data Flow**:
  1. An HTTP request targets an endpoint defined in [`routes/items.py`](file:///home/aswin/code/broto/fastapi_crud/routes/items.py) or [`main.py`](file:///home/aswin/code/broto/fastapi_crud/main.py).
  2. Request body / query parameters are parsed and validated using Pydantic models from [`schemas.py`](file:///home/aswin/code/broto/fastapi_crud/schemas.py).
  3. The route handler uses FastAPI's `Depends(get_db)` to acquire a SQLAlchemy `Session` initialized in [`database.py`](file:///home/aswin/code/broto/fastapi_crud/database.py).
  4. The route handler passes the database session and validated schema payload to a helper function in [`crud.py`](file:///home/aswin/code/broto/fastapi_crud/crud.py).
  5. [`crud.py`](file:///home/aswin/code/broto/fastapi_crud/crud.py) executes queries or transactions against PostgreSQL via the `Item` SQLAlchemy model defined in [`models.py`](file:///home/aswin/code/broto/fastapi_crud/models.py).
  6. Results are returned as SQLAlchemy model instances, serialized into JSON matching Pydantic response schemas (`from_attributes = True`), and returned to the caller.
  7. The `get_db()` generator closes the database session in its `finally` block upon request completion.

## Core Modules & Exact File Paths

- [`/home/aswin/code/broto/fastapi_crud/main.py`](file:///home/aswin/code/broto/fastapi_crud/main.py)
  - **Role**: Application entry point and router registration.
  - **Functionality**:
    - Executes `Base.metadata.create_all(bind=engine)` at module load time to automatically generate missing database tables.
    - Instantiates the primary `FastAPI()` application instance (`app`).
    - Registers the items router (`app.include_router(items.router, prefix='/items', tags=["Items"])`).
    - Defines the root endpoint `GET /` returning welcome JSON.

- [`/home/aswin/code/broto/fastapi_crud/database.py`](file:///home/aswin/code/broto/fastapi_crud/database.py)
  - **Role**: Database connection setup and session management.
  - **Functionality**:
    - Calls `dotenv.load_dotenv()` to parse environment configuration.
    - Reads `DATABASE_URL` via `os.getenv("DATABASE_URL")`.
    - Creates the SQLAlchemy connection engine via `create_engine(DATABASE_URL)`.
    - Constructs `SessionLocal` factory (`sessionmaker(autocommit=False, autoflush=False, bind=engine)`).
    - Creates base declarative class `Base = declarative_base()`.

- [`/home/aswin/code/broto/fastapi_crud/models.py`](file:///home/aswin/code/broto/fastapi_crud/models.py)
  - **Role**: Database ORM models.
  - **Functionality**:
    - Defines `Item(Base)` mapping to the `items` table in PostgreSQL.

- [`/home/aswin/code/broto/fastapi_crud/schemas.py`](file:///home/aswin/code/broto/fastapi_crud/schemas.py)
  - **Role**: Pydantic data validation schemas.
  - **Functionality**:
    - Defines `ItemBase` with `name` (str) and `description` (optional str).
    - Defines `ItemCreate` extending `ItemBase` for item creation payloads.
    - Defines `ItemResponse` extending `ItemBase` with `id` (int) and `Config.from_attributes = True`.

- [`/home/aswin/code/broto/fastapi_crud/crud.py`](file:///home/aswin/code/broto/fastapi_crud/crud.py)
  - **Role**: Data access routines and database operations.
  - **Functionality**:
    - `create_item(db, item)`: Instantiates and persists a new `Item` record.
    - `get_items(db, skip, limit)`: Fetches paginated `Item` records using offset/limit.
    - `get_item(db, item_id)`: Queries a single `Item` record by primary key.
    - `delete_item(db, item_id)`: Finds and deletes an `Item` record by primary key.

- [`/home/aswin/code/broto/fastapi_crud/routes/items.py`](file:///home/aswin/code/broto/fastapi_crud/routes/items.py)
  - **Role**: API route controllers for the `/items` endpoint prefix.
  - **Functionality**:
    - Defines DB session dependency generator `get_db()`.
    - `POST /`: Calls `create_item`.
    - `GET /`: Calls `get_items`.
    - `GET /{item_id}`: Calls `get_item`, raising HTTP 404 if missing.
    - `DELETE /{item_id}`: Calls `delete_item`, raising HTTP 404 if missing.

## Database Schemas & Data Models

### PostgreSQL Table: `items`
Defined in [`models.py`](file:///home/aswin/code/broto/fastapi_crud/models.py#L5-L10).

```sql
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    description VARCHAR NULLABLE
);
CREATE INDEX ix_items_id ON items (id);
CREATE INDEX ix_items_name ON items (name);
```

### SQLAlchemy Model (`models.py`)
```python
class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
```

### Pydantic Schemas (`schemas.py`)
```python
class ItemBase(BaseModel):
    name: str
    description: str | None = None

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int

    class Config:
        from_attributes = True
```

## API Endpoints & Integration Points

- **`GET /`**
  - **Handler**: `root()` in [`main.py`](file:///home/aswin/code/broto/fastapi_crud/main.py#L17-L19)
  - **Description**: Returns root welcome message.
  - **Response Payload**: `{"message": "Welcome to FastAPI with PostgreSQL"}`

- **`POST /items/`**
  - **Handler**: `create_new_item()` in [`routes/items.py`](file:///home/aswin/code/broto/fastapi_crud/routes/items.py#L18-L20)
  - **Description**: Creates a new item in the database.
  - **Request Body**: `ItemCreate` (`{"name": "Item Name", "description": "Optional description"}`)
  - **Response**: `ItemResponse` (`{"id": 1, "name": "Item Name", "description": "Optional description"}`)

- **`GET /items/`**
  - **Handler**: `read_items()` in [`routes/items.py`](file:///home/aswin/code/broto/fastapi_crud/routes/items.py#L23-L25)
  - **Description**: Retrieves a paginated list of items.
  - **Query Parameters**:
    - `skip` (int, default: `0`): Pagination offset.
    - `limit` (int, default: `10`): Max records returned.
  - **Response**: `list[ItemResponse]`

- **`GET /items/{item_id}`**
  - **Handler**: `read_item()` in [`routes/items.py`](file:///home/aswin/code/broto/fastapi_crud/routes/items.py#L28-L33)
  - **Description**: Retrieves a specific item by integer ID.
  - **Path Parameters**: `item_id` (int)
  - **Response**: `ItemResponse`
  - **Errors**: HTTP 404 (`{"detail": "Item not found"}`)

- **`DELETE /items/{item_id}`**
  - **Handler**: `remove_item()` in [`routes/items.py`](file:///home/aswin/code/broto/fastapi_crud/routes/items.py#L36-L40)
  - **Description**: Deletes a specific item by integer ID.
  - **Path Parameters**: `item_id` (int)
  - **Response**: `{"message": "Item deleted successfully"}`
  - **Errors**: HTTP 404 (`{"detail": "Item not found"}`)

## Setup Instructions & Legacy / Deprecated Dependencies

### Installation & Execution Setup
1. Create virtual environment:
   ```bash
   python -m venv fastapi-env
   source fastapi-env/bin/activate
   ```
2. Install exact locked dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create `.env` file in workspace root:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/dbname
   ```
4. Start ASGI server:
   ```bash
   uvicorn main:app --reload
   ```

### Documented Legacy Patterns & Dependencies
- **Deprecated SQLAlchemy Import**:
  - [`database.py`](file:///home/aswin/code/broto/fastapi_crud/database.py#L3) uses `from sqlalchemy.ext.declarative import declarative_base`.
  - In SQLAlchemy 2.0+, `sqlalchemy.ext.declarative` is deprecated in favor of `from sqlalchemy.orm import declarative_base` or `DeclarativeBase`.
- **Missing Update Endpoint**:
  - The codebase does not contain an update endpoint (`PUT` or `PATCH`), nor does [`crud.py`](file:///home/aswin/code/broto/fastapi_crud/crud.py) contain update logic.
- **Direct Schema Creation**:
  - [`main.py`](file:///home/aswin/code/broto/fastapi_crud/main.py#L7) triggers `Base.metadata.create_all(bind=engine)` directly at module import time rather than using database migration tools such as Alembic.
