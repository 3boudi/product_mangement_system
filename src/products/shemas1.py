from pydantic import BaseModel 
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    owner_id: Optional[int] = None
class ProductRead(BaseModel):
    id: int
    name: str
    price: float
    description: Optional[str] = None
    owner_id: Optional[int] = None