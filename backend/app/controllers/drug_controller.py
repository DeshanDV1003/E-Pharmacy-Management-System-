from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware.auth_middleware import get_current_user, require_roles
from app.models.user import User, UserType
from app.schemas.drug import DrugCreate, DrugResponse, DrugUpdate
from app.services.drug_service import DrugService

router = APIRouter(prefix="/api/drugs", tags=["Drugs"])

_inventory_roles = require_roles(UserType.stock_manager, UserType.pharmacy_manager, UserType.system_administrator)


@router.post("", response_model=DrugResponse, status_code=201)
def create_drug(body: DrugCreate, db: Session = Depends(get_db), _: User = Depends(_inventory_roles)):
    return DrugService(db).create_drug(body)


@router.get("", response_model=list[DrugResponse])
def list_drugs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return DrugService(db).list_drugs(skip, limit)


@router.get("/search", response_model=list[DrugResponse])
def search_drugs(q: str, skip: int = 0, limit: int = 50, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return DrugService(db).search_drugs(q, skip, limit)


@router.get("/low-stock", response_model=list[DrugResponse])
def low_stock(db: Session = Depends(get_db), _: User = Depends(_inventory_roles)):
    return DrugService(db).get_low_stock()


@router.get("/{drug_id}", response_model=DrugResponse)
def get_drug(drug_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return DrugService(db).get_drug(drug_id)


@router.patch("/{drug_id}", response_model=DrugResponse)
def update_drug(drug_id: int, body: DrugUpdate, db: Session = Depends(get_db), current_user: User = Depends(_inventory_roles)):
    return DrugService(db).update_drug(drug_id, body, current_user.id)
