from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_master_db
from app.schemas.organization import OrganizationCreate, OrganizationResponse, OrganizationGet
from app.services.organization import OrganizationService
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/create", response_model=OrganizationResponse)
def create_organization(
        org_data: OrganizationCreate,
        db: Session = Depends(get_master_db)
):
    # Check if email already exists
    user = OrganizationService.get_user_by_email(db, org_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This email is already linked to an organization"
        )

    # Check if organization already exists
    existing_org = OrganizationService.get_organization_by_name(db, org_data.organization_name)
    if existing_org:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization already exists"
        )

    try:
        organization = OrganizationService.create_organization(db, org_data)
        return organization

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create organization"
        )


@router.post("/get", response_model=OrganizationResponse)
def get_organization(
        org_data: OrganizationGet,
        db: Session = Depends(get_master_db),
        current_user: User = Depends(get_current_user)
):
    organization = OrganizationService.get_organization_by_name(db, org_data.organization_name)
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    if current_user.organization.name != organization.name:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User does not belong to organization"
        )
    return organization
