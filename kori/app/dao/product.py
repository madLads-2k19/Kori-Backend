from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy.exc import IntegrityError, NoResultFound

from kori.app.core.config import Settings
from kori.app.core.exceptions import NotFoundException
from kori.app.db.connection import DbConnector
from kori.app.models import ProductVersion
from kori.app.models.product import Product
from kori.app.schemas.product import ProductCreate, ProductSchema, ProductUpdate

settings = Settings()

db_connector = DbConnector(settings.DATABASE_URI)


def create(product_data: ProductCreate) -> ProductSchema:
    session = db_connector.get_session()

    new_product_db = Product(org_id=product_data.org_id, reorder_level=product_data.reorder_level)

    with session.begin() as transaction:
        try:
            session.add(new_product_db)
            session.flush()

            new_product_version_db = ProductVersion(
                version_id=1,
                product_id=new_product_db.id,
                name=product_data.name,
                price=product_data.price,
                measurement_unit=product_data.measurement_unit,
                valid_from=datetime.now(),
                valid_to=datetime(9999, 12, 31, 23, 59, 59, 999999),
            )

            session.add(new_product_version_db)
            transaction.commit()
        except IntegrityError:
            raise NotFoundException(message="Organisation not found.")
        except Exception:
            transaction.rollback()

    return ProductSchema(
        product_id=new_product_db.id,
        reorder_level=new_product_db.reorder_level,
        version_id=new_product_version_db.version_id,
        org_id=new_product_db.org_id,
        name=new_product_version_db.name,
        price=new_product_version_db.price,
        measurement_unit=new_product_version_db.measurement_unit,
    )


def get_products_by_organisation(org_id: UUID) -> list[ProductSchema]:
    session = db_connector.get_session()
    current_timestamp = datetime.now()

    product_list = session.query(Product).filter(Product.org_id == org_id)

    response_product_list = []
    for product in product_list:
        product_version = (
            session.query(ProductVersion)
            .filter(
                ProductVersion.product_id == product.id,
                ProductVersion.valid_from <= current_timestamp,
                ProductVersion.valid_to >= current_timestamp,
            )
            .one()
        )
        response_product_list.append(
            ProductSchema(
                product_id=product.id,
                reorder_level=product.reorder_level,
                version_id=product_version.version_id,
                org_id=product.org_id,
                name=product_version.name,
                price=product_version.price,
                measurement_unit=product_version.measurement_unit,
            )
        )

    return response_product_list


def get_product(product_id: UUID, timestamp: Optional[datetime] = None) -> ProductSchema:
    if not timestamp:
        timestamp = datetime.now()

    session = db_connector.get_session()
    try:
        product = session.query(Product).get(product_id)

        if not product:
            raise NotFoundException(message="Product Details not found")

        if product.is_deleted:
            raise NotFoundException(message="Product is deleted")
        product_version = (
            session.query(ProductVersion)
            .filter(
                ProductVersion.product_id == product_id,
                ProductVersion.valid_from <= timestamp,
                ProductVersion.valid_to >= timestamp,
            )
            .one()
        )

    except NoResultFound as e:
        raise NotFoundException(message="Product Details not found")

    return ProductSchema(
        product_id=product.id,
        reorder_level=product.reorder_level,
        version_id=product_version.version_id,
        org_id=product.org_id,
        name=product_version.name,
        price=product_version.price,
        measurement_unit=product_version.measurement_unit,
    )


def get_products_by_name(product_ids: list[UUID], product_name: str | None = None) -> list[ProductSchema]:
    session = db_connector.get_session()
    current_timestamp = datetime.now()
    product_versions = session.query(ProductVersion).filter(
        ProductVersion.product_id.in_(product_ids),
        ProductVersion.valid_from < current_timestamp,
        current_timestamp <= ProductVersion.valid_to,
    )
    if product_name:
        product_versions = product_versions.filter(ProductVersion.name.like(f"%{product_name}%"))

    products = []
    for product_version in product_versions:
        product = product_version.product
        products.append(
            ProductSchema(
                reorder_level=product.reorder_level,
                name=product_version.name,
                price=product_version.price,
                measurement_unit=product_version.measurement_unit,
                org_id=product.org_id,
                product_id=product.id,
                version_id=product_version.version_id,
            )
        )
    return products


def get_product_by_version_id(product_id: UUID, version_id: int) -> ProductSchema | None:
    session = db_connector.get_session()
    product_version = (
        session.query(ProductVersion)
        .filter(ProductVersion.product_id == product_id, ProductVersion.version_id == version_id)
        .one_or_none()
    )
    product = product_version.product
    return ProductSchema(
        reorder_level=product.reorder_level,
        name=product_version.name,
        price=product_version.price,
        measurement_unit=product_version.measurement_unit,
        org_id=product.org_id,
        product_id=product.id,
        version_id=product_version.version_id,
    )


def update(product_id: UUID, product_data: ProductUpdate) -> ProductSchema:
    session = db_connector.get_session()
    try:
        existing_product = session.query(Product).get(product_id)

        if not existing_product:
            raise NotFoundException(message="Product Details not found")

        latest_product_version = (
            session.query(ProductVersion)
            .filter(ProductVersion.product_id == product_id, ProductVersion.valid_to == "9999-12-31 23:59:59.999999")
            .one()
        )
    except NoResultFound:
        raise NotFoundException(message="Product Details not found")

    current_time = datetime.now()
    latest_product_version.valid_to = current_time

    updated_product_version_data = {
        "name": product_data.name or latest_product_version.name,
        "price": product_data.price or latest_product_version.price,
        "measurement_unit": product_data.measurement_unit or latest_product_version.measurement_unit,
    }
    version_id = latest_product_version.version_id

    if any(
        updated_product_version_data[k] != getattr(latest_product_version, k)
        for k in ["name", "measurement_unit", "price"]
    ):
        # Create a new version of the product with updated version_id
        new_product_version_db = ProductVersion(
            version_id=latest_product_version.version_id + 1,
            product_id=product_id,
            valid_from=current_time,
            valid_to=datetime(9999, 12, 31, 23, 59, 59, 999999),
            **updated_product_version_data,
        )

        session.add(new_product_version_db)
        session.commit()

        version_id = new_product_version_db.version_id

    return ProductSchema(
        product_id=product_id,
        reorder_level=existing_product.reorder_level,
        version_id=version_id,
        org_id=existing_product.org_id,
        **updated_product_version_data,
    )


def delete(product_id: UUID) -> None:
    session = db_connector.get_session()

    existing_product = session.query(Product).get(product_id)

    if not existing_product:
        raise NotFoundException(message="Product Details not found")

    existing_product.is_deleted = True
    session.commit()
