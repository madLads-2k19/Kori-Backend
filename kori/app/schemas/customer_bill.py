from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from kori.app.schemas.product_billed import ProductBilledCreate, ProductBilledSchema


class CustomerBillBase(BaseModel):
    org_id: UUID
    store_id: UUID
    customer_id: UUID
    user_id: UUID
    payment_method: str
    discount_price: float = 0
    delivery_address: str | None = None
    delivery_charge: float = 0


class CustomerBillCreate(CustomerBillBase):
    products_billed: list[ProductBilledCreate]


class CustomerBillDbCreate(CustomerBillBase):
    products_total: float
    net_price: float
    billed_at: datetime


class CustomerBillSchema(CustomerBillDbCreate):
    id: UUID
    products_billed: list[ProductBilledSchema]

    class Config:
        orm_mode = True
