from datetime import date, datetime

from pydantic import BaseModel, Field

from app.models.customer import Gender


class CustomerCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    contact_number: str = Field(..., min_length=1, max_length=20)
    email: str | None = None
    address: str | None = None
    dob: date | None = None
    gender: Gender | None = None
    discount_rate: float = Field(0.00, ge=0, le=100)
    clinical_remarks: str | None = None


class CustomerUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=150)
    contact_number: str | None = Field(None, min_length=1, max_length=20)
    email: str | None = None
    address: str | None = None
    dob: date | None = None
    gender: Gender | None = None
    discount_rate: float | None = Field(None, ge=0, le=100)
    clinical_remarks: str | None = None
    is_active: bool | None = None


class CustomerResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    name: str
    contact_number: str
    email: str | None
    address: str | None
    dob: date | None
    gender: Gender | None
    loyalty_points: float
    discount_rate: float
    clinical_remarks: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
