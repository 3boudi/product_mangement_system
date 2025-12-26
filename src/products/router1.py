from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from src.core.database import get_session
from src.products.service1 import ProductService
from src.products.shemas1 import ProductCreate, ProductUpdate, ProductRead, ProductWithOwner
from src.products.models1 import Product
from src.auth.utils import get_current_user

router = APIRouter(prefix="/products", tags=["products"])

# Public endpoints
@router.get("/{product_id}", response_model=ProductWithOwner)
def get_product_by_id(
    product_id: int,
    session: Session = Depends(get_session)
):
    service = ProductService(session)
    product = service.get_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Product not found"
        )
    return product

@router.get("/", response_model=list[ProductRead])
def get_all_products(
    session: Session = Depends(get_session)
):
    service = ProductService(session)
    products = service.get_all()
    return products

@router.get("/owner/{owner_id}", response_model=list[ProductRead])
def get_products_by_owner(
    owner_id: int,
    session: Session = Depends(get_session)
):
    service = ProductService(session)
    products = service.get_products_by_owner(owner_id)
    return products

# Protected endpoints (require authentication)
@router.post("/", response_model=ProductRead)
def create_product(
    data: ProductCreate,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    service = ProductService(session)
    
    # Always use current user's ID for ownership
    product = service.create_product(
        name=data.name,
        price=data.price,
        description=data.description,
        owner_id=current_user.id
    )
    return product

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    service = ProductService(session)
    
    # Check if product exists
    product = service.get_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Product not found"
        )
    
    # Check ownership
    if product.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized to delete this product"
        )
    
    success = service.delete_product(product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to delete product"
        )

@router.patch("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    data: ProductUpdate,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    service = ProductService(session)
    
    # Check if product exists
    product = service.get_by_id(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Product not found"
        )
    
    # Check ownership
    if product.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized to update this product"
        )
    
    # Update product with provided data
    update_data = {}
    if data.name is not None:
        update_data['name'] = data.name
    if data.price is not None:
        update_data['price'] = data.price
    if data.description is not None:
        update_data['description'] = data.description
    
    updated_product = service.update_product(
        product_id,
        **update_data
    )
    
    if not updated_product:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to update product"
        )
    
    return updated_product

@router.get("/me/products", response_model=list[ProductRead])
def get_my_products(
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    service = ProductService(session)
    products = service.get_products_by_owner(current_user.id)
    return products