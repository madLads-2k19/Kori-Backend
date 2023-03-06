from uuid import uuid4

from sqlalchemy import Column, String, ForeignKey, Boolean, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from kori.app.db.base import Base


class Customer(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    org_id = Column(ForeignKey("organization.id"))
    name = Column(String)
    email = Column(String)
    phone_number = Column(String)
    is_member = Column(Boolean)
    membership_points = Column(Integer)
    address = Column(Text)
    preferred_payment_method = Column(String)

    organization = relationship("Organization", back_populates="customers")
    customer_bills = relationship("CustomerBill", back_populates="customer")
