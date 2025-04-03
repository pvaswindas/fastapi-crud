from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from crud import create_item, get_items, get_item, delete_item
import schemas

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.ItemResponse)
def create_new_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return create_item(db, item)


@router.get("/", response_model=list[schemas.ItemResponse])
def read_items(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    return get_items(db, skip, limit)


@router.get("/{item_id}", response_model=schemas.ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.delete("/{item_id}")
def remove_item(item_id: int, db: Session = Depends(get_db)):
    if not delete_item(db, item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}
