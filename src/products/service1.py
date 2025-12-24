from sqlmodel import Session, select
from src.products.models1 import Product

class ProductService:
    
    def __init__(self, session: Session):
        self.session = session
    def create_product(self, name: str, price: float, description: str | None = None, owner_id: int | None = None) -> Product:
        new_product = Product(name=name, price=price, description=description, owner_id=owner_id)
        self.session.add(new_product)
        self.session.commit()
        self.session.refresh(new_product)
        return new_product
    def get_by_id(self, product_id: int) -> Product | None:
        statement = select(Product).where(Product.id == product_id)
        result = self.session.exec(statement).first()
        return result
    def get_all(self) -> list[Product]:
        statement = select(Product)
        results = self.session.exec(statement).all()
        return results
    def delete_product(self, product_id: int) -> bool:
        product = self.get_by_id(product_id)
        if product:
            self.session.delete(product)
            self.session.commit()
            return True
        return False
    def update_product(self, product_id: int, name: str | None = None, price: float | None = None, description: str | None = None) -> Product | None:
        product = self.get_by_id(product_id)
        if product:
            if name:
                product.name = name
            if price:
                product.price = price
            if description:
                product.description = description
            self.session.add(product)
            self.session.commit()
            self.session.refresh(product)
            return product
        return None
    def get_owner_by_product(self, product_id: int) -> list[Product]:
        product = self.get_by_id(product_id)
        if product:
            owner = product.owner
            return owner
        return None
