from uuid import UUID

from pydantic import BaseModel


class ProductBase(BaseModel):
    reorder_level: int


class ProductCreateRequest(ProductBase):
    name: str
    price: float
    measurement_unit: str


class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = None
    measurement_unit: str | None = None


class ProductCreate(ProductCreateRequest):
    org_id: UUID


class ProductSchema(ProductCreate):
    product_id: UUID
    version_id: int
