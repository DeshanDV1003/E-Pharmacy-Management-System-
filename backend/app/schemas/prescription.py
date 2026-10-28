from datetime import date, datetime

from pydantic import BaseModel, Field

from app.models.prescription import ReproduceType


class PrescriptionCreate(BaseModel):
    customer_id: int
    doctor_id: int | None = None
    issue_date: date
    drug_details_text: str | None = None
    reproduce_type: ReproduceType = ReproduceType.one_time
    valid_days: int | None = Field(None, gt=0)
    valid_months: int | None = Field(None, gt=0)


class PrescriptionUpdate(BaseModel):
    doctor_id: int | None = None
    drug_details_text: str | None = None
    reproduce_type: ReproduceType | None = None
    valid_days: int | None = Field(None, gt=0)
    valid_months: int | None = Field(None, gt=0)
    is_active: bool | None = None


class PrescriptionResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    customer_id: int
    doctor_id: int | None
    issue_date: date
    drug_details_text: str | None
    reproduce_type: ReproduceType
    valid_days: int | None
    valid_months: int | None
    scan_file_path: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime
