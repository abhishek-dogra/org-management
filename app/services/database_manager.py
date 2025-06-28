from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from app.core.database import Base, create_org_database_url
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


# This would be responsible for the creation of new database instances for the organizations on the request of admins
class DatabaseManager:
    @staticmethod
    def create_organization_database(org_name: str) -> str:
        db_name = f"org_{org_name.lower().replace(' ', '_').replace('-', '_')}"

        admin_url = f"postgresql://{settings.ORG_DB_USER}:{settings.ORG_DB_PASSWORD}@{settings.ORG_DB_HOST}:{settings.ORG_DB_PORT}/postgres"
        admin_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")

        try:
            with admin_engine.connect() as conn:
                # Check if database exists
                result = conn.execute(
                    text("SELECT 1 FROM pg_database WHERE datname = :db_name"),
                    {"db_name": db_name}
                )
                if result.fetchone():
                    logger.info(f"Database {db_name} already exists")
                else:
                    # Create database
                    conn.execute(text(f'CREATE DATABASE "{db_name}"'))
                    logger.info(f"Created database: {db_name}")

            # Create tables in the new database
            org_db_url = create_org_database_url(org_name)
            org_engine = create_engine(org_db_url)
            Base.metadata.create_all(bind=org_engine)

            return org_db_url

        except SQLAlchemyError as e:
            logger.error(f"Error creating database {db_name}: {e}")
            raise
        finally:
            admin_engine.dispose()
