from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr
    permission_level: str


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: bytes


class UserCreateRequest(UserBase):
    password: bytes


class UserUpdateBase(BaseModel):
    name: str | None
    email: EmailStr | None
    permission_level: str | None


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


class AuthResponse(BaseModel):
    org_id: UUID
    user_id: UUID
    token: str
