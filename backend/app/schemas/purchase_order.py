from datetime import date, datetime

from pydantic import BaseModel, Field

from app.models.purchase_order import PurchaseOrderStatus


class PurchaseOrderItemCreate(BaseModel):
    drug_id: int
    quantity_ordered: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)
    is_free_goods: bool = False


class PurchaseOrderItemResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    drug_id: int
    quantity_ordered: int
    quantity_received: int
    unit_price: float
    line_total: float
    is_free_goods: bool


class PurchaseOrderCreate(BaseModel):
    supplier_id: int
    order_date: date
    expected_delivery_date: date | None = None
    items: list[PurchaseOrderItemCreate] = Field(..., min_length=1)
    remarks: str | None = None


class PurchaseOrderUpdate(BaseModel):
    expected_delivery_date: date | None = None
    status: PurchaseOrderStatus | None = None
    received_date: date | None = None
    remarks: str | None = None


class PurchaseOrderResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    order_number: str
    supplier_id: int
    order_date: date
    expected_delivery_date: date | None
    received_date: date | None
    status: PurchaseOrderStatus
    remarks: str | None
    created_by_user_id: int | None
    items: list[PurchaseOrderItemResponse]
    created_at: datetime
    updated_at: datetime
