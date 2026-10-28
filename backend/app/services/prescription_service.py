from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.models.prescription import Prescription
from app.repositories.prescription_repository import PrescriptionRepository
from app.schemas.prescription import PrescriptionCreate, PrescriptionResponse, PrescriptionUpdate
from app.utils.file_utils import delete_file, save_upload_file


class PrescriptionService:
    def __init__(self, db: Session):
        self.repo = PrescriptionRepository(db)

    def create_prescription(self, data: PrescriptionCreate) -> PrescriptionResponse:
        prescription = Prescription(**data.model_dump())
        return PrescriptionResponse.model_validate(self.repo.create(prescription))

    def upload_scan(self, prescription_id: int, file: UploadFile) -> PrescriptionResponse:
        prescription = self.repo.get_by_id(prescription_id)
        if not prescription:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prescription not found.")

        if prescription.scan_file_path:
            delete_file(prescription.scan_file_path)

        prescription.scan_file_path = save_upload_file(file, subfolder="prescriptions")
        return PrescriptionResponse.model_validate(self.repo.update(prescription))

    def get_prescription(self, prescription_id: int) -> PrescriptionResponse:
        prescription = self.repo.get_by_id(prescription_id)
        if not prescription:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prescription not found.")
        return PrescriptionResponse.model_validate(prescription)

    def get_by_customer(self, customer_id: int, skip: int = 0, limit: int = 50) -> list[PrescriptionResponse]:
        return [PrescriptionResponse.model_validate(p) for p in self.repo.get_by_customer(customer_id, skip, limit)]

    def update_prescription(self, prescription_id: int, data: PrescriptionUpdate) -> PrescriptionResponse:
        prescription = self.repo.get_by_id(prescription_id)
        if not prescription:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prescription not found.")
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(prescription, field, value)
        return PrescriptionResponse.model_validate(self.repo.update(prescription))
