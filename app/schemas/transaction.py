from pydantic import BaseModel
from typing import Optional

class TransactionCreate(BaseModel):
    amount: float
    description: Optional[str]
    category_id: int
    type: str  # Добавляем поле type ('income' или 'outcome')

class TransactionRead(BaseModel):
    id: int
    amount: float
    description: Optional[str]
    category_id: int
    type: str

    class Config:
        orm_mode = True