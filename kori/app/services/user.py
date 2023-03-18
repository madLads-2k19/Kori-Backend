from uuid import UUID

from pydantic import EmailStr

import kori.app.dao.user as user_dao
from kori.app.core.crypto import hash_password
from kori.app.core.exceptions import NotFoundException
from kori.app.schemas.user import UserCreate, UserCreateRequest, UserSchema, UserUpdate, UserUpdateRequest


def create(org_id: UUID, create_request: UserCreateRequest) -> UserSchema:
    hashed_password = hash_password(create_request.password)
    new_user = UserCreate(**create_request.dict(), org_id=org_id, pass_hash=hashed_password)
    created_user = user_dao.create(new_user)
    return created_user


def get_user_by_id(user_id: UUID) -> UserSchema:
    user = user_dao.get_user_by_id(user_id)
    if not user:
        raise NotFoundException(message="User not found")
    return user


def get_user_by_email(email: EmailStr) -> UserSchema:
    user = user_dao.get_user_by_email(email)
    if not user:
        raise NotFoundException(message="User not found")
    return user


def update(user_id: UUID, update_request: UserUpdateRequest) -> UserSchema:
    hashed_password = None
    if update_request.password:
        hashed_password = hash_password(update_request.password)
    user_update = UserUpdate(**update_request.dict(), pass_hash=hashed_password)
    user = user_dao.update(user_id, user_update)
    if not user:
        raise NotFoundException(message="User not found")
    return user


def delete(user_id: UUID) -> None:
    return user_dao.delete(user_id)
