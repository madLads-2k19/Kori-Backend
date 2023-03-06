from uuid import UUID, uuid4

from fastapi import APIRouter

import kori.app.services.customer as customer_service
from kori.app.core.config import Settings
from kori.app.schemas.customer import Customer, CustomerCreate, CustomerUpdate

customer_router = APIRouter()
settings = Settings()


@customer_router.post("/", response_model=Customer)
def register_customer(customer_data: CustomerCreate) -> Customer:
    return customer_service.create(customer_data)
    # return Customer(
    #     id=uuid4(),
    #     **customer_data.dict(),
    # )


@customer_router.get("/{customer_id}", response_model=Customer)
def get_customer_by_id(customer_id: UUID) -> Customer:
    return customer_service.get_customer_by_id(customer_id)
    # return Customer.parse_obj(
    #     {
    #         "org_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    #         "email": "user@example.com",
    #         "is_member": False,
    #         "membership_points": 0,
    #         "address": "string",
    #         "preferred_payment_method": "string",
    #         "name": "string",
    #         "phone_number": "string",
    #         "id": "b6d47eb3-2bd2-4f8a-b565-e4ea162f965d"
    #     }
    # )


@customer_router.get("/{phone_number}", response_model=Customer)
def get_customer_by_phone_number(phone_number: str) -> Customer:
    return customer_service.get_customer_by_number(phone_number)
    # return Customer.parse_obj(
    #     {
    #         "org_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    #         "email": "user@example.com",
    #         "is_member": False,
    #         "membership_points": 0,
    #         "address": "string",
    #         "preferred_payment_method": "string",
    #         "name": "string",
    #         "phone_number": "string",
    #         "id": "b6d47eb3-2bd2-4f8a-b565-e4ea162f965d"
    #     }
    # )


@customer_router.put("/{customer_id}", response_model=Customer)
def update_customer(customer_id: UUID, customer_data: CustomerUpdate) -> Customer:
    return customer_service.update(customer_id, customer_data)
    # return Customer.parse_obj(
    #     {
    #         "org_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    #         "email": "user@example.com",
    #         "is_member": False,
    #         "membership_points": 0,
    #         "address": "string",
    #         "preferred_payment_method": "string",
    #         "name": "string",
    #         "phone_number": "string",
    #         "id": "b6d47eb3-2bd2-4f8a-b565-e4ea162f965d"
    #     }
    # )


@customer_router.delete("/{phone_number}")
def delete_customer(phone_number: str):
    customer_service.delete(phone_number)
    return "Deleted"
