from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware.auth_middleware import require_roles
from app.models.user import User, UserType
from app.schemas.supplier import SupplierCreate, SupplierResponse, SupplierUpdate
from app.services.supplier_service import SupplierService

router = APIRouter(prefix="/api/suppliers", tags=["Suppliers"])

_supply_roles = require_roles(UserType.stock_manager, UserType.pharmacy_manager, UserType.system_administrator)


@router.post("", response_model=SupplierResponse, status_code=201)
def create_supplier(body: SupplierCreate, db: Session = Depends(get_db), _: User = Depends(_supply_roles)):
    return SupplierService(db).create_supplier(body)


@router.get("", response_model=list[SupplierResponse])
def list_suppliers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _: User = Depends(_supply_roles)):
    return SupplierService(db).list_suppliers(skip, limit)


@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier(supplier_id: int, db: Session = Depends(get_db), _: User = Depends(_supply_roles)):
    return SupplierService(db).get_supplier(supplier_id)


@router.patch("/{supplier_id}", response_model=SupplierResponse)
def update_supplier(supplier_id: int, body: SupplierUpdate, db: Session = Depends(get_db), _: User = Depends(_supply_roles)):
    return SupplierService(db).update_supplier(supplier_id, body)


@router.delete("/{supplier_id}", status_code=204)
def delete_supplier(supplier_id: int, db: Session = Depends(get_db), _: User = Depends(_supply_roles)):
    SupplierService(db).delete_supplier(supplier_id)
