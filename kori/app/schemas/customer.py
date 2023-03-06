from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class CustomerBase(BaseModel):
    org_id: UUID
    email: Optional[EmailStr] = None
    is_member: bool = False
    membership_points: int = 0
    address: Optional[str] = None
    preferred_payment_method: Optional[str] = None


class CustomerCreate(CustomerBase):
    name: str
    phone_number: str


class CustomerUpdate(CustomerBase):
    name: Optional[str] = None
    phone_number: Optional[str] = None


class Customer(CustomerCreate):
    id: UUID

    class Config:
        orm_mode = True
