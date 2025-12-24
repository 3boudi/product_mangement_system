from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.core.database import create_db_and_tables ,test_connection
from src.users.router import router as users_router
from src.products.router1 import router as products_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting up...")
    test_connection()
    create_db_and_tables()   
    yield
    print("🛑 Shutting down...")


app = FastAPI(title="Neon FastAPI", lifespan=lifespan)

app.include_router(users_router)
app.include_router(products_router)