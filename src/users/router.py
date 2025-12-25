from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from src.core.database import get_session
from src.users.service import UserService
from src.users.shemas import UserCreate, UserRead, UserUpdate
from src.products.shemas1 import ProductRead
from src.auth.utils import get_current_active_user, get_current_user  # ✅ Correct import

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead)
async def create_user(
    data: UserCreate,
    session: Session = Depends(get_session)
): 
    service = UserService(session)
    user = service.create_user(name=data.name, email=data.email)
    return user

@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(
    user_id: int,
    session: Session = Depends(get_session)
):
    service = UserService(session)
    user = service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=list[UserRead])
async def get_all_users(
    session: Session = Depends(get_session)
):
    service = UserService(session)
    users = service.get_all()
    return users

@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    session: Session = Depends(get_session)
):
    service = UserService(session)
    success = service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    data: UserUpdate,
    session: Session = Depends(get_session)
):
    service = UserService(session)
    user = service.update_user(user_id, name=data.name, email=data.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/{user_id}/products", response_model=list[ProductRead])
async def get_user_products(
    user_id: int,
    session: Session = Depends(get_session)
):
    service = UserService(session)
    products = service.get_user_products(user_id)
    if isinstance(products, str):
        raise HTTPException(status_code=404, detail=products)
    return products

# Protected endpoints (require authentication)
@router.get("/me/profile", response_model=UserRead)
async def get_my_profile(
    current_user = Depends(get_current_user)  # ✅ Use the correct function
):
    return current_user

@router.get("/me/products", response_model=list[ProductRead])
async def get_my_products(
    session: Session = Depends(get_session),
    current_user = Depends(get_current_active_user)  # ✅ Use the correct function
):
    service = UserService(session)
    products = service.get_user_products(current_user.id)
    if isinstance(products, str):
        raise HTTPException(status_code=404, detail=products)
    return products