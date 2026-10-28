from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

import enum


class ReproduceType(str, enum.Enum):
    one_time = "one_time"
    recurrent = "recurrent"


class Prescription(Base):
    __tablename__ = "prescriptions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id", ondelete="RESTRICT"), nullable=False
    )
    doctor_id: Mapped[int | None] = mapped_column(
        ForeignKey("doctors.id", ondelete="SET NULL"), nullable=True
    )
    issue_date: Mapped[date] = mapped_column(Date, nullable=False)
    drug_details_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    reproduce_type: Mapped[ReproduceType] = mapped_column(
        Enum(ReproduceType), default=ReproduceType.one_time, nullable=False
    )
    valid_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    scan_file_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    customer: Mapped["Customer"] = relationship("Customer", back_populates="prescriptions")
    doctor: Mapped["Doctor"] = relationship("Doctor", back_populates="prescriptions")
    invoices: Mapped[list["Invoice"]] = relationship(
        "Invoice", back_populates="prescription"
    )
