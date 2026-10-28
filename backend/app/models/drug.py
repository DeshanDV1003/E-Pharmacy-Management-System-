from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

import enum


class DosageForm(str, enum.Enum):
    syrup = "syrup"
    tablet = "tablet"
    capsule = "capsule"
    vial = "vial"
    other = "other"


class Drug(Base):
    __tablename__ = "drugs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    item_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    brand_name: Mapped[str] = mapped_column(String(200), nullable=False)
    generic_name: Mapped[str] = mapped_column(String(200), nullable=False)
    active_ingredient: Mapped[str | None] = mapped_column(String(200), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    strength: Mapped[str | None] = mapped_column(String(50), nullable=True)
    dosage_form: Mapped[DosageForm] = mapped_column(Enum(DosageForm), nullable=False)
    batch_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    manufactured_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    expiry_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    unit_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    discount: Mapped[float] = mapped_column(Numeric(5, 2), default=0.00)
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    pack_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    low_stock_threshold: Mapped[int] = mapped_column(Integer, default=10)
    is_prescription_only: Mapped[bool] = mapped_column(Boolean, default=False)
    is_otc: Mapped[bool] = mapped_column(Boolean, default=True)
    is_high_alert: Mapped[bool] = mapped_column(Boolean, default=False)
    is_narcotic: Mapped[bool] = mapped_column(Boolean, default=False)
    supplier_id: Mapped[int | None] = mapped_column(
        ForeignKey("suppliers.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    supplier: Mapped["Supplier"] = relationship("Supplier", back_populates="drugs")
