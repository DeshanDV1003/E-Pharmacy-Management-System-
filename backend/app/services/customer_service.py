from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate


class CustomerService:
    def __init__(self, db: Session):
        self.repo = CustomerRepository(db)

    def create_customer(self, data: CustomerCreate) -> CustomerResponse:
        customer = Customer(**data.model_dump())
        return CustomerResponse.model_validate(self.repo.create(customer))

    def get_customer(self, customer_id: int) -> CustomerResponse:
        customer = self.repo.get_by_id(customer_id)
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found.")
        return CustomerResponse.model_validate(customer)

    def search_customers(self, query: str, skip: int = 0, limit: int = 50) -> list[CustomerResponse]:
        return [CustomerResponse.model_validate(c) for c in self.repo.search(query, skip, limit)]

    def list_customers(self, skip: int = 0, limit: int = 100) -> list[CustomerResponse]:
        return [CustomerResponse.model_validate(c) for c in self.repo.get_all(skip, limit)]

    def update_customer(self, customer_id: int, data: CustomerUpdate) -> CustomerResponse:
        customer = self.repo.get_by_id(customer_id)
        if not customer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found.")
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(customer, field, value)
        return CustomerResponse.model_validate(self.repo.update(customer))

    def add_loyalty_points(self, customer_id: int, points: float) -> None:
        customer = self.repo.get_by_id(customer_id)
        if customer:
            customer.loyalty_points = float(customer.loyalty_points) + points
            self.repo.update(customer)
