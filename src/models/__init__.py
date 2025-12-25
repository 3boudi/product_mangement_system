from __future__ import annotations
from sqlmodel import SQLModel

# Import all models here to ensure they're registered
from src.users.models import User
from src.products.models1 import Product

__all__ = ["User", "Product"]