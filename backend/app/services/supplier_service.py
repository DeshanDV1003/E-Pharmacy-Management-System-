from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.supplier import Supplier
from app.repositories.supplier_repository import SupplierRepository
from app.schemas.supplier import SupplierCreate, SupplierResponse, SupplierUpdate


class SupplierService:
    def __init__(self, db: Session):
        self.repo = SupplierRepository(db)

    def create_supplier(self, data: SupplierCreate) -> SupplierResponse:
        supplier = Supplier(**data.model_dump())
        return SupplierResponse.model_validate(self.repo.create(supplier))

    def get_supplier(self, supplier_id: int) -> SupplierResponse:
        supplier = self.repo.get_by_id(supplier_id)
        if not supplier:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found.")
        return SupplierResponse.model_validate(supplier)

    def list_suppliers(self, skip: int = 0, limit: int = 100) -> list[SupplierResponse]:
        return [SupplierResponse.model_validate(s) for s in self.repo.get_all(skip, limit)]

    def update_supplier(self, supplier_id: int, data: SupplierUpdate) -> SupplierResponse:
        supplier = self.repo.get_by_id(supplier_id)
        if not supplier:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found.")
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(supplier, field, value)
        return SupplierResponse.model_validate(self.repo.update(supplier))

    def delete_supplier(self, supplier_id: int) -> None:
        supplier = self.repo.get_by_id(supplier_id)
        if not supplier:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Supplier not found.")
        self.repo.delete(supplier)
