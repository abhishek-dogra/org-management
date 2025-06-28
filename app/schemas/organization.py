from pydantic import BaseModel, EmailStr
from datetime import datetime


class OrganizationCreate(BaseModel):
    email: EmailStr
    password: str
    organization_name: str


class OrganizationResponse(BaseModel):
    id: int
    name: str
    admin_email: str
    created_at: datetime
    database_url: str

    class Config:
        from_attributes = True


class OrganizationGet(BaseModel):
    organization_name: str
