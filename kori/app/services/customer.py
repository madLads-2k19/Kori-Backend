from uuid import UUID

import kori.app.dao.customer as customer_dao
from kori.app.schemas.customer import Customer, CustomerCreate, CustomerUpdate


def create(customer_data: CustomerCreate) -> Customer:
    return customer_dao.create(customer_data)


def get_customer_by_id(customer_id: UUID) -> Customer | None:
    return customer_dao.get_customer_by_id(customer_id)


def get_customer_by_number(phone_number: str) -> Customer | None:
    return customer_dao.get_customer_by_number(phone_number)


def update(customer_id: UUID, customer_data: CustomerUpdate) -> Customer:
    return customer_dao.update(customer_id, customer_data)


def delete(phone_number: str) -> None:
    return customer_dao.delete(phone_number)
