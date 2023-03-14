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
        timestamp=datetime.now(),
    )


def get_product(product_id: UUID, timestamp: Optional[datetime]) -> ProductSchema:
    session = db_connector.get_session()
    try:
        product = session.query(Product).filter(Product.id == product_id).one()

        if product.is_deleted:
            raise NotFoundException(message="Product is deleted")

        if timestamp:
            product_version = (
                session.query(ProductVersion)
                .filter(ProductVersion.valid_from <= timestamp, ProductVersion.valid_to == "9999-12-31 23:59:59.999999")
                .one()
            )
        else:
            product_version = (
                session.query(ProductVersion)
                .filter(
                    ProductVersion.product_id == product_id, ProductVersion.valid_to == "9999-12-31 23:59:59.999999"
                )
                .one()
            )

    except NoResultFound:
        raise NotFoundException(message="Product Details not found")

    return ProductSchema(
        product_id=product.id,
        reorder_level=product.reorder_level,
        version_id=product_version.version_id,
        org_id=product.org_id,
        name=product_version.name,
        price=product_version.price,
        measurement_unit=product_version.measurement_unit,
        timestamp=timestamp or datetime.now(),
    )


def update(product_id: UUID, product_data: ProductUpdate) -> ProductSchema:
    session = db_connector.get_session()
    try:
        existing_product = session.query(Product).filter(Product.id == product_id).one()

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

    if not (
        updated_product_version_data["name"] == latest_product_version.name
        and updated_product_version_data["price"] == latest_product_version.price
        and updated_product_version_data["measurement_unit"] == latest_product_version.measurement_unit
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
        timestamp=datetime.now(),
        **updated_product_version_data,
    )


def delete(product_id: UUID) -> None:
    session = db_connector.get_session()

    try:
        existing_product = session.query(Product).filter(Product.id == product_id).one()
    except NoResultFound:
        raise NotFoundException(message="Product not found")

    existing_product.is_deleted = True
    session.commit()
