from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware.auth_middleware import get_current_user
from app.models.user import User
from app.schemas.invoice import InvoiceCancelRequest, InvoiceCreate, InvoiceResponse
from app.services.invoice_service import InvoiceService

router = APIRouter(prefix="/api/invoices", tags=["Invoices"])


@router.post("", response_model=InvoiceResponse, status_code=201)
def create_invoice(body: InvoiceCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return InvoiceService(db).create_invoice(body, current_user.id)


@router.get("/customer/{customer_id}", response_model=list[InvoiceResponse])
def get_by_customer(customer_id: int, skip: int = 0, limit: int = 50, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return InvoiceService(db).get_by_customer(customer_id, skip, limit)


@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return InvoiceService(db).get_invoice(invoice_id)


@router.post("/{invoice_id}/cancel", response_model=InvoiceResponse)
def cancel_invoice(invoice_id: int, body: InvoiceCancelRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return InvoiceService(db).cancel_invoice(invoice_id, body, current_user.id)
