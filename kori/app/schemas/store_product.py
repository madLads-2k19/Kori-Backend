from uuid import UUID

from pydantic import BaseModel

from kori.app.schemas.product import ProductSchema


class StoreProductBase(BaseModel):
    product_id: UUID
    store_id: UUID
    stock_available: float


class StoreProductCreate(StoreProductBase):
    pass


class StoreProductUpdate(StoreProductBase):
    pass


class StoreProductSchema(StoreProductBase):
    stock_locked: float

    class Config:
        orm_mode = True


class StoreProductWithProduct(StoreProductSchema):
    product: ProductSchema


class AggregatedProduct(BaseModel):
    product_id: UUID
    total_stock: float
