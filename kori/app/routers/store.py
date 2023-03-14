from uuid import UUID

from fastapi import APIRouter

import kori.app.dao.store as store_dao
from kori.app.core.config import Settings
from kori.app.core.exceptions import ForbiddenException, NotFoundException
from kori.app.schemas.store import StoreCreate, StoreSchema, StoreUpdate

store_router = APIRouter()
settings = Settings()

BASE = "/{organization_id}"


@store_router.post(BASE, response_model=StoreSchema)
def create_store(organization_id: UUID, store_create: StoreCreate) -> StoreSchema:
    if store_create.org_id != organization_id:
        raise ForbiddenException()

    return store_dao.create(store_create)


@store_router.get(BASE + "/{store_id}", response_model=StoreSchema)
def get_store_by_id(organization_id: UUID, store_id: UUID) -> StoreSchema:
    store = store_dao.get_store_by_id(organization_id, store_id)

    if not store:
        raise NotFoundException()
    return store


@store_router.get(BASE, response_model=list[StoreSchema])
def get_all_stores(organization_id: UUID) -> list[StoreSchema]:
    return store_dao.get_stores_of_organization(organization_id)


@store_router.put(BASE + "/{store_id}", response_model=StoreSchema)
def update_store(organization_id: UUID, store_id: UUID, store_update: StoreUpdate) -> StoreSchema:
    if store_update.org_id != organization_id:
        raise ForbiddenException()

    return store_dao.update(organization_id, store_id, store_update)


@store_router.delete(BASE + "/{store_id}")
def delete_store(organization_id: UUID, store_id: UUID):
    store_dao.delete(organization_id, store_id)
    return "Deleted"
