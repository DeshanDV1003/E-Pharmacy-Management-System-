from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.drug import Drug
from app.models.price_adjustment import PriceAdjustment
from app.repositories.drug_repository import DrugRepository
from app.schemas.drug import DrugCreate, DrugResponse, DrugUpdate


class DrugService:
    def __init__(self, db: Session):
        self.repo = DrugRepository(db)
        self.db = db

    def create_drug(self, data: DrugCreate) -> DrugResponse:
        if self.repo.get_by_item_code(data.item_code):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Item code already exists.")
        drug = Drug(**data.model_dump())
        return DrugResponse.model_validate(self.repo.create(drug))

    def get_drug(self, drug_id: int) -> DrugResponse:
        drug = self.repo.get_by_id(drug_id)
        if not drug:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Drug not found.")
        return DrugResponse.model_validate(drug)

    def search_drugs(self, query: str, skip: int = 0, limit: int = 50) -> list[DrugResponse]:
        return [DrugResponse.model_validate(d) for d in self.repo.search(query, skip, limit)]

    def list_drugs(self, skip: int = 0, limit: int = 100) -> list[DrugResponse]:
        return [DrugResponse.model_validate(d) for d in self.repo.get_all(skip, limit)]

    def update_drug(self, drug_id: int, data: DrugUpdate, updated_by: int) -> DrugResponse:
        drug = self.repo.get_by_id(drug_id)
        if not drug:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Drug not found.")

        if data.unit_price is not None and data.unit_price != float(drug.unit_price):
            adjustment = PriceAdjustment(
                drug_id=drug_id,
                old_price=drug.unit_price,
                new_price=data.unit_price,
                adjusted_by_user_id=updated_by,
            )
            self.db.add(adjustment)

        for field, value in data.model_dump(exclude_none=True).items():
            setattr(drug, field, value)

        return DrugResponse.model_validate(self.repo.update(drug))

    def get_low_stock(self) -> list[DrugResponse]:
        return [DrugResponse.model_validate(d) for d in self.repo.get_low_stock()]
