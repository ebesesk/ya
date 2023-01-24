# from config import settings
from sqlalchemy import create_engine, engine_from_config
from sqlalchemy.orm import sessionmaker
from typing import Generator
from db.models.users import User
from db.models.videos import Video
# # For PostgreSQL Database
# SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# For SQLite Database
SQLALCHEMY_DATABASE_URL = 'sqlite:///./sqlite.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread" : False}
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 

