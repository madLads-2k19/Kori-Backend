from uuid import UUID

from pydantic import BaseModel


class StoreProductBase(BaseModel):
    product_id: UUID
    store_id: UUID
    stock_available: int


class StoreProductCreate(StoreProductBase):
    pass


class StoreProductUpdate(StoreProductBase):
    pass


class StoreProductSchema(StoreProductBase):
    stock_locked: int

    class Config:
        orm_mode = True
