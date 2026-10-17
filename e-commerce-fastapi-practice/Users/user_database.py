from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, declarative_base

USER_DATABASE_URL = 'sqlite:///./user_database.db'
DATABASE_URL = "sqlite:///./products.db"

engine = create_engine(USER_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

UserBase = declarative_base()

def get_user_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
