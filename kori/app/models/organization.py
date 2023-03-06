from uuid import uuid4

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from kori.app.db.base import Base


class Organization(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String)

    global_configs = relationship("GlobalConfig", back_populates="organization")
    warehouses = relationship("Warehouse", back_populates="organization")
    stores = relationship("Store", back_populates="organization")
    products = relationship("Product", back_populates="organization")
    users = relationship("User", back_populates="organization")
    customers = relationship("Customer", back_populates="organization")
    customer_bills = relationship("CustomerBill", back_populates="organization")
