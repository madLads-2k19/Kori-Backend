from uuid import UUID

from fastapi import APIRouter

import kori.app.dao.product as product_dao
import kori.app.dao.store as store_dao
import kori.app.dao.store_product as store_product_dao
from kori.app.core.config import Settings
from kori.app.core.exceptions import ForbiddenException
from kori.app.schemas.store_product import (
    StoreProductCreate,
    StoreProductSchema,
    StoreProductUpdate,
    StoreProductWithProduct,
)

store_product_router = APIRouter()
settings = Settings()

BASE = "/{organization_id}"


@store_product_router.post(BASE, response_model=StoreProductSchema)
def create_store_product_mapping(organization_id: UUID, store_product_create: StoreProductCreate) -> StoreProductSchema:
    store = store_dao.get_store_by_id(organization_id, store_product_create.store_id)
    product = product_dao.get_product(store_product_create.product_id)

    if store is None or product.org_id != organization_id:
        raise ForbiddenException()

    return store_product_dao.create(store_product_create)


@store_product_router.get(BASE + "/store/{store_id}/product/{product_id}", response_model=StoreProductSchema)
def get_store_product(organization_id: UUID, store_id: UUID, product_id: UUID) -> StoreProductSchema:
    store = store_dao.get_store_by_id(organization_id, store_id)
    if store is None:
        raise ForbiddenException()

    return store_product_dao.get_store_product(store_id, product_id)


@store_product_router.get(BASE + "/store/{store_id}", response_model=list[StoreProductWithProduct])
def get_all_store_products_of_store(organization_id: UUID, store_id: UUID) -> list[StoreProductWithProduct]:
    store = store_dao.get_store_by_id(organization_id, store_id)
    if store is None:
        raise ForbiddenException()

    return store_product_dao.get_all_store_products_of_store(store_id)


@store_product_router.get(BASE + "/product/{product_id}", response_model=list[StoreProductSchema])
def get_all_store_products_of_product(organization_id: UUID, product_id: UUID) -> list[StoreProductSchema]:
    product = product_dao.get_product(product_id)
    if product.org_id != organization_id:
        raise ForbiddenException()

    return store_product_dao.get_all_store_products_of_products(product_id)


@store_product_router.delete(BASE + "/{store_id}/{product_id}")
def delete_store(organization_id: UUID, store_id: UUID, product_id: UUID):
    store = store_dao.get_store_by_id(organization_id, store_id)
    if store is None:
        raise ForbiddenException()

    store_product_dao.delete(store_id, product_id)
    return "Deleted"
