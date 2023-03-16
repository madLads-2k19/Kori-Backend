from uuid import UUID

from fastapi import APIRouter

import kori.app.services.customer_bill as customer_bill_service
from kori.app.core.config import Settings
from kori.app.core.exceptions import ForbiddenException
from kori.app.schemas.customer_bill import CustomerBillCreate, CustomerBillSchema

customer_bill_router = APIRouter()
config = Settings()

BASE = "/{organization_id}"


@customer_bill_router.post(BASE, response_model=CustomerBillSchema)
def create_customer_bill(organization_id: UUID, bill_request: CustomerBillCreate) -> CustomerBillSchema:
    if organization_id != bill_request.org_id:
        raise ForbiddenException()

    return customer_bill_service.create_customer_bill(organization_id, bill_request)
