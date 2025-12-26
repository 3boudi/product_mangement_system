from sqlmodel import Session, select
from src.users.models import User
from src.products.models1 import Product
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, session: Session):
        self.session = session
    
    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    def create_user(self, name: str, email: str, password: str) -> User:
        hashed_password = self.get_password_hash(password)
        new_user = User(
            name=name, 
            email=email, 
            hashed_password=hashed_password,
            is_active=True,
            is_superuser=False,
            is_verified=False
        )
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user
    
    def get_by_id(self, user_id: int) -> User | None:
        statement = select(User).where(User.id == user_id)
        result = self.session.exec(statement).first()
        return result
    
    def get_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        result = self.session.exec(statement).first()
        return result
    
    def get_all(self) -> list[User]:
        statement = select(User)
        results = self.session.exec(statement).all()
        return results
    
    def delete_user(self, user_id: int) -> bool:
        user = self.get_by_id(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False
    
    def update_user(self, user_id: int, name: str | None = None, email: str | None = None) -> User | None:
        user = self.get_by_id(user_id)
        if user:
            if name is not None:
                user.name = name
            if email is not None:
                user.email = email
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user
        return None
    
    def get_user_products(self, user_id: int) -> list[Product]:
        statement = select(Product).where(Product.owner_id == user_id)
        products = self.session.exec(statement).all()
        return products