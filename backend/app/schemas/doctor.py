from datetime import datetime

from pydantic import BaseModel, Field


class DoctorCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=150)
    slmc_registration_number: str = Field(..., min_length=1, max_length=50)
    specialization: str | None = None
    contact_number: str | None = None
    email: str | None = None
    hospital: str | None = None


class DoctorUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=150)
    specialization: str | None = None
    contact_number: str | None = None
    email: str | None = None
    hospital: str | None = None


class DoctorResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    name: str
    slmc_registration_number: str
    specialization: str | None
    contact_number: str | None
    email: str | None
    hospital: str | None
    created_at: datetime
    updated_at: datetime
