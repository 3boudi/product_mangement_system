from fastapi import APIRouter , Depends
from sqlmodel import Session
from src.core.database import get_session
from src.products.models1 import Product
from src.users.service import UserService
from src.users.shemas import UserCreate, UserRead,UserUpdate
from src.users.models import User
from src.products.shemas1 import ProductRead 

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead)
async def create_user(
    data: UserCreate,
    session: Session = Depends(get_session)
): 
    service = UserService(session)
    user = service.create_user(name=data.name, email=data.email)
    return user

@router.get("/{user_id}", response_model=UserRead | dict)
async def get_user_by_id(
    user_id: int,
    session: Session = Depends(get_session)
):
    service = UserService(session)
    user = service.get_by_id(user_id)
    if user:
        return user
    return {"message": "User not found"}
@router.get("/", response_model=list[UserRead])
async def get_all_users(
    session: Session = Depends(get_session)
):
    service = UserService(session)
    users = service.get_all()
    return users
@router.delete("/{user_id}", response_model=dict)
async def delete_user(
    user_id: int,
    session: Session = Depends(get_session)
):
    service = UserService(session)
    success = service.delete_user(user_id)
    if success:
        return {"message": "User deleted successfully"}
    return {"message": "User not found"}
@router.put("/{user_id}", response_model=UserUpdate | dict)
async def update_user(
    user_id: int,
    data: UserUpdate,
    session: Session = Depends(get_session)
):
    service = UserService(session)
    user = service.update_user(user_id, name=data.name, email=data.email)
    if user:
        return user
    return {"message": "User not found"}
@router.get("/{user_id}/products", response_model=list[ProductRead] | dict)
async def get_user_products(
    user_id: int,
    session: Session = Depends(get_session)
):
    service = UserService(session)
    products = service.get_user_products(user_id)
    if isinstance(products, list):
        return products
    return {"message": products}
