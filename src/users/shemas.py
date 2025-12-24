from pydantic import BaseModel, EmailStr
from typing import Optional 

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    
class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    
    
