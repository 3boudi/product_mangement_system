from pydantic import BaseModel 
from typing import Optional
from src.users.shemas import UserRead

class ProductBase(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None

class ProductRead(ProductBase):
    id: int
    owner_id: Optional[int] = None
    
    class Config:
        from_attributes = True

class ProductWithOwner(ProductRead):
    owner: Optional[UserRead] = None