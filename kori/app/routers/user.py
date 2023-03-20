from uuid import UUID

from fastapi import APIRouter, Depends

import kori.app.services.user as user_service
from kori.app.core.config import Settings
from kori.app.core.crypto import verify_password
from kori.app.core.exceptions import AuthException
from kori.app.schemas.user import AuthResponse, UserCreateRequest, UserLoginRequest, UserSchema, UserUpdateRequest
from kori.app.services import auth as auth_service

user_router = APIRouter()
config = Settings()


@user_router.post("/{org_id}/signup", response_model=AuthResponse)
def signup(org_id: UUID, user_create_request: UserCreateRequest) -> AuthResponse:
    new_user = user_service.create(org_id, user_create_request)
    access_token = auth_service.create_access_token(new_user)
    return AuthResponse(
        name=new_user.name,
        email=new_user.email,
        permission_level=new_user.permission_level,
        default_store_id=new_user.default_store_id,
        org_id=new_user.org_id,
        user_id=new_user.id,
        token=access_token,
    )


@user_router.post("/login", response_model=AuthResponse)
def login(login_request: UserLoginRequest) -> AuthResponse:
    existing_user = user_service.get_user_by_email(login_request.email)
    if not existing_user:
        raise AuthException(message="Invalid email id")
    if not verify_password(login_request.password, existing_user.pass_hash):
        raise AuthException(message="Invalid password")
    access_token = auth_service.create_access_token(existing_user)
    return AuthResponse(
        name=existing_user.name,
        email=existing_user.email,
        permission_level=existing_user.permission_level,
        default_store_id=existing_user.default_store_id,
        org_id=existing_user.org_id,
        user_id=existing_user.id,
        token=access_token,
    )


@user_router.get("/{org_id}", response_model=UserSchema)
def get_user(org_id: UUID, user_id: UUID, user: UserSchema = Depends(auth_service.verify_access)) -> UserSchema:
    return user_service.get_user_by_id(user_id)


@user_router.put("/{org_id}", response_model=UserSchema)
def update_user(
    org_id: UUID,
    user_id: UUID,
    update_request: UserUpdateRequest,
    user: UserSchema = Depends(auth_service.verify_access),
) -> UserSchema:
    return user_service.update(user_id, update_request)


@user_router.delete("/{org_id}")
def delete_user(org_id: UUID, user_id: UUID, user: UserSchema = Depends(auth_service.verify_access)):
    user_service.delete(user_id)
    return "Deleted"
