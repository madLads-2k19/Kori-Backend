from uuid import uuid4

from sqlalchemy import Column, String, ForeignKey, Integer, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.types import TIMESTAMP


from kori.app.db.base import Base


class CustomerBill(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    org_id = Column(ForeignKey("organization.id"))
    store_id = Column(ForeignKey("store.id"))
    customer_id = Column(ForeignKey("customer.id"))
    user_id = Column(ForeignKey("user.id"))
    payment_method = Column(String)
    products_total = Column(Numeric)
    discount_price = Column(Numeric)
    delivery_address = Column(Text)
    delivery_charge = Column(Numeric)
    net_price = Column(Numeric)
    billed_at = Column(TIMESTAMP)

    organization = relationship("Organization", back_populates="customer_bills")
    store = relationship("Store", back_populates="customer_bills")
    customer = relationship("Customer", back_populates="customer_bills")
    user = relationship("User", back_populates="customer_bills")
    products_billed = relationship("ProductBilled", back_populates="customer_bill")
