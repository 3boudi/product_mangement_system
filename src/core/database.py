from sqlmodel import SQLModel, create_engine, Session
from src.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
)

def create_db_and_tables():
    # Clear existing tables with CASCADE option
    #SQLModel.metadata.drop_all(engine)
    # Create all tables
    SQLModel.metadata.create_all(engine)
def get_session():
    with Session(engine) as session:
        yield session
        
def test_connection():
    try:
        with engine.connect():
            print("✅ Database connection successful!")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")