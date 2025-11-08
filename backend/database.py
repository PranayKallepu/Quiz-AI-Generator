from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from the backend directory
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Database URL - supports SQLite (default), MySQL, and PostgreSQL
# SQLite is the default as it requires no additional setup or drivers
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./quiz.db"  # Default to SQLite for easier setup
)

# Create engine with appropriate configuration
# SQLite requires check_same_thread=False for FastAPI
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL, 
        echo=True,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL, echo=True)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models (SQLAlchemy 2.0 style)
class Base(DeclarativeBase):
    pass


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)

