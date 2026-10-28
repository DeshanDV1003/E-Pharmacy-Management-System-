from sqlalchemy.orm import Session

from app.models.drug import Drug


class DrugRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, drug_id: int) -> Drug | None:
        return self.db.get(Drug, drug_id)

    def get_by_item_code(self, item_code: str) -> Drug | None:
        return self.db.query(Drug).filter(Drug.item_code == item_code).first()

    def search(self, query: str, skip: int = 0, limit: int = 50) -> list[Drug]:
        return (
            self.db.query(Drug)
            .filter(
                Drug.item_code.ilike(f"%{query}%")
                | Drug.brand_name.ilike(f"%{query}%")
                | Drug.generic_name.ilike(f"%{query}%")
            )
            .filter(Drug.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_all(self, skip: int = 0, limit: int = 100, active_only: bool = True) -> list[Drug]:
        q = self.db.query(Drug)
        if active_only:
            q = q.filter(Drug.is_active == True)
        return q.offset(skip).limit(limit).all()

    def get_low_stock(self) -> list[Drug]:
        return (
            self.db.query(Drug)
            .filter(Drug.quantity <= Drug.low_stock_threshold, Drug.is_active == True)
            .all()
        )

    def create(self, drug: Drug) -> Drug:
        self.db.add(drug)
        self.db.commit()
        self.db.refresh(drug)
        return drug

    def update(self, drug: Drug) -> Drug:
        self.db.commit()
        self.db.refresh(drug)
        return drug
