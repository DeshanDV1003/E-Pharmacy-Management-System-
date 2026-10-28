from sqlalchemy.orm import Session

from app.models.prescription import Prescription


class PrescriptionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, prescription_id: int) -> Prescription | None:
        return self.db.get(Prescription, prescription_id)

    def get_by_customer(self, customer_id: int, skip: int = 0, limit: int = 50) -> list[Prescription]:
        return (
            self.db.query(Prescription)
            .filter(Prescription.customer_id == customer_id)
            .order_by(Prescription.issue_date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, prescription: Prescription) -> Prescription:
        self.db.add(prescription)
        self.db.commit()
        self.db.refresh(prescription)
        return prescription

    def update(self, prescription: Prescription) -> Prescription:
        self.db.commit()
        self.db.refresh(prescription)
        return prescription
