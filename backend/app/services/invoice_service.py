import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.invoice import Invoice, InvoiceItem, InvoiceStatus
from app.models.stock_movement import MovementType, ReferenceType, StockMovement
from app.repositories.drug_repository import DrugRepository
from app.repositories.invoice_repository import InvoiceRepository
from app.schemas.invoice import InvoiceCancelRequest, InvoiceCreate, InvoiceResponse


class InvoiceService:
    def __init__(self, db: Session):
        self.repo = InvoiceRepository(db)
        self.drug_repo = DrugRepository(db)
        self.db = db

    def create_invoice(self, data: InvoiceCreate, served_by: int) -> InvoiceResponse:
        subtotal = 0.0
        items = []

        for item_data in data.items:
            drug = self.drug_repo.get_by_id(item_data.drug_id)
            if not drug or not drug.is_active:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Drug ID {item_data.drug_id} not found.")
            if drug.quantity < item_data.quantity:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Insufficient stock for '{drug.brand_name}'.")

            discount_amount = round(item_data.unit_price * item_data.quantity * (item_data.discount_rate / 100), 2)
            line_total = round(item_data.unit_price * item_data.quantity - discount_amount, 2)
            subtotal += line_total

            items.append(InvoiceItem(
                drug_id=item_data.drug_id,
                quantity=item_data.quantity,
                unit_price=item_data.unit_price,
                discount_rate=item_data.discount_rate,
                discount_amount=discount_amount,
                line_total=line_total,
            ))

            drug.quantity -= item_data.quantity
            self.db.add(StockMovement(
                drug_id=drug.id,
                movement_type=MovementType.sale,
                quantity=-item_data.quantity,
                unit_cost=item_data.unit_price,
                reference_type=ReferenceType.invoice,
                performed_by_user_id=served_by,
            ))

        after_discount = round(subtotal - data.discount_amount, 2)
        tax_amount = round(after_discount * (data.tax_rate / 100), 2)
        total_amount = round(after_discount + tax_amount, 2)

        invoice = Invoice(
            invoice_number=f"INV-{uuid.uuid4().hex[:8].upper()}",
            customer_id=data.customer_id,
            doctor_id=data.doctor_id,
            prescription_id=data.prescription_id,
            subtotal=subtotal,
            discount_amount=data.discount_amount,
            tax_rate=data.tax_rate,
            tax_amount=tax_amount,
            total_amount=total_amount,
            payment_mode=data.payment_mode,
            notes=data.notes,
            served_by_user_id=served_by,
            items=items,
        )

        created = self.repo.create(invoice)
        for movement in self.db.new:
            if isinstance(movement, StockMovement):
                movement.reference_id = created.id

        self.db.commit()
        self.db.refresh(created)
        return InvoiceResponse.model_validate(created)

    def get_invoice(self, invoice_id: int) -> InvoiceResponse:
        invoice = self.repo.get_by_id(invoice_id)
        if not invoice:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found.")
        return InvoiceResponse.model_validate(invoice)

    def cancel_invoice(self, invoice_id: int, data: InvoiceCancelRequest, cancelled_by: int) -> InvoiceResponse:
        invoice = self.repo.get_by_id(invoice_id)
        if not invoice:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice not found.")
        if invoice.status == InvoiceStatus.cancelled:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invoice is already cancelled.")

        for item in invoice.items:
            drug = self.drug_repo.get_by_id(item.drug_id)
            if drug:
                drug.quantity += item.quantity
                self.db.add(StockMovement(
                    drug_id=drug.id,
                    movement_type=MovementType.adjustment,
                    quantity=item.quantity,
                    unit_cost=item.unit_price,
                    reference_type=ReferenceType.invoice,
                    reference_id=invoice.id,
                    notes=f"Reversal for cancelled invoice {invoice.invoice_number}",
                    performed_by_user_id=cancelled_by,
                ))

        invoice.status = InvoiceStatus.cancelled
        invoice.cancelled_at = datetime.now(timezone.utc)
        invoice.cancellation_reason = data.cancellation_reason
        return InvoiceResponse.model_validate(self.repo.update(invoice))

    def get_by_customer(self, customer_id: int, skip: int = 0, limit: int = 50) -> list[InvoiceResponse]:
        return [InvoiceResponse.model_validate(i) for i in self.repo.get_by_customer(customer_id, skip, limit)]
