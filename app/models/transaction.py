from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import date

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(String, nullable=False) # crypted amount
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    type = Column(String, nullable=False)  # Добавляем поле type
    date = Column(Date, default=date.today)  # добавили дату

    user = relationship("User")
    category = relationship("Category")