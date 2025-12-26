from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from src.core.database import get_session
from src.users.service import UserService
from src.users.shemas import UserCreate, UserRead, UserUpdate
from src.products.shemas1 import ProductRead
from src.auth.utils import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead)
async def create_user(
    data: UserCreate,
    session: Session = Depends(get_session)
): 
    service = UserService(session)
    
    # Check if user already exists
    existing_user = service.get_by_email(data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    user = service.create_user(
        name=data.name, 
        email=data.email,
        password=data.password
    )
    return user

@router.get("/{user_id}", response_model=UserRead)
async def get_user_by_id(
    user_id: int,
    session: Session = Depends(get_session)
):
    service = UserService(session)
    user = service.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    return user

@router.get("/", response_model=list[UserRead])
async def get_all_users(
    session: Session = Depends(get_session)
):
    service = UserService(session)
    users = service.get_all()
    return users

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    session: Session = Depends(get_session)
):
    service = UserService(session)
    success = service.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )

@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    data: UserUpdate,
    session: Session = Depends(get_session)
):
    service = UserService(session)
    user = service.update_user(user_id, name=data.name, email=data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    return user

@router.get("/{user_id}/products", response_model=list[ProductRead])
async def get_user_products(
    user_id: int,
    session: Session = Depends(get_session)
):
    service = UserService(session)
    user = service.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
    products = service.get_user_products(user_id)
    return products

# Protected endpoints (require authentication)
@router.get("/me/profile", response_model=UserRead)
async def get_my_profile(
    current_user = Depends(get_current_user)
):
    return current_user

@router.get("/me/products", response_model=list[ProductRead])
async def get_my_products(
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    service = UserService(session)
    products = service.get_user_products(current_user.id)
    return products