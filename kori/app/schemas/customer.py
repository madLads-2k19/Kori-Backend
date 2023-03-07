from uuid import UUID

from pydantic import BaseModel, EmailStr


class CustomerBase(BaseModel):
    org_id: UUID
    email: EmailStr | None = None
    is_member: bool = False
    membership_points: int = 0
    address: str | None = None
    preferred_payment_method: str | None = None


class CustomerCreate(CustomerBase):
    name: str
    phone_number: str


class CustomerUpdate(CustomerBase):
    name: str | None = None
    phone_number: str | None = None


class Customer(CustomerCreate):
    id: UUID

    class Config:
        orm_mode = True
