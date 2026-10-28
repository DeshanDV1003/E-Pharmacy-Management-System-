from datetime import date, datetime

from sqlalchemy import Date, DateTime, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    contact_number: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    dob: Mapped[date | None] = mapped_column(Date, nullable=True)
    loyalty_points: Mapped[float] = mapped_column(Numeric(10, 2), default=0.00)
    discount_rate: Mapped[float] = mapped_column(Numeric(5, 2), default=0.00)
    clinical_remarks: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    prescriptions: Mapped[list["Prescription"]] = relationship(
        "Prescription", back_populates="customer"
    )
    invoices: Mapped[list["Invoice"]] = relationship(
        "Invoice", back_populates="customer"
    )
