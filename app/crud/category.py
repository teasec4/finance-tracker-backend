from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import CategoryCreate

def create_category(db: Session, category: CategoryCreate, user_id: int):
    db_category = Category(name=category.name, user_id=user_id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session, user_id: int):
    return db.query(Category).filter(Category.user_id == user_id).all()

def get_category(db: Session, category_id: int, user_id: int):
    return db.query(Category).filter(Category.id == category_id, Category.user_id == user_id).first()

def update_category(db: Session, category_id: int, category_data: CategoryCreate, user_id: int):
    db_category = get_category(db, category_id, user_id)
    if not db_category:
        return None
    db_category.name = category_data.name
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int, user_id: int):
    db_category = get_category(db, category_id, user_id)
    if not db_category:
        return None
    db.delete(db_category)
    db.commit()
    return db_category