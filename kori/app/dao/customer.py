from uuid import UUID

from sqlalchemy.exc import IntegrityError

from kori.app.core.config import Settings
from kori.app.core.exceptions import DuplicateRecordException
from kori.app.db.connection import DbConnector
from kori.app.models.customer import Customer
from kori.app.schemas.customer import CustomerCreate, CustomerSchema, CustomerUpdate
from kori.app.utils.dict_utils import remove_null_values

config = Settings()

db_connector = DbConnector(config.DATABASE_URI)


def create(customer_data: CustomerCreate) -> CustomerSchema:
    session = db_connector.get_session()
    new_customer_db = Customer(**customer_data.dict())

    try:
        session.add(new_customer_db)
        session.commit()
    except IntegrityError:
        raise DuplicateRecordException(message="Account with similar phone number already exists.")

    return CustomerSchema.from_orm(new_customer_db)


def get_customer_by_id(customer_id: UUID) -> CustomerSchema | None:
    session = db_connector.get_session()
    customer = session.query(Customer).filter(Customer.id == customer_id).one_or_none()
    return CustomerSchema.from_orm(customer) if customer else None


def get_customer_by_number(phone_number: str) -> CustomerSchema | None:
    session = db_connector.get_session()
    customer = session.query(Customer).filter(Customer.phone_number == phone_number).one_or_none()
    return CustomerSchema.from_orm(customer) if customer else None


def update(customer_id: UUID, customer_data: CustomerUpdate) -> CustomerSchema | None:
    session = db_connector.get_session()
    update_data = remove_null_values(customer_data.dict())

    try:
        session.query(Customer).filter(Customer.id == customer_id).update(update_data)
        session.commit()
    except IntegrityError:
        raise DuplicateRecordException(message="Account with similar phone number already exists.")

    return get_customer_by_id(customer_id)


def delete(customer_id: UUID) -> None:
    session = db_connector.get_session()
    session.query(Customer).filter(Customer.id == customer_id).delete()
    session.commit()
