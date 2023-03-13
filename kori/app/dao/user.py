from uuid import UUID

from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError

from kori.app.core.config import Settings
from kori.app.core.exceptions import DuplicateRecordException
from kori.app.db.connection import DbConnector
from kori.app.models import User
from kori.app.schemas.user import UserCreate, UserSchema, UserUpdate
from kori.app.utils.dict_utils import remove_null_values

config = Settings()
db_connector = DbConnector(config.DATABASE_URI)


def create(user_data: UserCreate) -> UserSchema:
    session = db_connector.get_session()
    new_user_db = User(**user_data.dict())

    try:
        session.add(new_user_db)
        session.commit()
    except IntegrityError:
        raise DuplicateRecordException(message="Similar user already exists")

    return UserSchema.from_orm(new_user_db)


def get_user_by_id(user_id: UUID) -> UserSchema | None:
    session = db_connector.get_session()
    users = list(session.query(User).filter(User.id == user_id))
    fetched_user = next(iter(users), None)
    if fetched_user:
        return UserSchema.from_orm(fetched_user)


def get_user_by_email(org_id: UUID, email: EmailStr) -> UserSchema | None:
    session = db_connector.get_session()
    users = session.query(User).filter(User.org_id == org_id and User.email == email)
    fetched_user = next(iter(users), None)
    if fetched_user:
        return UserSchema.from_orm(fetched_user)


def update(user_id: UUID, user_data: UserUpdate) -> UserSchema:
    session = db_connector.get_session()
    update_data = remove_null_values(user_data.dict())

    try:
        session.query(User).filter(User.id == user_id).update(update_data)
        session.commit()
    except IntegrityError:
        raise DuplicateRecordException(message="Similar user already exists")

    return get_user_by_id(user_id)


def delete(user_id: UUID) -> None:
    session = db_connector.get_session()
    session.query(User).filter(User.id == user_id).delete()
    session.commit()
