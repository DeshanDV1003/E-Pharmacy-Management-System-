from sqlalchemy.orm import Session, joinedload

from app.models.purchase_order import PurchaseOrder, PurchaseOrderStatus


class PurchaseOrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, po_id: int) -> PurchaseOrder | None:
        return (
            self.db.query(PurchaseOrder)
            .options(joinedload(PurchaseOrder.items))
            .filter(PurchaseOrder.id == po_id)
            .first()
        )

    def get_by_order_number(self, order_number: str) -> PurchaseOrder | None:
        return self.db.query(PurchaseOrder).filter(PurchaseOrder.order_number == order_number).first()

    def get_pending(self) -> list[PurchaseOrder]:
        return (
            self.db.query(PurchaseOrder)
            .filter(PurchaseOrder.status.in_([PurchaseOrderStatus.submitted, PurchaseOrderStatus.partially_received]))
            .order_by(PurchaseOrder.order_date.desc())
            .all()
        )

    def get_all(self, skip: int = 0, limit: int = 100) -> list[PurchaseOrder]:
        return (
            self.db.query(PurchaseOrder)
            .order_by(PurchaseOrder.order_date.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, purchase_order: PurchaseOrder) -> PurchaseOrder:
        self.db.add(purchase_order)
        self.db.commit()
        self.db.refresh(purchase_order)
        return purchase_order

    def update(self, purchase_order: PurchaseOrder) -> PurchaseOrder:
        self.db.commit()
        self.db.refresh(purchase_order)
        return purchase_order
