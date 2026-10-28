from sqlalchemy.orm import Session

from app.models.customer import Customer


class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, customer_id: int) -> Customer | None:
        return self.db.get(Customer, customer_id)

    def get_by_contact_number(self, contact_number: str) -> Customer | None:
        return self.db.query(Customer).filter(Customer.contact_number == contact_number).first()

    def search(self, query: str, skip: int = 0, limit: int = 50) -> list[Customer]:
        return (
            self.db.query(Customer)
            .filter(Customer.contact_number.ilike(f"%{query}%") | Customer.name.ilike(f"%{query}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Customer]:
        return self.db.query(Customer).offset(skip).limit(limit).all()

    def create(self, customer: Customer) -> Customer:
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def update(self, customer: Customer) -> Customer:
        self.db.commit()
        self.db.refresh(customer)
        return customer
