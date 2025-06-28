import asyncio
import logging
from sqlalchemy import text, inspect
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from app.core.database import master_engine, Base

logger = logging.getLogger(__name__)


async def wait_for_database(max_retries: int = 30, delay: int = 2):
    for attempt in range(max_retries):
        try:
            with master_engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Database connection successful")
            return True
        except OperationalError as e:
            logger.warning(f"Database not ready (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(delay)
            else:
                logger.error("Max retries reached. Database is not available.")
                raise
    return False


async def create_tables_if_not_exist():
    try:
        await wait_for_database()

        # Check if tables exist
        inspector = inspect(master_engine)
        existing_tables = inspector.get_table_names()

        required_tables = ['organizations']
        missing_tables = [table for table in required_tables if table not in existing_tables]

        if missing_tables:
            logger.info(f"Creating missing tables: {missing_tables}")
            # Create all tables
            Base.metadata.create_all(bind=master_engine)
            logger.info("All tables created successfully")
        else:
            logger.info("All required tables already exist")

        # Verify tables were created
        inspector = inspect(master_engine)
        final_tables = inspector.get_table_names()
        logger.info(f"Available tables: {final_tables}")

    except SQLAlchemyError as e:
        logger.error(f"Database error during table creation: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during startup: {e}")
        raise


async def check_database_health():
    try:
        with master_engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            logger.info(f"Database health check passed. PostgreSQL version: {version}")
            return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False
