from uuid import UUID

import kori.app.dao.customer as customer_dao
from kori.app.core.exceptions import NotFoundException
from kori.app.schemas.customer import CustomerCreate, CustomerCreateRequest, CustomerSchema, CustomerUpdate


def create(org_id: UUID, customer_data: CustomerCreateRequest) -> CustomerSchema:
    customer_create = CustomerCreate(org_id=org_id, **customer_data.dict())
    return customer_dao.create(customer_create)


def get_customer_by_id(customer_id: UUID) -> CustomerSchema:
    customer = customer_dao.get_customer_by_id(customer_id)
    if not customer:
        raise NotFoundException(message="Customer not found")
    return customer


def get_customers_in_org(
    org_id: UUID, customer_name: str | None = None, phone_number: str | None = None
) -> list[CustomerSchema]:
    return customer_dao.get_customers_in_org(org_id, customer_name, phone_number)


def get_customer_by_number(phone_number: str) -> CustomerSchema:
    customer = customer_dao.get_customer_by_number(phone_number)
    if not customer:
        raise NotFoundException(message="Customer not found")
    return customer


def update(customer_id: UUID, customer_data: CustomerUpdate) -> CustomerSchema | None:
    customer = customer_dao.update(customer_id, customer_data)
    if not customer:
        raise NotFoundException(message="Customer not found")
    return customer


def delete(customer_id: UUID) -> None:
    return customer_dao.delete(customer_id)
