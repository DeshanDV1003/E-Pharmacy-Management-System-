from datetime import date

from sqlalchemy.orm import Session, joinedload

from app.models.invoice import Invoice, InvoiceStatus


class InvoiceRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, invoice_id: int) -> Invoice | None:
        return (
            self.db.query(Invoice)
            .options(joinedload(Invoice.items))
            .filter(Invoice.id == invoice_id)
            .first()
        )

    def get_by_invoice_number(self, invoice_number: str) -> Invoice | None:
        return self.db.query(Invoice).filter(Invoice.invoice_number == invoice_number).first()

    def get_by_customer(self, customer_id: int, skip: int = 0, limit: int = 50) -> list[Invoice]:
        return (
            self.db.query(Invoice)
            .filter(Invoice.customer_id == customer_id)
            .order_by(Invoice.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_date_range(self, start: date, end: date) -> list[Invoice]:
        return (
            self.db.query(Invoice)
            .filter(Invoice.created_at >= start, Invoice.created_at <= end)
            .order_by(Invoice.created_at.desc())
            .all()
        )

    def get_cancelled(self) -> list[Invoice]:
        return (
            self.db.query(Invoice)
            .filter(Invoice.status == InvoiceStatus.cancelled)
            .order_by(Invoice.cancelled_at.desc())
            .all()
        )

    def create(self, invoice: Invoice) -> Invoice:
        self.db.add(invoice)
        self.db.commit()
        self.db.refresh(invoice)
        return invoice

    def update(self, invoice: Invoice) -> Invoice:
        self.db.commit()
        self.db.refresh(invoice)
        return invoice
