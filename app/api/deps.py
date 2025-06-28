from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_master_db
from app.core.security import verify_token
from app.services.organization import OrganizationService

security = HTTPBearer()


def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_master_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_token(credentials.credentials)
    if payload is None:
        raise credentials_exception
    user_id = payload.get("user_id", None)
    if user_id is None:
        raise credentials_exception

    user = OrganizationService.get_user_by_id(db, user_id)
    if user is None:
        raise credentials_exception

    return user
