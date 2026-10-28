from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

import enum


class MovementType(str, enum.Enum):
    purchase = "purchase"
    sale = "sale"
    adjustment = "adjustment"
    return_to_supplier = "return_to_supplier"
    transfer_in = "transfer_in"
    transfer_out = "transfer_out"


class ReferenceType(str, enum.Enum):
    invoice = "invoice"
    purchase_order = "purchase_order"
    goods_receipt = "goods_receipt"
    supplier_return = "supplier_return"
    manual = "manual"


class StockMovement(Base):
    __tablename__ = "stock_movements"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    drug_id: Mapped[int] = mapped_column(
        ForeignKey("drugs.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    movement_type: Mapped[MovementType] = mapped_column(Enum(MovementType), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_cost: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    reference_type: Mapped[ReferenceType] = mapped_column(Enum(ReferenceType), nullable=False)
    reference_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    performed_by_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), index=True
    )

    drug: Mapped["Drug"] = relationship("Drug", back_populates="stock_movements")
