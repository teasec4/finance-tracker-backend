from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.schemas.transaction import TransactionCreate, TransactionRead
from app.crud.transaction import create_transaction
from app.crud import transaction as crud_transaction
from app.core.deps import get_db, get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=TransactionRead)
def create_new_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    print(f"create_transaction: Received transaction: {transaction.dict()}")
    print(f"create_transaction: Current user ID: {current_user.id}")
    
    return create_transaction(db, transaction, current_user.id)

@router.get("/", response_model=List[TransactionRead])
def read_transactions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud_transaction.get_transactions(db, current_user.id)

@router.put("/{transaction_id}", response_model=TransactionRead)
def update_existing_transaction(transaction_id: int, transaction_data: TransactionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_transaction = crud_transaction.update_transaction(db, transaction_id, current_user.id, transaction_data)
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

@router.delete("/{transaction_id}")
def delete_existing_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_transaction = crud_transaction.delete_transaction(db, transaction_id, current_user.id)
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"detail": "Transaction deleted"}