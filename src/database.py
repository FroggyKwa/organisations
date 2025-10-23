from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    from src.models import Base
    Base.metadata.create_all(bind=engine)

