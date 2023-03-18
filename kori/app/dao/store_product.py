from datetime import datetime
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from kori.app.core.config import Settings
from kori.app.core.exceptions import DuplicateRecordException, NotFoundException, StockLevelException
from kori.app.db.connection import DbConnector
from kori.app.models import Product, ProductVersion, StoreProduct
from kori.app.schemas.product import ProductWithStock
from kori.app.schemas.store_product import AggregatedProduct, StoreProductCreate, StoreProductSchema, StoreProductUpdate
from kori.app.utils.dict_utils import remove_null_values

settings = Settings()

db_connector = DbConnector(settings.DATABASE_URI)


def create(store_product_create: StoreProductCreate) -> StoreProductSchema:
    session = db_connector.get_session()

    new_store_product_db = StoreProduct(**store_product_create.dict(), stock_locked=0)

    try:
        session.add(new_store_product_db)
        session.commit()
    except IntegrityError:
        raise DuplicateRecordException(message="Store Product mapping already exists")

    return StoreProductSchema.from_orm(new_store_product_db)


def get_store_product(store_id: UUID, product_id: UUID) -> StoreProductSchema | None:
    session = db_connector.get_session()
    store_products = list(
        session.query(StoreProduct).filter(StoreProduct.store_id == store_id, StoreProduct.product_id == product_id)
    )

    return StoreProductSchema.from_orm(store_products[0]) if len(store_products) > 0 else None


def get_products_by_stores(store_ids: list[UUID]) -> list[AggregatedProduct]:
    session = db_connector.get_session()
    result = (
        session.query(StoreProduct.product_id, func.sum(StoreProduct.stock_available))
        .filter(StoreProduct.store_id.in_(store_ids))
        .group_by(StoreProduct.product_id)
    )
    return [AggregatedProduct(product_id=entry[0], total_stock=entry[1]) for entry in result]


def get_all_store_products_of_store(store_id: UUID) -> list[StoreProductSchema]:
    session = db_connector.get_session()
    store_products = list(session.query(StoreProduct).filter(StoreProduct.store_id == store_id))
    return [StoreProductSchema.from_orm(store_product) for store_product in store_products]


def get_all_store_products_of_products(product_id: UUID) -> list[StoreProductSchema]:
    session = db_connector.get_session()
    store_products = list(session.query(StoreProduct).filter(StoreProduct.product_id == product_id))
    return [StoreProductSchema.from_orm(store_product) for store_product in store_products]


def update(store_id: UUID, product_id: UUID, store_product_update: StoreProductUpdate) -> StoreProductSchema:
    session = db_connector.get_session()
    update_data = remove_null_values(store_product_update.dict())

    updated_count = (
        session.query(StoreProduct)
        .filter(StoreProduct.store_id == store_id, StoreProduct.product_id == product_id)
        .update(update_data)
    )
    session.commit()

    if updated_count == 0:
        raise NotFoundException(message="No records matched for update")

    return get_store_product(store_id, product_id)


def lock_store_product(store_id: UUID, product_id: UUID, lock_quantity: int) -> StoreProductSchema:
    session = db_connector.get_session()
    store_product_records = list(
        session.query(StoreProduct).filter(StoreProduct.store_id == store_id, StoreProduct.product_id == product_id)
    )

    if len(store_product_records) == 0:
        raise NotFoundException()

    store_product_record = store_product_records[0]

    new_total_locked_qty = store_product_record.stock_locked + lock_quantity
    if new_total_locked_qty > store_product_record.stock_available:
        raise StockLevelException()

    store_product_record.stock_locked = new_total_locked_qty
    session.commit()

    return get_store_product(store_id, product_id)


def delete(store_id: UUID, product_id: UUID) -> None:
    session = db_connector.get_session()
    deleted_count = (
        session.query(StoreProduct)
        .filter(StoreProduct.store_id == store_id, StoreProduct.product_id == product_id)
        .delete()
    )
    session.commit()

    if deleted_count == 0:
        raise NotFoundException(message="No records matched for delete")
