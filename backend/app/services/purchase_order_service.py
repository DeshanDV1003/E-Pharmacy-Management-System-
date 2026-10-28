import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.purchase_order import PurchaseOrder, PurchaseOrderItem, PurchaseOrderStatus
from app.repositories.drug_repository import DrugRepository
from app.repositories.purchase_order_repository import PurchaseOrderRepository
from app.schemas.purchase_order import PurchaseOrderCreate, PurchaseOrderResponse, PurchaseOrderUpdate


class PurchaseOrderService:
    def __init__(self, db: Session):
        self.repo = PurchaseOrderRepository(db)
        self.drug_repo = DrugRepository(db)

    def create_purchase_order(self, data: PurchaseOrderCreate, created_by: int) -> PurchaseOrderResponse:
        items = []
        for item_data in data.items:
            drug = self.drug_repo.get_by_id(item_data.drug_id)
            if not drug:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Drug ID {item_data.drug_id} not found.")
            line_total = round(item_data.quantity_ordered * item_data.unit_price, 2)
            items.append(PurchaseOrderItem(
                drug_id=item_data.drug_id,
                quantity_ordered=item_data.quantity_ordered,
                unit_price=item_data.unit_price,
                line_total=line_total,
                is_free_goods=item_data.is_free_goods,
            ))

        po = PurchaseOrder(
            order_number=f"PO-{uuid.uuid4().hex[:8].upper()}",
            supplier_id=data.supplier_id,
            order_date=data.order_date,
            expected_delivery_date=data.expected_delivery_date,
            remarks=data.remarks,
            created_by_user_id=created_by,
            items=items,
        )
        return PurchaseOrderResponse.model_validate(self.repo.create(po))

    def get_purchase_order(self, po_id: int) -> PurchaseOrderResponse:
        po = self.repo.get_by_id(po_id)
        if not po:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase order not found.")
        return PurchaseOrderResponse.model_validate(po)

    def list_purchase_orders(self, skip: int = 0, limit: int = 100) -> list[PurchaseOrderResponse]:
        return [PurchaseOrderResponse.model_validate(p) for p in self.repo.get_all(skip, limit)]

    def list_pending(self) -> list[PurchaseOrderResponse]:
        return [PurchaseOrderResponse.model_validate(p) for p in self.repo.get_pending()]

    def update_purchase_order(self, po_id: int, data: PurchaseOrderUpdate) -> PurchaseOrderResponse:
        po = self.repo.get_by_id(po_id)
        if not po:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase order not found.")
        if po.status == PurchaseOrderStatus.cancelled:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot update a cancelled order.")
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(po, field, value)
        return PurchaseOrderResponse.model_validate(self.repo.update(po))
