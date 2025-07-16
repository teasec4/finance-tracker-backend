from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.category import CategoryCreate, CategoryRead
from app.crud.category import create_category
from app.crud import category as crud_category
from app.core.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=CategoryRead)
def create_new_category(category: CategoryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_category.create_category(db, category, current_user.id)

@router.get("/", response_model=List[CategoryRead])
def read_categories(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_category.get_categories(db, current_user.id)

@router.put("/{category_id}", response_model=CategoryRead)
def update_existing_category(category_id: int, category_data: CategoryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_category = crud_category.update_category(db, category_id, category_data, current_user.id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.delete("/{category_id}")
def delete_existing_category(category_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_category = crud_category.delete_category(db, category_id, current_user.id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"detail": "Category deleted"}