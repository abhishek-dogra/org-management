from datetime import timedelta

from app.core.config import settings
from app.core.security import create_access_token


class AuthService:
    @staticmethod
    def authenticate_user(user_id: int) -> dict:
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"user_id": user_id},
            expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
