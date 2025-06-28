from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.organization import Organization
from app.models.user import User
from app.schemas.organization import OrganizationCreate
from app.services.database_manager import DatabaseManager
from app.core.security import get_password_hash
import logging

logger = logging.getLogger(__name__)


class OrganizationService:
    @staticmethod
    def create_organization(db: Session, org_data: OrganizationCreate) -> Organization:
        try:
            # Create organization database
            org_db_url = DatabaseManager.create_organization_database(org_data.organization_name)

            # Create organization record in master database
            db_organization = Organization(
                name=org_data.organization_name,
                admin_email=org_data.email,
                database_url=org_db_url
            )
            db.add(db_organization)
            db.commit()

            db.refresh(db_organization)
            hashed_password = get_password_hash(org_data.password)
            admin_user = User(
                email=org_data.email,
                hashed_password=hashed_password,
                organization_id=db_organization.id,
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)

            return db_organization

        except SQLAlchemyError as e:
            db.rollback()
            print(f"Error creating organization: {e}")
            raise

    @staticmethod
    def get_organization_by_name(db: Session, org_name: str) -> Organization:
        return db.query(Organization).filter(Organization.name == org_name).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        return db.query(User).filter(User.id == user_id).first()
