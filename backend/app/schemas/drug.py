from datetime import date, datetime

from pydantic import BaseModel, Field

from app.models.drug import DosageForm


class DrugCreate(BaseModel):
    item_code: str = Field(..., min_length=1, max_length=50)
    brand_name: str = Field(..., min_length=1, max_length=200)
    generic_name: str = Field(..., min_length=1, max_length=200)
    active_ingredient: str | None = None
    description: str | None = None
    strength: str | None = None
    dosage_form: DosageForm
    storage_requirements: str | None = None
    batch_number: str | None = None
    manufactured_date: date | None = None
    expiry_date: date | None = None
    unit_price: float = Field(..., gt=0)
    discount: float = Field(0.00, ge=0, le=100)
    quantity: int = Field(0, ge=0)
    pack_size: int | None = Field(None, gt=0)
    low_stock_threshold: int = Field(10, ge=0)
    reorder_level: int = Field(10, ge=0)
    is_prescription_only: bool = False
    is_otc: bool = True
    is_high_alert: bool = False
    is_narcotic: bool = False
    category_id: int | None = None
    supplier_id: int | None = None


class DrugUpdate(BaseModel):
    brand_name: str | None = Field(None, min_length=1, max_length=200)
    generic_name: str | None = Field(None, min_length=1, max_length=200)
    active_ingredient: str | None = None
    description: str | None = None
    strength: str | None = None
    dosage_form: DosageForm | None = None
    storage_requirements: str | None = None
    batch_number: str | None = None
    manufactured_date: date | None = None
    expiry_date: date | None = None
    unit_price: float | None = Field(None, gt=0)
    discount: float | None = Field(None, ge=0, le=100)
    pack_size: int | None = Field(None, gt=0)
    low_stock_threshold: int | None = Field(None, ge=0)
    reorder_level: int | None = Field(None, ge=0)
    is_prescription_only: bool | None = None
    is_otc: bool | None = None
    is_high_alert: bool | None = None
    is_narcotic: bool | None = None
    is_active: bool | None = None
    category_id: int | None = None
    supplier_id: int | None = None


class DrugResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    item_code: str
    brand_name: str
    generic_name: str
    active_ingredient: str | None
    description: str | None
    strength: str | None
    dosage_form: DosageForm
    storage_requirements: str | None
    batch_number: str | None
    manufactured_date: date | None
    expiry_date: date | None
    unit_price: float
    discount: float
    quantity: int
    pack_size: int | None
    low_stock_threshold: int
    reorder_level: int
    is_prescription_only: bool
    is_otc: bool
    is_high_alert: bool
    is_narcotic: bool
    is_active: bool
    category_id: int | None
    supplier_id: int | None
    created_at: datetime
    updated_at: datetime
