from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    slmc_registration_number: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    specialization: Mapped[str | None] = mapped_column(String(100), nullable=True)
    contact_number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(150), nullable=True)
    hospital: Mapped[str | None] = mapped_column(String(200), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    prescriptions: Mapped[list["Prescription"]] = relationship(
        "Prescription", back_populates="doctor"
    )
    invoices: Mapped[list["Invoice"]] = relationship(
        "Invoice", back_populates="doctor"
    )
