from datetime import datetime
from typing import Optional
from uuid import UUID

import kori.app.dao.product as product_dao
import kori.app.dao.store_product as store_product_dao
from kori.app.schemas.product import ProductCreate, ProductCreateRequest, ProductSchema, ProductUpdate, ProductWithStock


def create(org_id: UUID, product_data: ProductCreateRequest) -> ProductSchema:
    product_create = ProductCreate(org_id=org_id, **product_data.dict())
    return product_dao.create(product_data=product_create)


def get_product(product_id: UUID, timestamp: Optional[datetime] = None) -> ProductSchema:
    return product_dao.get_product(product_id=product_id, timestamp=timestamp)


def get_products_by_stores(store_ids: list[UUID], product_name: str | None = None) -> list[ProductWithStock]:
    aggregated_products = store_product_dao.get_products_by_stores(store_ids)
    stock_mapping = {product.product_id: product.total_stock for product in aggregated_products}
    products = product_dao.get_products_by_name(list(stock_mapping.keys()), product_name)
    return [
        ProductWithStock(**product.dict(), total_stock=stock_mapping.get(product.product_id)) for product in products
    ]


def update(product_id: UUID, product_data: ProductUpdate) -> ProductSchema:
    return product_dao.update(product_id=product_id, product_data=product_data)


def delete(product_id: UUID) -> None:
    return product_dao.delete(product_id=product_id)
