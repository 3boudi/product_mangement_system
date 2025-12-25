from src.core.database import get_session
from src.auth.utils import get_password_hash
from src.users.models import User
from src.products.models1 import Product

# Create a test session
session = next(get_session())

# Create a user
user = User(
    email="test@example.com",
    name="Test User",
    hashed_password=get_password_hash("password123"),
    is_active=True,
    is_superuser=False,
    is_verified=False
)
session.add(user)
session.commit()
session.refresh(user)
print(f"✅ Created user: {user.id}, {user.email}")

# Create a product for this user
product = Product(
    name="Test Product",
    price=99.99,
    description="Test product description",
    owner_id=user.id
)
session.add(product)
session.commit()
session.refresh(product)
print(f"✅ Created product: {product.id}, {product.name}, Owner ID: {product.owner_id}")

# Test the relationship
print(f"User's products: {user.products}")  # Should show the product
print(f"Product's owner: {product.owner.name}")  # Should show the user's name