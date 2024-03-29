from enum import Enum
from uuid import UUID

from pydantic import BaseModel, EmailStr


class PermissionLevel(str, Enum):
    user = "user"
    admin = "admin"


class UserBase(BaseModel):
    name: str
    email: EmailStr
    permission_level: PermissionLevel
    default_store_id: UUID | None


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: bytes


class UserCreateRequest(UserBase):
    password: bytes


class UserUpdateBase(BaseModel):
    name: str | None
    email: EmailStr | None
    permission_level: PermissionLevel | None
    default_store_id: UUID | None


class UserUpdateRequest(UserUpdateBase):
    password: bytes | None


class UserUpdate(UserUpdateBase):
    pass_hash: bytes | None


class UserCreate(UserBase):
    org_id: UUID
    pass_hash: bytes


class UserSchema(UserCreate):
    id: UUID

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    user_id: str
    org_id: str
    exp: int | None


class AuthResponse(UserBase):
    org_id: UUID
    user_id: UUID
    token: str
