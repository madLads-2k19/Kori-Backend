from uuid import UUID

from sqlalchemy.exc import IntegrityError

from kori.app.core.config import Settings
from kori.app.core.exceptions import DuplicateRecordException
from kori.app.db.connection import DbConnector
from kori.app.models.customer import CustomerOrm
from kori.app.schemas.customer import Customer, CustomerCreate, CustomerUpdate
from kori.app.utils.dict_utils import remove_null_values

settings = Settings()

db_connector = DbConnector(settings.DATABASE_URI)


def create(customer_data: CustomerCreate) -> Customer:
    session = db_connector.get_session()
    new_customer_db = CustomerOrm(**customer_data.dict())

    try:
        session.add(new_customer_db)
        session.commit()
    except IntegrityError:
        raise DuplicateRecordException(message="Account with similar phone number already exists.")

    return Customer.from_orm(new_customer_db)


def get_customer_by_id(customer_id: UUID) -> Customer | None:
    session = db_connector.get_session()
    customers = list(session.query(CustomerOrm).filter(CustomerOrm.id == customer_id))
    return Customer.from_orm(customers[0]) if customers else None


def get_customer_by_number(phone_number: str) -> Customer | None:
    session = db_connector.get_session()
    customers = list(session.query(CustomerOrm).filter(CustomerOrm.phone_number == phone_number))
    return Customer.from_orm(customers[0]) if customers else None


def update(customer_id: UUID, customer_data: CustomerUpdate) -> Customer:
    session = db_connector.get_session()
    update_data = remove_null_values(customer_data.dict())

    try:
        session.query(CustomerOrm).filter(CustomerOrm.id == customer_id).update(update_data)
        session.commit()
    except IntegrityError:
        raise DuplicateRecordException(message="Account with similar phone number already exists.")

    return get_customer_by_id(customer_id)


def delete(phone_number: str) -> None:
    session = db_connector.get_session()
    session.query(CustomerOrm).filter(CustomerOrm.phone_number == phone_number).delete()
    session.commit()
