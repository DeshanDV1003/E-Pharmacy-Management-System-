from datetime import datetime

from pydantic import BaseModel, Field


class SupplierCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    address: str | None = None
    contact_number: str | None = None
    special_remarks: str | None = None


class SupplierUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=200)
    address: str | None = None
    contact_number: str | None = None
    special_remarks: str | None = None


class SupplierResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    name: str
    address: str | None
    contact_number: str | None
    special_remarks: str | None
    created_at: datetime
    updated_at: datetime
