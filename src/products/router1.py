from fastapi import APIRouter, Depends
from sqlmodel import Session
from src.core.database import get_session
from src.products.service1 import ProductService
from src.products.shemas1 import ProductCreate
from src.products.models1 import Product

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=Product)
def create_product(
    data: ProductCreate,
    session: Session = Depends(get_session)
):
    service = ProductService(session)
    product = service.create_product( name=data.name, price=data.price, description=data.description, owner_id=data.owner_id)
    return product
@router.get("/{product_id}", response_model=Product | dict)
def get_product_by_id(
    product_id: int,
    session: Session = Depends(get_session)
):
    service = ProductService(session)
    product = service.get_by_id(product_id)
    if product:
        return product
    return {"message": "Product not found"}
@router.get("/", response_model=list[Product])
def get_all_products(
    session: Session = Depends(get_session)
):
    service = ProductService(session)
    products = service.get_all()
    return products
@router.delete("/{product_id}", response_model=dict)
def delete_product(
    product_id: int,
    session: Session = Depends(get_session)
):
    service = ProductService(session)
    success = service.delete_product(product_id)
    if success:
        return {"message": "Product deleted successfully"}
    return {"message": "Product not found"}
@router.put("/{product_id}", response_model=Product | dict)
def update_product(
    product_id: int,
    data: ProductCreate,
    session: Session = Depends(get_session)
):
    service = ProductService(session)
    product = service.update_product(
        product_id,
        name=data.name,
        price=data.price,
        description=data.description
    )
    if product:
        return product
    return {"message": "Product not found"}
@router.get("/owner/{owner_id}", response_model=list[Product])
def get_owner_by_product(
    product_id: int,
    session: Session = Depends(get_session)
):
    service = ProductService(session)
    owner = service.get_owner_by_product(product_id)
    return owner


