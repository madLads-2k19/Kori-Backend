from datetime import datetime
from uuid import UUID

import kori.app.dao.product as product_dao
from kori.app.schemas.product import ProductCreate, ProductCreateRequest, ProductSchema, ProductUpdate


def create(org_id: UUID, product_data: ProductCreateRequest) -> ProductSchema:
    product_create = ProductCreate(org_id=org_id, **product_data.dict())
    return product_dao.create(product_data=product_create)


def get_latest_product_by_id(product_id: UUID) -> ProductSchema:
    return product_dao.get_latest_product_by_id(product_id=product_id)


def get_product_by_timestamp(product_id: UUID, timestamp: datetime) -> ProductSchema:
    return product_dao.get_product_by_timestamp(product_id=product_id, timestamp=timestamp)


def update(product_id: UUID, product_data: ProductUpdate) -> ProductSchema:
    return product_dao.update(product_id=product_id, product_data=product_data)


def delete(product_id: UUID) -> None:
    return product_dao.delete(product_id=product_id)
