from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionRead
import os

def create_transaction(db: Session, transaction: TransactionCreate, user_id: int):
    db_transaction = Transaction(
        amount=transaction.amount,
        description=transaction.description,
        category_id=transaction.category_id,
        user_id=user_id
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transactions(db: Session, user_id: int):
    return db.query(Transaction).filter(Transaction.user_id == user_id).all()

def get_transaction(db: Session, transaction_id: int, user_id: int):
    return db.query(Transaction).filter(Transaction.id == transaction_id, Transaction.user_id == user_id).first()

def update_transaction(db: Session, transaction_id: int, user_id: int, transaction_data: TransactionCreate):
    db_transaction = get_transaction(db, transaction_id, user_id)
    if not db_transaction:
        return None
    db_transaction.amount = transaction_data.amount
    db_transaction.description = transaction_data.description
    db_transaction.category_id = transaction_data.category_id
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def delete_transaction(db: Session, transaction_id: int, user_id: int):
    db_transaction = get_transaction(db, transaction_id, user_id)
    if not db_transaction:
        return None
    db.delete(db_transaction)
    db.commit()
    return db_transaction