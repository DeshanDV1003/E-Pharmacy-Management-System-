from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class SupplierReturn(Base):
    __tablename__ = "supplier_returns"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    return_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("suppliers.id", ondelete="RESTRICT"), nullable=False
    )
    return_date: Mapped[date] = mapped_column(Date, nullable=False)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    processed_by_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    items: Mapped[list["SupplierReturnItem"]] = relationship(
        "SupplierReturnItem", back_populates="supplier_return", cascade="all, delete-orphan"
    )


class SupplierReturnItem(Base):
    __tablename__ = "supplier_return_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    supplier_return_id: Mapped[int] = mapped_column(
        ForeignKey("supplier_returns.id", ondelete="CASCADE"), nullable=False
    )
    drug_id: Mapped[int] = mapped_column(
        ForeignKey("drugs.id", ondelete="RESTRICT"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_cost: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    supplier_return: Mapped["SupplierReturn"] = relationship(
        "SupplierReturn", back_populates="items"
    )
