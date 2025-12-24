from sqlmodel import Session, select
from src.products.models1 import Product
from src.users.models import User

class UserService:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, name: str, email: str) -> User:
        new_user = User(name=name, email=email)
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user

    def get_by_id(self, user_id: int) -> User | None:
        statement = select(User).where(User.id == user_id)
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
            if name:
                user.name = name
            if email:
                user.email = email
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user
        return None
    def get_user_products(self, user_id: int) -> list[Product] | str:
        user = self.get_by_id(user_id)
        if user:
            if user.products:
                return user.products
            else:  # No products
                return "This user has no products"
        return "User not found"  # User doesn't exist
                