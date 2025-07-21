from app.db.session import engine, SessionLocal
from app.db.base import Base
from app.models import user, category, transaction
from app.models.category import Category

def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    default_categories = [
    {"name": "Food", "type": "expense"},
    {"name": "Transport", "type": "expense"},
    {"name": "Entertainment", "type": "expense"},
    {"name": "Health", "type": "expense"},
    {"name": "Bills", "type": "expense"},
    {"name": "Shopping", "type": "expense"},
    {"name": "Salary", "type": "income"},
    {"name": "Investments", "type": "income"}
]
    print("Seeding default categories...")

    for name in default_categories:
        existing = db.query(Category).filter_by(name=name['name']).first()
        if not existing:
            db.add(Category(name=name['name'], type=name['type']))
            print(f"Category added: {name['name']} - type: {name['type']}")
        else:
            print(f"Category already exists: {name}")
            
    db.commit()
    db.close()
    print("Default categories initialized!")
            

if __name__ == "__main__":
    init_db()