from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_master_db
from app.core.security import verify_password
from app.schemas.token import Token, LoginRequest
from app.services.auth import AuthService
from app.services.organization import OrganizationService

router = APIRouter()


@router.post("/login", response_model=Token)
def login(
        login_data: LoginRequest,
        db: Session = Depends(get_master_db)
):
    email = login_data.email
    password = login_data.password

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    # Get user
    user = OrganizationService.get_user_by_email(db, email.strip().lower())

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Verify password
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Check if user is active
    if hasattr(user, 'is_active') and not user.is_active:
        raise HTTPException(status_code=401, detail="Account is disabled")

    auth_result = AuthService.authenticate_user(user.id)

    return {
        "access_token": auth_result["access_token"],
        "token_type": auth_result["token_type"]
    }
