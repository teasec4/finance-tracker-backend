from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from app.models.category import Category
from fastapi import HTTPException

def create_user(db: Session, user: UserCreate):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pw = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # копируем глобальные категории
    global_categories = db.query(Category).filter(Category.user_id == None).all()
    for cat in global_categories:
        new_cat = Category(name=cat.name, type=cat.type, user_id=db_user.id)
        db.add(new_cat)
    db.commit()

    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()