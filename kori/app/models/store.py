from uuid import uuid4

from sqlalchemy import Column, String, ForeignKey, Boolean, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from kori.app.db.base import Base


class Store(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    org_id = Column(ForeignKey("organization.id"))
    name = Column(String)

    organization = relationship("Organization", back_populates="stores")
    customer_bills = relationship("CustomerBill", back_populates="store")
    store_products = relationship("StoreProduct", back_populates="store")

