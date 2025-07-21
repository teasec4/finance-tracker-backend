from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True) # nullable для глобальных
    type = Column(String, nullable=False)  # 'income' or 'expense'

    user = relationship("User")

    __table_args__ = (UniqueConstraint('name', 'user_id', name='_user_category_uc'),)