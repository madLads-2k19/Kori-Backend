import re
from uuid import UUID

from pydantic import BaseModel, EmailStr, validator


class CustomerBase(BaseModel):
    email: EmailStr | None = None
    is_member: bool = False
    membership_points: int = 0
    address: str | None = None
    preferred_payment_method: str | None = None


class CustomerCreateRequest(CustomerBase):
    name: str
    phone_number: str

    @validator("phone_number")
    def validate_phone_number(cls, value: str) -> str:
        match = re.search(r"^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$", value)
        if not match:
            raise ValueError("Invalid phone number")
        return value


class CustomerUpdate(CustomerBase):
    name: str | None = None
    phone_number: str | None = None

    @validator("phone_number")
    def validate_phone_number(cls, value: str | None) -> str | None:
        if not value:
            return
        match = re.search(r"^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$", value)
        if not match:
            raise ValueError("Invalid phone number")
        return value


class CustomerCreate(CustomerCreateRequest):
    org_id: UUID


class CustomerSchema(CustomerCreate):
    id: UUID

    class Config:
        orm_mode = True
