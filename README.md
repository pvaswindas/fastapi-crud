# FastAPI CRUD Service

A RESTful API built with FastAPI, SQLAlchemy 2.0, and PostgreSQL for item management.

## Tech Stack

- **Framework**: FastAPI 0.115.12
- **ASGI Server**: Uvicorn 0.34.0
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy 2.0.40
- **Data Validation**: Pydantic 2.11.2
- **Database Driver**: psycopg2-binary 2.9.10
- **Environment Management**: python-dotenv 1.1.0

## Quick Start

### 1. Environment Setup

Create and activate a Python virtual environment:

```bash
python -m venv fastapi-env
source fastapi-env/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the root directory with your PostgreSQL connection string:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

### 3. Run Application

Start the development server with auto-reload:

```bash
uvicorn main:app --reload
```

- **API Endpoint**: `http://127.0.0.1:8000`
- **Interactive Documentation (Swagger UI)**: `http://127.0.0.1:8000/docs`
- **Alternative Documentation (ReDoc)**: `http://127.0.0.1:8000/redoc`

## API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Root endpoint / health check |
| `POST` | `/items/` | Create a new item |
| `GET` | `/items/` | List items (supports `skip` and `limit` pagination) |
| `GET` | `/items/{item_id}` | Get item by ID |
| `DELETE` | `/items/{item_id}` | Delete item by ID |

## Project Structure

```
.
├── crud.py          # Data access layer and database queries
├── database.py      # Database engine and session initialization
├── main.py          # FastAPI application entry point and router registration
├── models.py        # SQLAlchemy ORM models
├── schemas.py       # Pydantic validation and response schemas
├── requirements.txt # Dependency specifications
└── routes/
    └── items.py     # API router for item endpoints
```