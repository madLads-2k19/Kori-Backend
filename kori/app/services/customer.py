from uuid import UUID

import kori.app.dao.customer as customer_dao
from kori.app.schemas.customer import CustomerCreate, CustomerCreateRequest, CustomerSchema, CustomerUpdate


def create(org_id: UUID, customer_data: CustomerCreateRequest) -> CustomerSchema:
    customer_create = CustomerCreate(org_id=org_id, **customer_data.dict())
    return customer_dao.create(customer_create)


def get_customer_by_id(customer_id: UUID) -> CustomerSchema | None:
    return customer_dao.get_customer_by_id(customer_id)


def get_customer_by_number(phone_number: str) -> CustomerSchema | None:
    return customer_dao.get_customer_by_number(phone_number)


def update(customer_id: UUID, customer_data: CustomerUpdate) -> CustomerSchema:
    return customer_dao.update(customer_id, customer_data)


def delete(customer_id: UUID) -> None:
    return customer_dao.delete(customer_id)
