from sqlalchemy.orm import Session

from app.models.doctor import Doctor


class DoctorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, doctor_id: int) -> Doctor | None:
        return self.db.get(Doctor, doctor_id)

    def get_by_slmc(self, slmc_number: str) -> Doctor | None:
        return self.db.query(Doctor).filter(Doctor.slmc_registration_number == slmc_number).first()

    def search(self, query: str, skip: int = 0, limit: int = 50) -> list[Doctor]:
        return (
            self.db.query(Doctor)
            .filter(Doctor.name.ilike(f"%{query}%") | Doctor.slmc_registration_number.ilike(f"%{query}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Doctor]:
        return self.db.query(Doctor).offset(skip).limit(limit).all()

    def create(self, doctor: Doctor) -> Doctor:
        self.db.add(doctor)
        self.db.commit()
        self.db.refresh(doctor)
        return doctor

    def update(self, doctor: Doctor) -> Doctor:
        self.db.commit()
        self.db.refresh(doctor)
        return doctor
