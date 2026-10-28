from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class GoodsReceipt(Base):
    __tablename__ = "goods_receipts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    grn_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    purchase_order_id: Mapped[int | None] = mapped_column(
        ForeignKey("purchase_orders.id", ondelete="SET NULL"), nullable=True
    )
    supplier_id: Mapped[int] = mapped_column(
        ForeignKey("suppliers.id", ondelete="RESTRICT"), nullable=False
    )
    received_date: Mapped[date] = mapped_column(Date, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    received_by_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    purchase_order: Mapped["PurchaseOrder"] = relationship(
        "PurchaseOrder", back_populates="goods_receipts"
    )
    items: Mapped[list["GoodsReceiptItem"]] = relationship(
        "GoodsReceiptItem", back_populates="goods_receipt", cascade="all, delete-orphan"
    )


class GoodsReceiptItem(Base):
    __tablename__ = "goods_receipt_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    goods_receipt_id: Mapped[int] = mapped_column(
        ForeignKey("goods_receipts.id", ondelete="CASCADE"), nullable=False
    )
    drug_id: Mapped[int] = mapped_column(
        ForeignKey("drugs.id", ondelete="RESTRICT"), nullable=False
    )
    quantity_received: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_cost: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    is_free_goods: Mapped[bool] = mapped_column(Boolean, default=False)
    batch_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    expiry_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    goods_receipt: Mapped["GoodsReceipt"] = relationship(
        "GoodsReceipt", back_populates="items"
    )
