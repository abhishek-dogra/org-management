from fastapi import APIRouter
from app.api.endpoints import organization, auth

api_router = APIRouter()

api_router.include_router(organization.router, prefix="/org", tags=["organizations"])
api_router.include_router(auth.router, prefix="/admin", tags=["authentication"])