from app.db.session import engine, SessionLocal
from app.db.base import Base
from app.models import user, category, transaction
from app.models.category import Category

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    default_categories = ["Food", "Transport", "Entertainment", "Health", "Bills", "Shopping", "Salary", "Investments"]
    print("Seeding default categories...")

    for name in default_categories:
        existing = db.query(Category).filter_by(name=name).first()
        if not existing:
            db.add(Category(name=name))
            print(f"Category added: {name}")
        else:
            print(f"Category already exists: {name}")
            
    db.commit()
    db.close()
    print("Default categories initialized!")
            

if __name__ == "__main__":
    init_db()