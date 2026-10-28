from datetime import datetime

from pydantic import BaseModel, Field

from app.models.invoice import InvoiceStatus, PaymentMode


class InvoiceItemCreate(BaseModel):
    drug_id: int
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)
    discount_rate: float = Field(0.00, ge=0, le=100)


class InvoiceItemResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    drug_id: int
    quantity: int
    unit_price: float
    discount_rate: float
    discount_amount: float
    line_total: float


class InvoiceCreate(BaseModel):
    customer_id: int | None = None
    doctor_id: int | None = None
    prescription_id: int | None = None
    items: list[InvoiceItemCreate] = Field(..., min_length=1)
    discount_amount: float = Field(0.00, ge=0)
    tax_rate: float = Field(0.00, ge=0)
    payment_mode: PaymentMode
    notes: str | None = None


class InvoiceCancelRequest(BaseModel):
    cancellation_reason: str = Field(..., min_length=1)


class InvoiceResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    invoice_number: str
    customer_id: int | None
    doctor_id: int | None
    prescription_id: int | None
    subtotal: float
    discount_amount: float
    tax_rate: float
    tax_amount: float
    total_amount: float
    payment_mode: PaymentMode
    status: InvoiceStatus
    notes: str | None
    cancelled_at: datetime | None
    cancellation_reason: str | None
    served_by_user_id: int | None
    items: list[InvoiceItemResponse]
    created_at: datetime
    updated_at: datetime
