from uuid import UUID

from fastapi import APIRouter

import kori.app.services.customer as customer_service
from kori.app.core.config import Settings
from kori.app.schemas.customer import CustomerCreateRequest, CustomerSchema, CustomerUpdate

customer_router = APIRouter()
config = Settings()


@customer_router.post("/{organization_id}", response_model=CustomerSchema)
def register_customer(organization_id: UUID, customer_data: CustomerCreateRequest) -> CustomerSchema:
    return customer_service.create(organization_id, customer_data)


@customer_router.get("/{customer_id}", response_model=CustomerSchema)
def get_customer_by_id(customer_id: UUID) -> CustomerSchema:
    return customer_service.get_customer_by_id(customer_id)


@customer_router.get("/number/{phone_number}", response_model=CustomerSchema)
def get_customer_by_phone_number(phone_number: str) -> CustomerSchema:
    return customer_service.get_customer_by_number(phone_number)


@customer_router.put("/{customer_id}", response_model=CustomerSchema)
def update_customer(customer_id: UUID, customer_data: CustomerUpdate) -> CustomerSchema:
    return customer_service.update(customer_id, customer_data)


@customer_router.delete("/{customer_id}")
def delete_customer(customer_id: UUID):
    customer_service.delete(customer_id)
    return "Deleted"
