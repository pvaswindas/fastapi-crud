from fastapi import FastAPI
from database import engine, Base
from routes import items


# Initialize DB
Base.metadata.create_all(bind=engine)


app = FastAPI()


# Include Routes
app.include_router(items.router, prefix='/items', tags=["Items"])


@app.get('/')
def root():
    return {"message": "Welcome to FastAPI with PostgreSQL"}
