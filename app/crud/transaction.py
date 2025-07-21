from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionRead
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from datetime import date

load_dotenv()

ENCRYPTION_KEY = os.environ['ENCRYPTION_KEY']
fernet = Fernet(ENCRYPTION_KEY.encode())

def encrypt_amount(amount: float) -> str:
    return fernet.encrypt(str(amount).encode()).decode()

def decrypt_amount(encrypted_amount: str) -> float:
    return float(fernet.decrypt(encrypted_amount.encode()).decode())

def create_transaction(db: Session, transaction: TransactionCreate, user_id: int):
    encrypted_amount = encrypt_amount(transaction.amount)
    db_transaction = Transaction(
        amount=encrypted_amount,
        description=transaction.description,
        category_id=transaction.category_id,
        user_id=user_id,
        type=transaction.type,
        date=transaction.date or date.today()
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    db_transaction.amount = decrypt_amount(db_transaction.amount)
    return db_transaction

def get_transactions(db: Session, user_id: int):
    db_transactions = db.query(Transaction).filter(Transaction.user_id == user_id).all()
    for transaction in db_transactions:
        transaction.amount = decrypt_amount(transaction.amount)
    return db_transactions

def get_transaction(db: Session, transaction_id: int, user_id: int):
    db_transaction = db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.user_id == user_id).first()
    if db_transaction:
        db_transaction.amount = decrypt_amount(db_transaction.amount)
    return db_transaction


def update_transaction(db: Session, transaction_id: int, user_id: int, transaction_data: TransactionCreate):
    db_transaction = get_transaction(db, transaction_id, user_id)
    if not db_transaction:
        return None
    db_transaction.amount = encrypt_amount(transaction_data.amount)
    db_transaction.description = transaction_data.description
    db_transaction.category_id = transaction_data.category_id
    db_transaction.type = transaction_data.type
    db_transaction.date = transaction_data.date or db_transaction.date
    
    db.commit()
    db.refresh(db_transaction)
    db_transaction.amount = decrypt_amount(db_transaction.amount)
    return db_transaction

def delete_transaction(db: Session, transaction_id: int, user_id: int):
    db_transaction = get_transaction(db, transaction_id, user_id)
    if not db_transaction:
        return None
    db.delete(db_transaction)
    db.commit()
    return db_transaction