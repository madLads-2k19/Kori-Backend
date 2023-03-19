from uuid import UUID

from pydantic import BaseModel, validator

from kori.app.schemas.product import ProductSchema


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

    class Config:
        orm_mode = True


class ProductBilledWithProduct(BaseModel):
    reorder_level: int
    name: str
    price: float
    measurement_unit: str
    product_id: UUID
    product_quantity: float
    total_cost: float
    version_id: int
