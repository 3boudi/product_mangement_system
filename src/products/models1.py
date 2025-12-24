from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from src.users.models import User

class Product(SQLModel, table=True):
    __tablename__="products"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    description: Optional[str] = None
    owner_id: Optional[int]= Field(default=None, foreign_key="users.id")
    owner: Optional["User"]=Relationship(back_populates="products")