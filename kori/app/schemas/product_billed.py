from uuid import UUID

from pydantic import BaseModel, validator


class ProductBilledBase(BaseModel):
    product_id: UUID
    product_quantity: float


class ProductBilledCreate(ProductBilledBase):
    pass


class ProductBilledDbCreate(ProductBilledBase):
    total_cost: float
    version_id: int


class ProductBilledSchema(ProductBilledDbCreate):
    customer_bill_id: UUID
