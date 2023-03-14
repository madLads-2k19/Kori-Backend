from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import APIRouter

import kori.app.services.product as product_service
from kori.app.core.config import Settings
from kori.app.schemas.product import ProductCreateRequest, ProductSchema, ProductUpdate

product_router = APIRouter()
settings = Settings()


@product_router.post("/{org_id}", response_model=ProductSchema)
def create_product(org_id: UUID, product_data: ProductCreateRequest) -> ProductSchema:
    return product_service.create(org_id=org_id, product_data=product_data)


@product_router.get("/{product_id}", response_model=ProductSchema)
def get_product_by_id(product_id: UUID, timestamp: Optional[datetime] = None) -> ProductSchema:
    return product_service.get_product(product_id=product_id, timestamp=timestamp)


@product_router.put("/{product_id}", response_model=ProductSchema)
def update_product(product_id: UUID, product_data: ProductUpdate) -> ProductSchema:
    return product_service.update(product_id=product_id, product_data=product_data)


@product_router.delete("/{product_id}")
def delete_product(product_id: UUID):
    product_service.delete(product_id)
    return "Deleted"
