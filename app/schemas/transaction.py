from pydantic import BaseModel
from typing import Optional
from typing import Literal
from datetime import date as DateType


class TransactionCreate(BaseModel):
    amount: float
    category_id: int
    type: Literal['income', 'expense']  # Ограничиваем значения type
    description: Optional[str] = None
    date: Optional[DateType] = None
    
class TransactionRead(BaseModel):
    id: int
    amount: float
    description: Optional[str]
    category_id: int
    type: str
    user_id: int  # Предполагаем, что user_id обязателен в ответе
    date: DateType

    class Config:
        orm_mode = True