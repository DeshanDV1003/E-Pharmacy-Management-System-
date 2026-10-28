from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware.auth_middleware import require_roles
from app.models.user import User, UserType
from app.schemas.purchase_order import PurchaseOrderCreate, PurchaseOrderResponse, PurchaseOrderUpdate
from app.services.purchase_order_service import PurchaseOrderService

router = APIRouter(prefix="/api/purchase-orders", tags=["Purchase Orders"])

_supply_roles = require_roles(UserType.stock_manager, UserType.pharmacy_manager, UserType.system_administrator)


@router.post("", response_model=PurchaseOrderResponse, status_code=201)
def create_purchase_order(body: PurchaseOrderCreate, db: Session = Depends(get_db), current_user: User = Depends(_supply_roles)):
    return PurchaseOrderService(db).create_purchase_order(body, current_user.id)


@router.get("", response_model=list[PurchaseOrderResponse])
def list_purchase_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), _: User = Depends(_supply_roles)):
    return PurchaseOrderService(db).list_purchase_orders(skip, limit)


@router.get("/pending", response_model=list[PurchaseOrderResponse])
def list_pending(db: Session = Depends(get_db), _: User = Depends(_supply_roles)):
    return PurchaseOrderService(db).list_pending()


@router.get("/{po_id}", response_model=PurchaseOrderResponse)
def get_purchase_order(po_id: int, db: Session = Depends(get_db), _: User = Depends(_supply_roles)):
    return PurchaseOrderService(db).get_purchase_order(po_id)


@router.patch("/{po_id}", response_model=PurchaseOrderResponse)
def update_purchase_order(po_id: int, body: PurchaseOrderUpdate, db: Session = Depends(get_db), _: User = Depends(_supply_roles)):
    return PurchaseOrderService(db).update_purchase_order(po_id, body)
