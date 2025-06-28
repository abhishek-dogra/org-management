from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Master database engine
master_engine = create_engine(settings.MASTER_DATABASE_URL)
MasterSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=master_engine)

Base = declarative_base()


def get_master_db():
    db = MasterSessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_org_database_url(org_name: str) -> str:
    db_name = f"org_{org_name.lower().replace(' ', '_').replace('-', '_')}"
    return f"postgresql://{settings.ORG_DB_USER}:{settings.ORG_DB_PASSWORD}@{settings.ORG_DB_HOST}:{settings.ORG_DB_PORT}/{db_name}"
