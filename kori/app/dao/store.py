from uuid import UUID

from kori.app.core.config import Settings
from kori.app.core.exceptions import NotFoundException
from kori.app.db.connection import DbConnector
from kori.app.models import Organization, Store
from kori.app.schemas.store import StoreCreate, StoreSchema, StoreUpdate
from kori.app.utils.dict_utils import remove_null_values

settings = Settings()

db_connector = DbConnector(settings.DATABASE_URI)


def create(store_create: StoreCreate) -> StoreSchema:
    session = db_connector.get_session()
    new_org_db = Store(**store_create.dict())

    session.add(new_org_db)
    session.commit()

    return StoreSchema.from_orm(new_org_db)


def get_store_by_id(organization_id: UUID, store_id: UUID) -> StoreSchema:
    session = db_connector.get_session()
    stores = list(session.query(Store).filter(Store.org_id == organization_id, Store.id == store_id))

    if len(stores) == 0:
        raise NotFoundException()

    return StoreSchema.from_orm(stores[0])


def get_stores_of_organization(organization_id) -> list[StoreSchema]:
    session = db_connector.get_session()
    stores = list(session.query(Store).filter(Store.org_id == organization_id))
    return [StoreSchema.from_orm(store) for store in stores]


def update(organization_id: UUID, store_id: UUID, store_update: StoreUpdate) -> StoreSchema:
    session = db_connector.get_session()
    update_data = remove_null_values(store_update.dict())

    updated_count = (
        session.query(Store).filter(Organization.id == organization_id, Store.id == store_id).update(update_data)
    )
    session.commit()

    if updated_count == 0:
        raise NotFoundException(message="No records matched for update")

    return get_store_by_id(organization_id, store_id)


def delete(organization_id: UUID, store_id: UUID) -> None:
    session = db_connector.get_session()
    deleted_count = session.query(Store).filter(Organization.id == organization_id, Store.id == store_id).delete()
    session.commit()

    if deleted_count == 0:
        raise NotFoundException(message="No records matched for delete")
