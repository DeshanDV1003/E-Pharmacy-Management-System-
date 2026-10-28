from datetime import datetime

from pydantic import BaseModel, Field

from app.models.user import UserType


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    nic: str = Field(..., min_length=1, max_length=20)
    user_type: UserType
    address: str | None = None
    contact_number: str | None = None
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8)
    remarks: str | None = None


class UserUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=150)
    address: str | None = None
    contact_number: str | None = None
    user_type: UserType | None = None
    remarks: str | None = None
    is_active: bool | None = None


class UserResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    name: str
    nic: str
    user_type: UserType
    address: str | None
    contact_number: str | None
    username: str
    remarks: str | None
    is_active: bool
    last_login_at: datetime | None
    created_at: datetime
    updated_at: datetime


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
