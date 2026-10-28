from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware.auth_middleware import get_current_user
from app.models.user import User
from app.schemas.prescription import PrescriptionCreate, PrescriptionResponse, PrescriptionUpdate
from app.services.prescription_service import PrescriptionService

router = APIRouter(prefix="/api/prescriptions", tags=["Prescriptions"])


@router.post("", response_model=PrescriptionResponse, status_code=201)
def create_prescription(body: PrescriptionCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return PrescriptionService(db).create_prescription(body)


@router.post("/{prescription_id}/scan", response_model=PrescriptionResponse)
def upload_scan(prescription_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return PrescriptionService(db).upload_scan(prescription_id, file)


@router.get("/customer/{customer_id}", response_model=list[PrescriptionResponse])
def get_by_customer(customer_id: int, skip: int = 0, limit: int = 50, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return PrescriptionService(db).get_by_customer(customer_id, skip, limit)


@router.get("/{prescription_id}", response_model=PrescriptionResponse)
def get_prescription(prescription_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return PrescriptionService(db).get_prescription(prescription_id)


@router.patch("/{prescription_id}", response_model=PrescriptionResponse)
def update_prescription(prescription_id: int, body: PrescriptionUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return PrescriptionService(db).update_prescription(prescription_id, body)
