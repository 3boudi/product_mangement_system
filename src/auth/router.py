from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from src.core.database import get_session
from src.auth.schemas import Token, UserCreate, UserLogin, UserResponse
from src.auth.utils import (
    authenticate_user, create_access_token, get_password_hash,
    get_current_user, get_current_active_user, get_current_superuser,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from src.users.models import User
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate, session: Session = Depends(get_session)):
    # Check if user already exists
    statement = select(User).where(User.email == user.email)
    existing_user = session.exec(statement).first()
    
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    new_user = User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password,
        is_active=True,
        is_superuser=False,
        is_verified=False
    )
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return new_user

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, session: Session = Depends(get_session)):
    user = authenticate_user(user_data.email, user_data.password, session)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/verify-token")
async def verify_token(current_user: User = Depends(get_current_user)):
    return {"valid": True, "user_id": current_user.id}