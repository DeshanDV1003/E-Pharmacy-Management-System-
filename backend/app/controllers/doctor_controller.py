from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware.auth_middleware import get_current_user
from app.models.user import User
from app.schemas.doctor import DoctorCreate, DoctorResponse, DoctorUpdate
from app.services.doctor_service import DoctorService

router = APIRouter(prefix="/api/doctors", tags=["Doctors"])


@router.post("", response_model=DoctorResponse, status_code=201)
def create_doctor(body: DoctorCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return DoctorService(db).create_doctor(body)


@router.get("", response_model=list[DoctorResponse])
def list_doctors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return DoctorService(db).list_doctors(skip, limit)


@router.get("/search", response_model=list[DoctorResponse])
def search_doctors(q: str, skip: int = 0, limit: int = 50, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return DoctorService(db).search_doctors(q, skip, limit)


@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(doctor_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return DoctorService(db).get_doctor(doctor_id)


@router.patch("/{doctor_id}", response_model=DoctorResponse)
def update_doctor(doctor_id: int, body: DoctorUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return DoctorService(db).update_doctor(doctor_id, body)
