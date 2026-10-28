from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.doctor import Doctor
from app.repositories.doctor_repository import DoctorRepository
from app.schemas.doctor import DoctorCreate, DoctorResponse, DoctorUpdate


class DoctorService:
    def __init__(self, db: Session):
        self.repo = DoctorRepository(db)

    def create_doctor(self, data: DoctorCreate) -> DoctorResponse:
        if self.repo.get_by_slmc(data.slmc_registration_number):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="SLMC registration number already exists.")
        doctor = Doctor(**data.model_dump())
        return DoctorResponse.model_validate(self.repo.create(doctor))

    def get_doctor(self, doctor_id: int) -> DoctorResponse:
        doctor = self.repo.get_by_id(doctor_id)
        if not doctor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found.")
        return DoctorResponse.model_validate(doctor)

    def search_doctors(self, query: str, skip: int = 0, limit: int = 50) -> list[DoctorResponse]:
        return [DoctorResponse.model_validate(d) for d in self.repo.search(query, skip, limit)]

    def list_doctors(self, skip: int = 0, limit: int = 100) -> list[DoctorResponse]:
        return [DoctorResponse.model_validate(d) for d in self.repo.get_all(skip, limit)]

    def update_doctor(self, doctor_id: int, data: DoctorUpdate) -> DoctorResponse:
        doctor = self.repo.get_by_id(doctor_id)
        if not doctor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found.")
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(doctor, field, value)
        return DoctorResponse.model_validate(self.repo.update(doctor))
