from pydantic import BaseModel
from typing import Optional

class CategoryCreate(BaseModel):
    name: str
    type: str  # income or expense

class CategoryRead(BaseModel):
    id: int
    name: str
    type: str  # income or expense
    user_id: Optional[int]

    class Config:
        orm_mode = True