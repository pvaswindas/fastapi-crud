# Simple FastAPI CRUD

## 🚀 Overview
This project is a **FastAPI** backend with **CRUD** (Create, Read, Update, Delete) operations using **PostgreSQL** and **SQLAlchemy**. It is a **simple CRUD API built for learning purposes**, providing a RESTful API for managing data with structured request validation using **Pydantic**.

## 📌 Features
- FastAPI-based RESTful API
- CRUD operations for database models
- PostgreSQL as the database
- SQLAlchemy ORM for database interactions
- Pydantic for request validation
- Environment variable management with `.env`

## 🛠️ Tech Stack
- **FastAPI** - Web framework
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM for database interaction
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## 📂 Project Structure
```
fastapi_crud/
│── routes/          # API route handlers
│── models.py        # Database models
│── schemas.py       # Pydantic schemas
│── database.py      # Database connection setup
│── crud.py          # CRUD operations
│── main.py          # FastAPI app entry point
│── .env             # Environment variables
│── .gitignore       # Ignored files
│── README.md        # Project documentation
```

## ⚡ Installation
### 1️⃣ Clone the Repository
```sh
git clone https://github.com/your-username/fastapi-crud.git
cd fastapi-crud
```

### 2️⃣ Set Up Virtual Environment
```sh
python -m venv fastapi-env
source fastapi-env/bin/activate  # On Windows use `fastapi-env\Scripts\activate`
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables
Create a `.env` file in the project root:
```
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### 5️⃣ Run the FastAPI Server
```sh
uvicorn main:app --reload
```

## 📌 API Endpoints
| Method | Endpoint         | Description         |
|--------|-----------------|---------------------|
| POST   | `/items/`       | Create an item     |
| GET    | `/items/`       | Get all items      |
| GET    | `/items/{id}`   | Get a specific item |
| PUT    | `/items/{id}`   | Update an item     |
| DELETE | `/items/{id}`   | Delete an item     |

## 🎯 Learning Purpose
This is a **simple CRUD API** built to understand and practice **FastAPI, SQLAlchemy, and PostgreSQL**. It is not intended for production use but serves as a foundation for learning backend development with FastAPI.

🚀 **Happy coding!**