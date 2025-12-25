from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.core.database import create_db_and_tables, test_connection
from src.users.router import router as users_router
from src.products.router1 import router as products_router
from src.auth.router import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting up...")
    test_connection()
    create_db_and_tables()   
    yield
    print("🛑 Shutting down...")

app = FastAPI(title="FastAPI with Simple Authentication", lifespan=lifespan)

# Include routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(products_router)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI with Simple Authentication"}